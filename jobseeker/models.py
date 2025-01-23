from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator

# Create your models here.
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='jobseeker', unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    resume = models.FileField(upload_to='job_seekers/resumes/', null=True, blank=True)
    fathers_name = models.CharField(max_length=20)
    mothers_name = models.CharField(max_length=20)
    skills = models.TextField()
    address = models.TextField()
    contact_no = models.CharField(max_length=11, blank=True)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    age = models.IntegerField(validators=[MinValueValidator(18)])
    education = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
