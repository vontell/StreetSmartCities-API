# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(City)
admin.site.register(Task)
admin.site.register(Data)
admin.site.register(Analysis)