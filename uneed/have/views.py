from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, loader
from twython import twython
from django.contrib.sessions.models import Session
from googlemaps import GoogleMaps
 
def checksession(request):
	return render_to_response('have/login.html')

def auth(request):
	api = twython.setup('Basic', request.POST['user'], request.POST['pass'])

	if (api):
		request.session['username'] = request.POST['user']
		request.session['password'] = request.POST['pass']
		return render_to_response('have/add.html')

	else:
		return render_to_response('have/login.html')
	
def tweet(request):
	api = twython.setup('Basic', request.session['username'], request.session['password'])
	gmaps = GoogleMaps()

	what = request.POST['what']
	where = request.POST['where']

	lat, lng = gmaps.address_to_latlng(where)
	tweet = "@U_Need :" + what + ":" + str(lat) + ':' + str(lng) + ":#ihave"

	api.updateStatus(tweet)

	return render_to_response('have/add.html')
 
