# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import random, decimal, json

from .models import *

# Create your views here.
def get_city(request, city):
    town = get_object_or_404(City, pk=city)
    return JsonResponse({'city': town.name, 'score': town.score})

def delete_tasks(request):
    Task.objects.all().delete()
    return JsonResponse({'success': True})

def get_tasks(request):
    return HttpResponse(serializers.serialize("json", Task.objects.all()))

def generate_tasks(request):
    titles = ['Clean street', 'Broken stop light', 'Garbage is everywhere', 'Solicitors are always here', 'Help with my garden', 'More parking spaces?', 'Stop sign is knocked down', 'IOT device is destroyed', 'Traffic busy in area today']
    descriptions = ["I've noticed that this has been a problem for a while; any tips?", "This task is also relevant to others in the area.", "Any help would be extremely appreciated!"]
    
    # Calculate random lat long points
    minLat = -84.4070885221
    minLong = 33.7336389505
    maxLat = -84.3700339754
    maxLong = 33.7758460904
    
    latRange = maxLat - minLat
    longRange = maxLong - minLong
    
    for i in range(500):
        lat = ((random.randrange(0, 1000) / 1000.0) * latRange) + minLat
        long = ((random.randrange(0, 1000) / 1000.0) * longRange) + minLong
        Task.create(random.choice(titles), random.choice(descriptions), lat, long, random.randrange(0,300,1), "Atlanta,GA")
        
    return JsonResponse({'success': True})
    

def get_user(request, username):
    user = get_object_or_404(User, pk=username)
    result = {}
    result['name'] = user.name
    result['username'] = user.username
    result['image'] = user.image
    result['score'] = user.score
    result['city'] = user.city
    result['created'] = user.created
    
    return JsonResponse(result)

def get_data(request):
    return HttpResponse(serializers.serialize("json", Data.objects.all()))

def analyze_iot(request):
    
    # First delete existing data
    Data.objects.all().delete();
    
    import requests, json, datetime

    import datetime
    def pretty_date(timestamp):
        print(
            datetime.datetime.fromtimestamp(
                timestamp
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

    url = "https://890407d7-e617-4d70-985f-01792d693387.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token"

    # First we auth
    print("Getting Authentication")
    querystring = {"grant_type":"client_credentials"}

    payload = "username=ic.admin&password=admin"
    headers = {
        'authorization': "Basic dWNzZC5kZXZlbG9wZXI6QHVjc2QuZGV2ZWxvcGVy",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()
    accessToken = response["access_token"]
    print("Got access token: " + accessToken[0:20] + "...")

    # Then we get all assets
    print("Getting All Assets")
    url = "https://ic-metadata-service.run.aws-usw02-pr.ice.predix.io/v2/metadata/assets/search"
    querystring = {"bbox":"33.754226:-84.396138,33.746551:-84.384996","page":"0","size":"200"}
    headers = {
        'authorization': "Bearer " + accessToken,
        'predix-zone-id': "SDSIM-IE-PARKING",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    content = response["content"]
    print("Found", len(content), "devices in Atlanta, GA")

    # Now we start constructing what we are looking for. First, we do per device, their location, description, and status?
    print("Starting to build analysis...")
    analysis = {}
    for entry in content:
        latlng = entry["coordinates"].split(":")
        name = entry["assetUid"]
        analysis[name] = {"desc": entry["assetType"], "lat": latlng[0], "lng": latlng[1], "types": entry["eventTypes"]}

    # So um why not make a heat map?
    print("Starting to grab heat and humidity information")
    startTime = 1500292800000
    endTime =   startTime + 43200000

    pretty_date(startTime / 1000.0)
    pretty_date(endTime / 1000.0)

    headers = {
        'authorization': "Bearer " + accessToken,
        'predix-zone-id': "SDSIM-IE-ENVIRONMENTAL",
        'cache-control': "no-cache"
        }

    tempCount = 0
    humCount = 0
    for asset in analysis:
        if "TEMPERATURE" in analysis[asset]["types"]:
            url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/assets/" + asset + "/events/"
            querystring = {"eventType":"TEMPERATURE","startTime": str(startTime),"endTime": str(endTime)}
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            if "content" in response:
                average = sum(x["measures"]["mean"] for x in response["content"]) / (1.0*len(response["content"]))
                analysis[asset]["temp"] = average
                tempCount += 1
        if "HUMIDITY" in analysis[asset]["types"]:
            url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/assets/" + asset + "/events/"
            querystring = {"eventType":"HUMIDITY","startTime": str(startTime),"endTime": str(endTime)}
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            if "content" in response:
                average = sum(x["measures"]["mean"] for x in response["content"]) / (1.0*len(response["content"]))
                analysis[asset]["humidity"] = average
                humCount += 1

    print("Got temperature data from", tempCount, "devices")
    print("Got humidity data from", humCount, "devices")

    # print("Now, let's try to get some images from these locations")
    # camTime = 1507766507000
    # pretty_date(camTime / 1000.0)
    # headers['predix-zone-id'] = "SDSIM-IE-PUBLIC-SAFETY"
    # camCount = 0
    # from IPython.display import Image
    # from IPython.core.display import HTML, display
    # for asset in assets:
    #     if "CAMERA" == analysis[asset]["desc"]:
    #         url = "https://ic-media-service.run.aws-usw02-pr.ice.predix.io/v2/mediastore/ondemand/assets/" + asset + "/media"
    #         querystring = {"mediaType":"IMAGE","timestamp": str(camTime)}
    #         response = requests.request("GET", url, headers=headers, params=querystring).json()
    #         response = requests.request("GET", response["pollUrl"], headers=headers).json()
    #         imageUrl = response["listOfEntries"]["content"][0]["url"]
    #         if imageUrl is not None:
    #             display(Image(url= imageUrl))
    #             print(imageUrl)

    print("Now we are going to try something a little tough; a vector map of pedestrian travel.")
    pedStart = 1500328704000
    pedEnd = 1500368704000
    pretty_date(pedStart / 1000.0)
    pretty_date(pedEnd / 1000.0)
    headers['predix-zone-id'] = "SDSIM-IE-PEDESTRIAN"
    pedEvents = []
    for asset in analysis:
        device = analysis[asset]
        if "PEDEVT" in device["types"]:
            url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/assets/" + asset + "/events"
            querystring = {"eventType":"PEDEVT","startTime":str(1500328704000),"endTime":str(1500368704000)}
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            for event in response["content"]:
                pedEvents.append({
                    "asset": asset,
                    "direction": event["measures"]["direction"],
                    "count": event["measures"]["pedestrianCount"],
                    "speed": event["measures"]["speed"]
                })

    print("Found", len(pedEvents), "pedestrian events!")

    print("We now have some interesting data. Let's begin putting it all together.")

    deviceCoverage = {}
    for asset in analysis:
        thing = analysis[asset]
        for device in thing["types"]:
            if device in deviceCoverage:
                deviceCoverage[device] += 1
            else:
                deviceCoverage[device] = 1

    for asset in analysis:
        thing = analysis[asset]
        if thing["desc"] in deviceCoverage:
            deviceCoverage[thing["desc"]] += 1
        else:
            deviceCoverage[thing["desc"]] = 1

    print(deviceCoverage)
    
    Data.create(deviceCoverage["PEDEVT"], deviceCoverage["CAMERA"], deviceCoverage["MIC"], deviceCoverage["TEMPERATURE"])
    Data.create(str(analysis))
    return JsonResponse({'success': True})
    
    
    
    