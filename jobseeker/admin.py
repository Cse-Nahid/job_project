from django.contrib import admin
from .models import JobSeekerProfile

class JobSeekerProfileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    list_display = ['id', 'username', 'sex', 'age', 'education', 'experience', 'address', 'contact_no', 'get_email', 'get_user_type']

    def username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_user_type(self, obj):
        return obj.user.user_type

admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
