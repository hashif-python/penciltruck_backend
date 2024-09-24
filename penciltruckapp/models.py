from django.db import models
from django.utils import timezone

class StudyMaterialDonation(models.Model):
    STUDY_MATERIAL_CHOICES = [
        ('Books', 'Books'),
        ('Notebooks', 'Notebooks'),
        ('Stationery', 'Stationery'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
        ('Collected', 'Collected'),
    ]

    name = models.CharField(max_length=100)  # Donor's name
    study_material_type = models.CharField(max_length=50, choices=STUDY_MATERIAL_CHOICES)  # Study material type
    description = models.TextField()  # Description of the study material
    street_address = models.CharField(max_length=255)  # Pickup street address
    city = models.CharField(max_length=100)  # Pickup city
    state = models.CharField(max_length=100)  # Pickup state
    postal_code = models.CharField(max_length=20)  # Postal code
    country = models.CharField(max_length=100)  # Country
    mobile_no = models.CharField(max_length=15)  # Mobile number (up to 15 digits to handle international numbers)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Status of the donation
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-populates when the record is created

    def __str__(self):
        return f"{self.name} - {self.study_material_type} ({self.status})"
