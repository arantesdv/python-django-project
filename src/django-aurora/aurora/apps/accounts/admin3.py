import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from aurora.apps.accounts.models import Patient, Doctor, Nurse, ConsanguineRelation
from aurora.apps.accounts.forms import UserRegisterForm, UserLoginForm
#RegisterForm, RegisterChangeForm
from django.forms import forms


class CsvImportForm(forms.Form):
	csv_file = forms.FileField()


class ExportCsvMixin:
	def export_as_csv(self, request, queryset):
		meta = self.model._meta
		field_names = [field.name for field in meta.fields]
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = f'attachment; filename={meta}.csv'
		writer = csv.writer(response)
		writer.writerow(field_names)
		for obj in queryset:
			row = writer.writerow([getattr(obj, field) for field in field_names])
		return response
	
	export_as_csv.short_description = "Export Selected"
	
	
class UserInline(admin.StackedInline):
	model = User
	fields = ('username', 'password1', 'password2')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin, ExportCsvMixin):
	fieldsets = (
		(None, {'fields': ('user','self_user','f_name', 'l_name')}),
		(None, {'fields': ('gender', 'bdate')}),
		(None, {'fields': ('address', 'city', 'state')}),
	)
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	date_hierarchy = 'bdate'
	# autocomplete_fields = ('user',)
	# raw_id_fields = ('user',)
	search_fields = ('user', '__str__')
	list_display = ('__str__', 'user', 'code', 'slug', 'bdate', 'get_age', 'gender', 'address', 'city', 'state', 'is_patient', 'is_doctor', 'is_nurse')
	list_display_links = ('__str__', 'user')
	actions = ['export_as_csv']
	#inlines = [UserInline]
	
	def has_delete_permission(self, request, obj=None):
		return True
	

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin, ExportCsvMixin):
	fieldsets = (
		(_("User"), {'fields': ('user','self_user','f_name', 'l_name')}),
		(None, {'fields': ('gender', 'bdate')}),
		(_("Address"), {'fields': ('address', 'city', 'state')}),
	)
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	list_display = ('__str__', 'user', 'code', 'slug', 'bdate', 'get_age', 'gender', 'address', 'city', 'state', 'is_patient', 'is_doctor', 'is_nurse')
	list_display_links = ('__str__', 'user')
	actions = ['export_as_csv']

	def has_delete_permission(self, request, obj=None):
		return True



@admin.register(ConsanguineRelation)
class ConsanguineRelationAdmin(admin.ModelAdmin, ExportCsvMixin):
	fieldsets = (
		(None, {'fields': ('patient', 'relative', 'relation', 'confidense')}),
	)
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	list_display = ('patient', 'relative', 'relation', 'confidense')
	list_display_links = ('patient',)
	actions = ['export_as_csv']

	def has_delete_permission(self, request, obj=None):
		return True