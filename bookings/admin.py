

from django.contrib import admin
from django.utils.html import format_html

from .models import Teacher, Lesson, Booking, Category, Material, YouTubeVideo, Availability
from .models import ContactMessage
from .models import Events
from .models import UserProfile
from .models import Article

admin.site.register(ContactMessage)
admin.site.register(Events)
admin.site.register(UserProfile)

# Register the models
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'duration', 'price', 'status', 'category']
    list_filter = ['status', 'teacher', 'category']
    search_fields = ['title', 'teacher__name', 'category__name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    search_fields = ['title', 'category__name']
    list_filter = ['category']

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_email', 'lesson', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['student_name', 'student_email', 'lesson__title']



@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'available_date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['available_date', 'teacher']
    search_fields = ['teacher__name']

    # Custom method to check if a slot is booked
    def is_booked(self, obj):
        return Booking.objects.filter(availability=obj).exists()
    is_booked.boolean = True  # Displays a checkmark icon for True/False
    is_booked.short_description = 'Booked'  # Label for the column in the admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)

admin.site.register(Article, ArticleAdmin)

