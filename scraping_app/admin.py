from django.contrib import admin
from .models import Company_Details

# Register your models here.

class Company_Details_Admin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'registered_address_town', 'url', 'revenue', 'registered_address_postcode', 'linkedin_url')
    search_fields = ('company_name', 'email', 'registered_address_town', 'url', 'company_summary', 'revenue', 'registered_address_postcode', 'linkedin_url', 'do_not_contact_status')
    list_per_page = 25


admin.site.register(Company_Details, Company_Details_Admin)