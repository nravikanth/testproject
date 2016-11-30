import logging
from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from testproject.testapp1.configfile import *
app_logger = logging.getLogger('app')
app_stats_logger = logging.getLogger('app_stats')
#from settings import API_DOMAIN, API_PWD, API_USER
from .forms import NameForm

API_URLS = {
    'city_list' : API_DOMAIN + 'get_city_list'
}
# Create your views here.
def get_name(request):
    app_logger.debug("came to get_name")
    app_stats_logger.info('stats logs')
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse(request.POST.get('your_name', 'Done'))
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})

def api_call_method(url_path, method='GET'):
    if method == 'GET':
        return requests.get(API_URLS.get(url_path), auth=HTTPBasicAuth(API_USER, API_PWD))
    else:
        pass

def get_data(request):
    #import pdb;pdb.set_trace()
    obj = api_call_method('city_list')
    if not obj.status_code == 200:
        return HttpResponse("Failed getting data")
    return HttpResponse(obj.json())
