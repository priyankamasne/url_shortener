from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from mainApp.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def index(request):
    c = {}
    # to enable CSRF protection
    c.update(csrf(request))
    return render_to_response('mainApp/index.html', c)
 
def redirect_short_url(request, short_url):
    '''
    Given a short_url, this method redirects the request 
    to originallong URL

    '''
    # get object, if not found return 404 error
    url = get_object_or_404(Urls, pk=short_url) 
    return HttpResponseRedirect(url.httpurl)
 
def validate_url(url):
    '''
    Method for validating a long URL
    
    '''
    val = URLValidator()
    try:
        val(url)
    except ValidationError, e:
        raise e

def shorten_url(request):
    '''
    Given a long URL, this method 
    1) calls get_shorturl_hash method to generate a new hash
    2) saves the new hash_key and long_url to db
    3) returns an HTTP response 

    '''
    url = request.POST.get("url", '')
    try :
        validate_url(url)
        if not (url == ''):
            short_id = get_shorturl_hash()
            b = Urls(httpurl=url, short_id=short_id)
            b.save()
     
            response_data = {}
            response_data['url'] = settings.SITE_URL + "/" + short_id
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponse(json.dumps({"error": "error occurs"}),
                 content_type="application/json")
    except Exception as e:
        print e;
        return HttpResponse(json.dumps({"error": str(e)}), content_type="application/json")
 
def get_shorturl_hash():
    '''
    This method
    1) generates a 8 character long hask key
    2) checks if hash has already been assigned
    3) return the hash key 

    '''
    length = 8
    char_list = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        hash_key = ''.join(random.choice(char_list) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return hash_key