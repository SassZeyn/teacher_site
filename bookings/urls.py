
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('available-lessons/', views.available_lessons, name='available_lessons'),
    path('contact/', views.contact, name='contact'),
    path('booking/<int:lesson_id>/', views.booking_form, name='booking_form'),
    path('payment/', views.payment_page, name='payment_page'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('api/availability-events/', views.get_availability_events, name='get_availability_events'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_lessons, name='category_lessons'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('materials/', views.materials, name='materials'),
    path('materials/<int:category_id>/', views.materials_by_category, name='materials_by_category'),
    path('youtube/', views.homepage_youtube, name='homepage_youtube'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('email-verification-pending/', views.email_verification_pending, name='email_verification_pending'),
    path('index/', views.index, name='index'),
    path('articles/', views.articles_view, name='articles'),  # Updated to articles_view
    path('payment/paypal/<int:lesson_id>/', views.create_paypal_payment, name='create_paypal_payment'),
    path('payment/paypal/return/', views.paypal_return, name='paypal_return'),
    path('payment/paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('payment/ameria/<int:lesson_id>/', views.create_ameria_payment, name='create_ameria_payment'),
    path('payment/ameria/return/', views.ameria_payment_return, name='ameria_payment_return'),
    path('payment/ameria/cancel/', views.ameria_payment_cancel, name='ameria_payment_cancel'),
    path('get-availability-events/', views.get_availability_events, name='get_availability_events'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),

    path('payment/mock/initiate/', views.initiate_mock_payment, name='initiate_mock_payment'),
    path('payment/mock/confirm/', views.confirm_mock_payment, name='confirm_mock_payment'),
    path('payment/mock/cancel/', views.cancel_mock_payment, name='cancel_mock_payment'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/success/', views.payment_success, name='payment_success'),


    # other paths



    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





