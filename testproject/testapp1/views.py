import logging
from django.shortcuts import render
from django.http import HttpResponse
#from common.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
import requests
from requests.auth import HTTPBasicAuth
from testproject.testapp1.configfile import *
from django.core.cache import cache
from django_redis import get_redis_connection
import json
app_logger = logging.getLogger('app')
app_stats_logger = logging.getLogger('app_stats')
#from settings import API_DOMAIN, API_PWD, API_USER
from .forms import NameForm
# con = get_redis_connection("default")
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
    cache_key = 'get_city_list'
#     data = con.get(cache_key)
    if not False:
        app_logger.info("didn't find data in redis")
        obj = api_call_method('city_list')
        if not obj.status_code == 200:
            return HttpResponse("Failed getting data")
        data = obj.json()
        data = data.get('data')
#         con.set(cache_key, json.dumps(data), timeout=60*60*5)
    else:
        data = json.loads(data)
#         app_logger.info('found data in redis: %s' %data)
    template = loader.get_template('city_list_page.html')
#     app_logger.info(data)
    data = {x:data.get(x) for x in data if data.get(x).get('country_code', '')=='IN'}
    context = {'city_data': data}
    return HttpResponse(template.render(context,request))
    #return HttpResponse(json.dumps(obj.json()))
