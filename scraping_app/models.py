from django.db import models

# Create your models here.
# Company Name
# Email
# Registered Address Town
# URL
# Company Summary
# Revenue
# Is Direct Linkedin URL?
# Registered Address Postcode
# LinkedIn URL
# DO NOT CONTACT Status

# ['', 'BRAY LEINO LIMITED', 'hello@brayleino.co.uk', 'Barnstaple', 'https://www.brayleino.co.uk/', 'Bray Leino is an award-winning integrated Agency. We use our creativenergy to drive growth for Clients by going beyond and finding better ways to answer their challenges.', '£26.0m', '', 'EX32 0RN', 'https://www.linkedin.com/in/chris-harris-62702181/', '']

class Company_Details(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    registered_address_town = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    company_summary = models.TextField(null=True, blank=True)
    revenue = models.CharField(max_length=15, null=True, blank=True)
    registered_address_postcode = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    do_not_contact_status = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
