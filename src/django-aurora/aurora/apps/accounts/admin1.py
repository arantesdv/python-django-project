from django.contrib import admin
from django.contrib.auth.admin import User

from .models import Patient
from django.db import models


class UserInline(admin.StackedInline):
	model = User
	
	
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	inlines = [UserInline]