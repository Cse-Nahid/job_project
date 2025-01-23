from django.contrib import admin
from .models import EmployerProfile

# Register your models here.
class EmployerAdmin(admin.ModelAdmin):
    def employer(self, obj):
        return obj.user.username
    
    def email(self, obj):
        return obj.user.email
    
    def user_type(self, obj):
        return obj.user.user_type
    
    list_display = ['id', 'employer', 'company_name', 'business_info', 'company_address', 'email', 'user_type']


admin.site.register(EmployerProfile, EmployerAdmin)