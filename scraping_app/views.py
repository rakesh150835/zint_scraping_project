from django.shortcuts import render, redirect
import openpyxl
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import FileResponse

from .zint_scraping import scrape_data
from .models import Company_Details
from .cal_distance import cal_distance

# Create your views here.

def home(request):
    return render(request, 'scraping_app/home.html')


def scrape_data_view(request):
    #scrape_data()
    return render(request, 'scraping_app/home.html')

    
# get data from the database and save it to an excel file
def get_data(request):
    try:
        if request.method == 'POST':
            company_name = request.POST.get('company_name')
            distance = request.POST.get('distance')
            post_code = request.POST.get('post_code')
            # Remove any spaces from both end of the post code
            post_code = post_code.strip()
            # initialize the worksheet
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = f"{company_name}-Data-within-{distance}km"
            # Define the column headers
            headers = ['contact names', 'website addresses', 'e-mail addresses', 'business names']
            ws.append(headers)

            companies = Company_Details.objects.all()

            for company in companies:
                calculated_distance = cal_distance(post_code, company.registered_address_postcode)
                if calculated_distance and calculated_distance <= int(distance):
                    # Write data to the worksheet
                    ws.append([company.company_name, company.url, company.email, company.company_name])

            # Set up the response to serve as an Excel file download
            filename = f"{ws.title}.xlsx"
            # Get the file path in the media directory
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            # Save the file to the media directory
            wb.save(file_path)

            return redirect('download_page', filename=filename)
        
        return render(request, 'scraping_app/home.html')
    
    except Exception as e:
        return render(request, 'scraping_app/home.html', {'error': "An error occurred!"})
    




def download_page(request, filename):
    try:
        file_url = f"{settings.MEDIA_URL}{filename}"
            
        context = {
            'file_url': file_url,
            'filename': filename
        }
            
        return render(request, 'scraping_app/download_page.html', context)
    
    except Exception as e:
        return render(request, 'scraping_app/home.html', {'error': "An error occurred, please try again!"})


def download_file(request, filename):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Delete the file after serving it
            os.remove(file_path)
            
            return response
        else:
            raise Http404("File does not exist")
        
    except Exception as e:
        return render(request, 'scraping_app/home.html', {'error': "An error occurred, please try again!"})


def cancel_download(request, filename):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return redirect('home')
    
    except Exception as e:
        return render(request, 'scraping_app/home.html', {'error': "An error occurred, please try again!"})

