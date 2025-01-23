# from django.db import models
# from django.conf import settings
# from jobs.models import Job


# class Application(models.Model):
#     # job_seeker = models.ForeignKey(
#     #     settings.AUTH_USER_MODEL, 
#     #     on_delete=models.CASCADE,
#     #     related_name='applications'
#     # )
#     # job = models.ForeignKey(
#     #     'jobs.Job',
#     #     on_delete=models.CASCADE,
#     #     related_name='applications'
#     # )
#     # resume = models.FileField(upload_to='resumes/')  # Ensure this field exists
#     # date_applied = models.DateField(auto_now_add=True)  # Ensure this field exists

#     # def __str__(self):
#     #     return f"{self.job_seeker} applied for {self.job}"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    date_applied = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(null=True, blank=True)  # Add this field if needed  
    def __str__(self):
        return f"{self.job} - {self.job_seeker}"
