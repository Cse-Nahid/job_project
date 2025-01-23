from django.db import models
from accounts.models import CustomUser



# Create your models here.
class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Ensure CASCADE is set

    company_name = models.CharField(max_length=50)
    company_address = models.TextField()
    business_info = models.TextField()

    def __str__(self):
        return f'{self.company_name}'
    
    