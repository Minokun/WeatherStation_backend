from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^apiData/',views.apiData),
]

# urlpatterns = format_suffix_patterns(urlpatterns)