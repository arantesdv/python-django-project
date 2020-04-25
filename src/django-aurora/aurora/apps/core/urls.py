from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from .views import (
	home,
	thanks,
)

app_name = 'core'

urlpatterns = (
	path('', home, name='home'),
	path('thank-you/', thanks, name='thanks'),

)
