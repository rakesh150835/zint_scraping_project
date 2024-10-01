from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
import os

from .zint_scraping import scrape_data
from .models import Company_Details
from .cal_distance import cal_distance

# Create your views here.

def home(request):
    return render(request, 'scraping_app/home.html')


def scrape_data_view(request):
    #scrape_data()
    return render(request, 'scraping_app/scrape_data.html')

    

def get_data(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        distance = request.POST.get('distance')
        post_code = request.POST.get('post_code')
        # Remove any spaces from both end of the post code
        post_code = post_code.strip()

        companies = Company_Details.objects.all()

        for company in companies:
            calculated_distance = cal_distance(post_code, company.registered_address_postcode)
            if calculated_distance and calculated_distance <= int(distance):
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = f"{company_name}-Data-within-{distance}km"

                # Define the column headers
                headers = ['contact names', 'website addresses', 'e-mail addresses', 'business names']
                ws.append(headers)
                # Write data to the worksheet
                ws.append([company.company_name, company.url, company.email, company.company_name])

                # Set up the response to serve as an Excel file download
                filename = f"{ws.title}.xlsx"
                # Get the current working directory
                current_dir = os.getcwd()
                # Define the full path for the file
                file_path = os.path.join(current_dir, filename)

                # Save the workbook to the current working directory
                wb.save(file_path)

                return HttpResponse(f"Excel file saved at: {file_path}")
    
    
    return render(request, 'scraping_app/get_data.html')