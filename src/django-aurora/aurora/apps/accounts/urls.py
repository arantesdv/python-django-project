from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from .views import (
	login_view,
	register_view,
	logout_view,
)

app_name = 'accounts'

urlpatterns = (
    path('login/',login_view, name='login'),
    path('signup/', register_view, name='signup'),
    path('logout/', logout_view, name='logout'),
)
