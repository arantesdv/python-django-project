from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from aurora.apps.accounts.models import Patient, Doctor, Nurse


class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
	
	def save(self, commit=True):
		user = super().save(commit=False)
		
		if commit:
			user.save()
		return user


class RegisterChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', ]
	
	def save(self, commit=True):
		user = super().save(commit=False)
		
		if commit:
			user.save()
		return user


class PatientForm(forms.ModelForm):
	class Meta:
		model = Patient
		fields = '__all__'
		
		def create(self, user):
			super().__init__()
			self.user = user
			return self
		
		def save(self, commit=True):
			patient = super().save(commit=False)
			
			if commit:
				patient.save()
			return patient


class DoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = '__all__'
		
		def save(self, commit=True):
			doctor = super().save(commit=False)
			
			if commit:
				doctor.save()
			return doctor


class NurseForm(forms.ModelForm):
	class Meta:
		model = Nurse
		fields = '__all__'
		
		def save(self, commit=True):
			nurse = super().save(commit=False)
			
			if commit:
				nurse.save()
			return nurse