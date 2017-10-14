from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /api/Atlanta,GA/
    url(r'^city/(?P<city>.+)/$', views.get_city),
    url(r'^user/(?P<username>.+)/$', views.get_user)
]