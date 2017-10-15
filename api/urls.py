from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /api/Atlanta,GA/
    url(r'^city/(?P<city>.+)/$', views.get_city),
    url(r'^user/(?P<username>.+)/$', views.get_user),
    url(r'^tasks/generate/$', views.generate_tasks),
    url(r'^tasks/delete/$', views.delete_tasks),
    url(r'^tasks/$', views.get_tasks),
    url(r'^data/generate/$', views.analyze_iot),
    url(r'^data/$', views.get_data),
]