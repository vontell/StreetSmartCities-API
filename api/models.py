# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=600)
    score = models.IntegerField(default=0)
    city = models.CharField(max_length=300)
    created = models.DateTimeField('date created')
    
class City(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    latitude = models.DecimalField(decimal_places=2, max_digits=50)
    longitude = models.DecimalField(decimal_places=2, max_digits=50)
    favorites = models.IntegerField(default=0)
    city = models.CharField(max_length=300)
    created = models.DateTimeField('date created')
    
class Comment(models.Model):
    # If I get around to it...
    created = models.DateTimeField('date created')