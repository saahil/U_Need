from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from twython import twython
from googlemaps import GoogleMaps
from django.contrib.sessions.models import Session

def in_vic(lat1, lng1, lat2, lng2):
	if (abs(lat1-lat2) <= 5) and (abs(lng1-lng2) <= 5):
		return 1
	else:
		return 0

def enter(request):
	return render_to_response('need/enter.html')

def lookup(request):
	what = (request.POST['what']).lower()
	where = (request.POST['where']).lower()

	api = twython.setup('Basic', username='U_Need', password='')
	gmaps = GoogleMaps()

	mentions = api.getUserMentions(since_id=4698625520)

	a = []

	lat1, lng1 = gmaps.address_to_latlng(where)

	#if is not (api):
	#	render_to_response('need/enter.html')

	for stat in mentions:
		text = (stat["text"]).lower()
		ele = text.split(':')
		lat2 = float(ele[2])
		lng2 = float(ele[3])
		if (text.find(what) != -1) and (in_vic(lat1, lng1, lat2, lng2) == 1):
			actual = gmaps.latlng_to_address(lat2, lng2)
			tweet = ele[1] + " " + actual
			a.append(tweet)

	t = loader.get_template("need/results.html")

	c = Context({'stat': a},)
	return HttpResponse(t.render(c))

	
