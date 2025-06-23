import pytz
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, Lesson, Booking, Category, Material, YouTubeVideo, Availability, User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import logging
from .models import ContactMessage
from .forms import ContactForm
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.encoding import force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Events
from django.http import JsonResponse
from .paypal_utils import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from .models import UserProfile
import json
from datetime import datetime
from .models import Article
from django.http import JsonResponse
from .models import Booking, Lesson
from django.http import HttpResponseBadRequest




logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'bookings/index.html')

def privacy_policy(request):
    return render(request, 'bookings/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'bookings/terms_and_conditions.html')

@login_required
def payment_page(request):
    lesson_id = request.GET.get('lesson_id')
    if not lesson_id:
        messages.error(request, "Invalid lesson selected.")
        return redirect('available_lessons')

    try:
        lesson = Lesson.objects.get(id=int(lesson_id))
    except (Lesson.DoesNotExist, ValueError):
        messages.error(request, "Lesson not found.")
        return redirect('available_lessons')

    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    # Sample payment methods - you can replace this with dynamic data if needed
    payment_methods = [
        {"name": "Debit / credit card", "icon": "card-icon.png"},
        {"name": "PayPal", "icon": "paypal-icon.png"},
        {"name": "WebMoney", "icon": "webmoney-icon.png"},
        {"name": "Skrill eWallet", "icon": "skrill-icon.png"},
        {"name": "Bank Transfer", "icon": "bank-icon.png"},
    ]

    return render(request, 'bookings/payment.html', {
        'lesson': lesson,
        'start_time': start_time,
        'end_time': end_time,
        'payment_methods': payment_methods,
    })

@login_required
def create_ameria_payment(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    # Prepare the data to send to Ameria Bank’s payment API
    payload = {
        "merchant_id": settings.AMERIA_MERCHANT_ID,
        "amount": str(lesson.price),
        "currency": "AMD",
        "order_id": lesson_id,  # You can replace this with a unique ID
        "description": f"Payment for lesson: {lesson.title}",
        "callback_url": request.build_absolute_uri(reverse('ameria_payment_return')),
        "cancel_url": request.build_absolute_uri(reverse('ameria_payment_cancel'))
    }

    # Make the API request
    response = requests.post(f"{settings.AMERIA_ENDPOINT}/initiate-payment", json=payload, headers={
        "Authorization": f"Bearer {settings.AMERIA_API_KEY}"
    })

    if response.status_code == 200:
        payment_url = response.json().get('payment_url')
        return redirect(payment_url)
    else:
        return JsonResponse({"error": "Failed to initiate payment with Ameria Bank."}, status=500)


@login_required
def ameria_payment_return(request):
    # Handle successful payment, e.g., verify payment status and update booking
    return redirect('payment_success')
@login_required
def ameria_payment_cancel(request):
    # Handle canceled payment
    return redirect('payment_failure')



@login_required
def create_paypal_payment(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('paypal_return')),
            "cancel_url": request.build_absolute_uri(reverse('paypal_cancel'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": lesson.title,
                    "sku": f"lesson-{lesson_id}",
                    "price": str(lesson.price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(lesson.price),
                "currency": "USD"
            },
            "description": f"Payment for lesson: {lesson.title}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return JsonResponse({"error": "An error occurred during PayPal payment creation."}, status=500)



@login_required
def paypal_return(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment successful
        return redirect('payment_success')  # Show success page
    else:
        # Payment failed
        return redirect('payment_failure')  # Show failure page


@login_required
def paypal_cancel(request):
    return redirect('payment_failure')



def email_verification_pending(request):
    return render(request, 'bookings/email_verification_pending.html')


def send_verification_email(user, request):
    """
    Send a verification email with a unique token to activate the user's account.
    """
    current_site = get_current_site(request)
    subject = "Activate Your Account"
    html_message = render_to_string('registration/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body='Please use an HTML-compatible email client to view this message.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(html_message, "text/html")
    email.send()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True  # Activate the user's account
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('signup')





def category_lessons(request, category_id):
    """ Display lessons under a specific category """
    category = get_object_or_404(Category, id=category_id)
    lessons = Lesson.objects.filter(category=category, status='active')
    return render(request, 'bookings/category_lessons.html', {
        'category': category,
        'lessons': lessons,
        'lesson_description': category.lesson_description  # Passing description to the template
    })


def homepage(request):
    """ Display homepage with teacher info, categories, materials, and YouTube videos """
    teacher = Teacher.objects.first()
    categories = Category.objects.all()  # Get all lesson categories
    material_categories = Category.objects.prefetch_related('materials').all()  # Get material categories
    youtube_videos = YouTubeVideo.objects.all()  # Get YouTube videos

    # Pass all relevant data to the template
    return render(request, 'bookings/homepage.html', {
        'teacher': teacher,
        'categories': categories,
        'material_categories': material_categories,
        'youtube_videos': youtube_videos,
    })


@login_required
def materials_by_category(request, category_id):
    """ Display materials by selected category """
    category = get_object_or_404(Category, id=category_id)
    materials = Material.objects.filter(category=category)

    # Pass category and description to the template
    return render(request, 'bookings/materials_by_category.html', {
        'category': category,
        'materials': materials,
        'description': category.material_description  # Use the correct attribute
    })


def available_lessons(request):
    """ Display all available lessons """
    lessons = Lesson.objects.filter(status='active')
    teacher = Teacher.objects.first()
    return render(request, 'bookings/available_lessons.html', {
        'lessons': lessons,
        'teacher': teacher,
    })


def contact(request):
    """ Handle contact form submission """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            try:
                # Save message to the database
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    message=message
                )

                # Send email
                send_mail(
                    f"Message from {name}",
                    message,
                    email,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully.')
            except Exception as e:
                print(f"Error: {e}")  # Optional: Log the exception
                messages.error(request, 'Failed to send your message. Please try again later.')

            return redirect('homepage')
        else:
            # If form is not valid, render with errors
            messages.error(request, 'Please check your form and try again.')
    else:
        form = ContactForm()

    return render(request, 'bookings/contact.html', {'form': form})


@login_required
def booking_form(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    teacher = lesson.teacher

    # Fetch all availability slots (both booked and unbooked)
    availability = Availability.objects.filter(
        teacher=teacher,
        available_date__gte=timezone.now().date()  # Only fetch future dates
    )

    events = []
    for slot in availability:
        start_datetime = timezone.make_aware(datetime.combine(slot.available_date, slot.start_time))
        end_datetime = timezone.make_aware(datetime.combine(slot.available_date, slot.end_time))

        # Check if the slot is booked (related Booking exists)
        is_booked = hasattr(slot, 'booking') and slot.booking is not None

        events.append({
            "title": "Booked" if is_booked else f"{teacher.name}",
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
            "lessonId": lesson.id,
            "extendedProps": {
                "teacherName": teacher.name,
                "booked": is_booked,  # Pass booked status to the frontend
            }
        })

    return render(request, 'bookings/booking_form.html', {
        'lesson': lesson,
        'events': json.dumps(events),
    })


def payment_page(request):
    selected_slots_json = request.GET.get('selected_slots')
    selected_slots = json.loads(selected_slots_json) if selected_slots_json else []

    # Retrieve the first lesson ID if available in selected slots
    lesson_id = selected_slots[0].get('lessonId') if selected_slots else None
    lesson = get_object_or_404(Lesson, id=lesson_id) if lesson_id else None

    # Calculate the total price based on the number of selected slots
    total_price = lesson.price * len(selected_slots) if lesson else 0

    return render(request, 'bookings/payment.html', {
        'lesson': lesson,
        'selected_slots': selected_slots,
        'total_price': total_price,  # Pass the total price to the template
    })


def calendar_view(request):
    return render(request, 'bookings/calendar.html')


def get_availability_events(request):
    availabilities = Availability.objects.filter(booking__isnull=True)
    events = []

    for availability in availabilities:
        events.append({
            'title': f"{availability.teacher.name} - {availability.start_time} - {availability.end_time}",
            'start': f"{availability.available_date}T{availability.start_time}",
            'end': f"{availability.available_date}T{availability.end_time}",
            'extendedProps': {
                'teacherName': availability.teacher.name,

            }
        })

    return JsonResponse(events, safe=False)



def send_booking_notification(booking):
    """ Send email notification to admin for a new booking """
    subject = f'New Booking Alert: {booking.lesson.title}'
    message = f"New booking by {booking.student_name} for {booking.lesson.title} on {booking.date}."
    try:
        send_mail(subject, message, 'no-reply@yourdomain.com', ['sasszeyn@gmail.com'], fail_silently=False)
    except:
        print('Failed to send booking notification email.')


def send_confirmation_email(booking):
    """ Send confirmation email to the student once the booking is confirmed """
    subject = 'Lesson Booking Confirmed'
    message = f'Your booking for {booking.lesson.title} on {booking.date} has been confirmed.'
    try:
        send_mail(subject, message, 'no-reply@yourdomain.com', [booking.student_email], fail_silently=False)
    except:
        print('Failed to send confirmation email.')


def category_list(request):
    """ Display all categories """
    categories = Category.objects.all()
    return render(request, 'bookings/categories.html', {
        'categories': categories,
    })


def signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # This prevents the user from logging in before email confirmation
            user.save()

            # Send the email verification
            send_verification_email(user, request)

            messages.success(request, 'Almost there! 🎉 We’ve sent an email to your address. Please click the link in that email to activate your account and start booking your lessons!')
        else:
            messages.error(request, 'Registration failed. Please check the form and try again.')
    else:
        form = StudentSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})




def logout_view(request):
    """ Handle user logout """
    logout(request)
    return redirect('homepage')


@login_required
def materials(request):
    """ Display all materials """
    materials_list = Material.objects.all()
    return render(request, 'bookings/materials.html', {
        'materials': materials_list
    })


def about(request):
    """ Display the 'About Me' page """
    return render(request, 'bookings/about.html')


def homepage_youtube(request):
    """ Display homepage with YouTube videos """
    youtube_videos = YouTubeVideo.objects.all()
    return render(request, 'bookings/homepage.html', {
        'youtube_videos': youtube_videos,
    })


def articles_view(request):
    articles = Article.objects.order_by('-published_at')  # Order by most recent first
    return render(request, 'bookings/articles.html', {'articles': articles})


@login_required
def initiate_mock_payment(request):
    """Initiates a mock payment and redirects to a confirmation page."""
    selected_slots_json = request.GET.get('selected_slots')
    selected_slots = json.loads(selected_slots_json) if selected_slots_json else []

    # Assuming at least one slot has been selected
    lesson_id = selected_slots[0].get('lessonId') if selected_slots else None
    lesson = get_object_or_404(Lesson, id=lesson_id) if lesson_id else None

    # Calculate the total price for the selected slots
    total_price = lesson.price * len(selected_slots) if lesson else 0

    # Redirect to mock confirmation page
    return redirect(
        reverse('confirm_mock_payment') + f'?selected_slots={selected_slots_json}&total_price={total_price}')


from django.utils.timezone import make_aware
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@login_required
def confirm_mock_payment(request):
    # Get necessary data from the request
    selected_slots_json = request.GET.get('selected_slots')
    total_price = request.GET.get('total_price')

    # Parse selected_slots if it exists
    selected_slots = json.loads(selected_slots_json) if selected_slots_json else []

    # Ensure user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    formatted_slots = []  # List to store formatted slots

    # Loop through selected slots to create a booking for each
    for slot in selected_slots:
        lesson_id = slot.get('lessonId')
        start_time = slot.get('start')
        end_time = slot.get('end')

        # Convert the start and end time to readable format
        start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00")).astimezone(pytz.timezone("UTC"))
        end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00")).astimezone(pytz.timezone("UTC"))
        formatted_start = start_dt.strftime("%B %d, %Y, %I:%M %p")
        formatted_end = end_dt.strftime("%I:%M %p")

        # Append formatted date-time to list
        formatted_slots.append(f"{formatted_start} - {formatted_end}")

        # Fetch the lesson object
        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Find the corresponding Availability instance using teacher and date/time details
        availability = Availability.objects.filter(
            teacher=lesson.teacher,
            available_date=start_dt.date(),
            start_time=start_dt.time()
        ).first()

        if not availability:
            messages.error(request, f"No availability found for selected slot: {formatted_start} - {formatted_end}")
            return redirect('available_lessons')

        # Create and save the booking in the database with the availability instance
        booking = Booking.objects.create(
            student_name=request.user.get_full_name(),
            student_email=request.user.email,
            lesson=lesson,
            availability=availability,
            date=start_dt,
            status='Confirmed',
            user=request.user,
            suggested_date=timezone.now()
        )

    # Format the slots for the email content
    formatted_slots_str = "\n".join(formatted_slots)

    # Email content for user
    subject_user = "Your Booking Confirmation"
    message_user = f"Thank you for booking with us. Here are your booking details:\n\nSelected Slots:\n{formatted_slots_str}\n\nTotal Price: ${total_price}."

    # Email content for admin
    subject_admin = "New Booking Alert"
    message_admin = f"A new booking has been made.\n\nUser: {request.user.get_full_name()} ({request.user.email})\n\nSelected Slots:\n{formatted_slots_str}\n\nTotal Price: ${total_price}."

    # Send confirmation to the user
    send_mail(
        subject_user,
        message_user,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )

    # Send notification to the admin
    send_mail(
        subject_admin,
        message_admin,
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    # Redirect to success page after saving booking and sending emails
    return redirect('payment_success')




@login_required
def cancel_mock_payment(request):
    """Handles payment cancellation and redirects to a failure page."""
    return render(request, 'bookings/payment_failure.html')


@login_required
def payment_failure(request):
    return render(request, 'bookings/payment_failure.html')

@login_required
def payment_success(request):
    return render(request, 'bookings/payment_success.html', {
        'message': 'Payment Successful! Your lesson has been booked, and a confirmation email has been sent.'
    })

