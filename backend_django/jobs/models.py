from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255, default="Unknown")
    link = models.URLField(blank=True, null=True, default="https://remoteok.com/")  # 👈 not "url"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    text = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"
    


class UserJobView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.job.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
