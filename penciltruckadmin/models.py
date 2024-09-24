from django.db import models
from django.utils import timezone

class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='volunteers/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image2 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image3 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image4 = models.ImageField(upload_to='gallery/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class VolunteerRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=100,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Volunteer Request from {self.name}"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    
class OtpInfo(models.Model):
    email = models.EmailField()
    email_otp = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    phone_otp = models.CharField(max_length=15)
    

    def __str__(self):
        return f"Volunteer Request from {self.email}"
