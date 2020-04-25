from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('This user does not exist.')
			if not user.check_password(password):
				raise forms.ValidationError('Incorrect password.')
			if not user.is_active:
				raise forms.ValidationError('This user is not active.')
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label=_("Email Adress"))
	email2 = forms.EmailField(label=_("Confirm Email Adress"))
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password1',
			'password2',
		]
		
	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError('The email addresses do not match.')
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError('This email is already in use.')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError("Passwords do not match.")
		return super(UserRegisterForm, self).clean(*args, **kwargs)




