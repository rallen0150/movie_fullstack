"""movierater URL Configuration

These URLS are mainly for top level url paths, not for the custom API as the other urls.py is for
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^auth/', obtain_auth_token),
]
