from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


# change admin header, title and index_title
admin.site.site_header = "Aurora Admin"
admin.site.site_title = "Aurora Admin Portal"
admin.site.index_title = "Welcome to Aurora Researcher Portal"

urlpatterns = i18n_patterns(
    path('core/', include('aurora.apps.core.urls')),
    path('accounts/', include('aurora.apps.accounts.urls')),
    path('admin/', admin.site.urls, name='admin'),
)
