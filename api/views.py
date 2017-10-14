# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
    return JsonResponse(serializers.serialize("json", Task.objects.all()), safe=False)

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