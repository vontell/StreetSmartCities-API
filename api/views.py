# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import *

# Create your views here.
def get_city(request, city):
    town = get_object_or_404(City, pk=city)
    return JsonResponse({'city': town.name, 'score': town.score})

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