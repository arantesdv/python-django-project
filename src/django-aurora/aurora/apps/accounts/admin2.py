import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from aurora.apps.accounts.models import Patient, Doctor, Nurse
from aurora.apps.accounts.forms import RegisterForm, RegisterChangeForm
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


# PatientFormSet = inlineformset_factory(User, Patient, fields=('f_name', 'l_name'))
# patient = User.objects.get(username=username)
# formset = PatientFormSet(instance=patient)


# Register your models here.
# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
# 	actions_selection_counter = True
# 	empty_value_display = _("- empty -")
# 	model = Patient
# 	fieldsets = [
# 		(_("User"), {'fields': ('username', 'password1', 'password2')}),
# 		(_("Patient"), {'exclude': (None)}),
# 	]
#
# Define a new User admin


class UserAdmin(BaseUserAdmin):
	form = RegisterChangeForm
	add_form = RegisterForm


class UserInline(admin.StackedInline):
	model = User
	fields = ('username', 'password1', 'password2')


class PatientInline(admin.StackedInline):
	model = Patient
	fields = ('family', 'doctors')
	autocomplete_fields = ('family', 'doctors')


# can_delete = False


class DoctorInline(admin.StackedInline):
	model = Doctor


# can_delete = False


class NurseInline(admin.StackedInline):
	model = Nurse


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin, ExportCsvMixin):
	fields =  (('f_name', 'l_name'), ('gender', 'bdate'), ('address', 'city', 'state'), 'family', 'doctors')
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	date_hierarchy = 'bdate'
	# autocomplete_fields = ('user',)
	# raw_id_fields = ('user',)
	search_fields = ('user', '__str__')
	list_display = ('__str__', 'user', 'get_code', 'bdate', 'get_age', 'gender', 'address', 'city', 'state')
	list_display_links = ('__str__', 'user')
	actions = ['export_as_csv']
	
	def has_delete_permission(self, request, obj=None):
		return True


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin, ExportCsvMixin):
	fields = ('user', ('f_name', 'l_name'), ('gender', 'bdate'), ('address', 'city', 'state'), 'patients')
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	date_hierarchy = 'bdate'
	# autocomplete_fields = ('user',)
	# raw_id_fields = ('user',)
	search_fields = ('user', '__str__')
	list_display = ('__str__', 'bdate', 'get_age')
	list_display_links = ('__str__',)
	actions = ['export_as_csv']
	
	def has_delete_permission(self, request, obj=None):
		return True


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin, ExportCsvMixin):
	fields = ('user', ('f_name', 'l_name'), ('gender', 'bdate'), ('address', 'city', 'state'))
	actions_on_top = False
	actions_on_bottom = True
	actions_selection_counter = True
	date_hierarchy = 'bdate'
	# autocomplete_fields = ('user',)
	# raw_id_fields = ('user',)
	search_fields = ('user', '__str__')
	list_display = ('__str__', 'bdate', 'get_age', 'gender', 'address', 'city', 'state')
	list_display_links = ('__str__',)
	actions = ['export_as_csv']
	
	def has_delete_permission(self, request, obj=None):
		return True


admin.site.unregister(User)
#admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

