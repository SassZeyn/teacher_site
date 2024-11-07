
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    lesson_description = models.TextField(blank=True)  # Description for lesson categories
    material_description = models.TextField(blank=True)  # Description for material categories

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in minutes
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')  # Linked to teacher

    def __str__(self):
        return self.title


class Booking(models.Model):
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)  # Booking date
    status = models.CharField(max_length=20, choices=(('Confirmed', 'Confirmed'), ('Pending', 'Pending')))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_date = models.DateTimeField(null=True, blank=True)  # If students suggest alternative dates
    calendly_event_url = models.URLField(max_length=500, blank=True, null=True)  # Store Calendly event URL
    availability = models.OneToOneField("Availability", on_delete=models.CASCADE)  # String reference to avoid circular import

    def __str__(self):
        return f"{self.student_name} - {self.lesson.title}"




class Material(models.Model):
    category = models.ForeignKey(Category, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    thumbnail_image = models.ImageField(upload_to='youtube_thumbnails/')

    def __str__(self):
        return self.title

    def get_video_id(self):
        """Extracts the video ID from YouTube URL for embedding."""
        if "v=" in self.video_url:
            return self.video_url.split("v=")[1]
        elif "youtu.be" in self.video_url:
            return self.video_url.split("/")[-1]
        return None


class Availability(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    available_date = models.DateField()  # Date of availability
    start_time = models.TimeField()  # Starting time of availability
    end_time = models.TimeField()  # Ending time of availability
    calendly_event_url = models.URLField(max_length=500, blank=True, null=True)  # Store Calendly event URL

    def __str__(self):
        return f"Availability for {self.teacher.name} on {self.available_date} from {self.start_time} to {self.end_time}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"



class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table ="tblevents"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=200)
    introduction = models.TextField(blank=True, null=True)
    content = models.TextField()
    conclusion = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)  # Add this field

    def __str__(self):
        return self.title

