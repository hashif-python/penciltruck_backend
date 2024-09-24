from re import A
from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Gallery)
admin.site.register(Volunteer)
admin.site.register(Banner)
admin.site.register(VolunteerRequest)
admin.site.register(NewsletterSubscription)
admin.site.register(OtpInfo)
