# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

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
    
class Analysis(models.Model) :
    analysis = models.CharField(max_length=255)
    
    @classmethod
    def create(cls, analysis):
        data = cls(analysis=analysis)
        data.save()
        return data
    
class Data(models.Model):
    peds = models.IntegerField(default=39998)
    cams = models.IntegerField(default=40)
    mics = models.IntegerField(default=41)
    temps = models.IntegerField(default=20)
    
    @classmethod
    def create(cls, peds, cams, mics, temps, analysis):
        data = cls(peds=peds, cams=cams, mics=mics, temps=temps, analysis=analysis)
        data.save()
        return data
    

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    latitude = models.DecimalField(decimal_places=20, max_digits=50)
    longitude = models.DecimalField(decimal_places=20, max_digits=50)
    favorites = models.IntegerField(default=0)
    city = models.CharField(max_length=300)
    created = models.DateTimeField('date created')
    
    @classmethod
    def create(cls, title, desc, latitude, longitude, favorites, city):
        task = cls(title=title, description=desc, latitude=latitude, longitude=longitude, favorites=favorites, city=city, created=datetime.now())
        task.save()
        return task
    
    
class Comment(models.Model):
    # If I get around to it...
    created = models.DateTimeField('date created')