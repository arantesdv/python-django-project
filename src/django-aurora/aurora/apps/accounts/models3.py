import uuid
import datetime
from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from aurora.apps.core.models import CreationModificationDateBase, MetaTagsBase, UrlBase
from django.db.models.signals import post_save


GENDER_OPTIONS = (
	('O', 'Nenhum/Outro'),
	('M', 'Masculino'),
	('F', 'Feminino'),
)

BRAZILIAN_STATES = (
	('DF', 'Distrito Federal'),
	('AC', 'Acre'),
	('AL', 'Alagoas'),
	('AP', 'Amapá'),
	('AM', 'Amazonas'),
	('BA', 'Bahia'),
	('CE', 'Ceará'),
	('ES', 'Espírito Santo'),
	('GO', 'Goiás'),
	('MA', 'Maranhão'),
	('MT', 'Mato Grosso'),
	('MS', 'Mato Grosso do Sul'),
	('MG', 'Minas Gerais'),
	('PA', 'Pará'),
	('PB', 'Paraíba'),
	('PR', 'Paraná'),
	('PE', 'Pernambuco'),
	('PI', 'Piauí'),
	('RJ', 'Rio de Janeiro'),
	('RN', 'Rio Grande do Norte'),
	('RS', 'Rio Grande do Sul'),
	('RO', 'Rondônia'),
	('RR', 'Roraima'),
	('SC', 'Santa Catarina'),
	('SP', 'São Paulo'),
	('SE', 'Sergipe'),
	('TO', 'Tocantins'),
)

FAMILY_OPTIONS = (
	(1, _('Mother')),
	(2, _('Father')),
	(3, _('Sibling')),
	(4, _('Offspring')),
	(5, _('Second degree relatives')),
)

CONFIDENCE_OPTIONS = (
	(1, 'Mínima'),
	(2, 'Baixa'),
	(3, 'Moderada'),
	(4, 'Elevada'),
	(5, 'Máxima'),
)
		

class Profile(CreationModificationDateBase, MetaTagsBase, UrlBase):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
	self_user = models.BooleanField(default=True, verbose_name=_("Self user"))
	f_name = models.CharField(max_length=50, verbose_name=_("First name"))
	l_name = models.CharField(max_length=50, verbose_name=_("Last name"))
	bdate = models.DateField(default=date(1978,9,7), verbose_name=_("Birth date"))
	gender = models.CharField(max_length=1, choices=GENDER_OPTIONS, default='M', verbose_name=_("Gender"))
	email = models.EmailField(default='arantesdv@me.com')
	phone = models.CharField(max_length=20, default='+5562', verbose_name=_("Phone number"))
	address = models.CharField(max_length=200, default='Rua Rodrigues Tomaz 95 Jundiaí', verbose_name=_("Address"))
	city = models.CharField(max_length=100, default='Anápolis', verbose_name=_("City"))
	state = models.CharField(max_length=2, choices=BRAZILIAN_STATES, default='GO', verbose_name=_("State"))
	slug = models.SlugField(blank=True, default=None, null=True)
	code = models.CharField(max_length=12, blank=True, default="")
	is_patient = models.BooleanField(default=False, editable=False, verbose_name=_("Is patient"))
	is_doctor = models.BooleanField(default=False, editable=False, verbose_name=_("Is doctor"))
	is_nurse = models.BooleanField(default=False, editable=False, verbose_name=_("Is nurse"))


	# def __init__(self, user, *args, **kwargs):
	# 	self.user = user
	# 	super().__init__(*args, **kwargs)

	
	class Meta:
		abstract = True
		constraints = [models.UniqueConstraint(fields=['f_name','l_name', 'bdate', 'gender'], name='unique_profile')]
		verbose_name = _("Profile")
		verbose_name_plural = _("Profile")
	
	def __str__(self):
		return '%s %s' % (self.f_name, self.l_name)
	
	def get_age(self):
		year = timedelta(days=365)
		today = date.today()
		years = (today - self.bdate) / year
		if years < 1:
			residual = ((today - self.bdate) / year) - int(years)
			months = residual * 12
			age = '%i meses' % months
		elif years == 1:
			age = '%i ano' % years
		elif years > 1:
			age = '%i anos' % years
		return '%s' % age
	
	def full_name(self):
		return '%s %s' % (self.f_name, self.l_name)
	
	def short_name(self):
		return self.f_name
	
	def composed_name(self):
		return '%s %s' % (self.f_name.split()[0],  self.l_name.split()[-1])
	
	def get_code(self):
		initial_1 = self.f_name.split()[0][0]
		initial_2 = self.l_name.split()[-1][0]
		number = self.bdate.strftime("%Y%m%d")
		code = str(number) + initial_1 + initial_2
		return code
	
	def get_slug_name(self):
		string = self.full_name()
		slug = slugify(string)
		return slug
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.full_name())
		self.code = self.get_code()
		super().save(*args, **kwargs)


class Patient(Profile):
	patient_status = models.BooleanField(default=True, verbose_name=_("Is active"))
	#family = models.ManyToManyField('Patient', blank=True, related_name='patient_family')
	doctors = models.ManyToManyField('Doctor', blank=True, related_name='patient_doctors', name='doctors')
	
	class Meta:
		verbose_name = _("Patient")
		verbose_name_plural = _("Patients")
		
	#
	# def save(self, *args, **kwargs):
	# 	self.slug = self.get_slug_name()
	# 	self.code = self.get_code()
	# 	user = User.objects.get(username__icontains=self.slug)
	# 	if not user:
	# 		user = User.objects.create(username=self.slug, first_name=self.f_name, last_name=self.l_name)
	# 		user.set_password(f'{self.code}')
	# 		user.save()
	# 	self.user = user
	# 	super().save(*args, **kwargs)
	
	# def save(self, *args, **kwargs):
	# 	slug = self.get_slug_name()
	# 	code = self.get_code()
	# 	user = User.objects.get(patient_user=self.id)
	# 	self.user['username'] = slug
	# 	self.user['first_name'] = self.f_name
	# 	self.user['last_name'] = self.l_name
	# 	self.user = user
	# 	self.code = code
	# 	self.slug = slug
	# 	super().save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.full_name())
		self.code = self.get_code()
		self.is_patient = True
		super().save(*args, **kwargs)


class Doctor(Profile):
	doctor_status = models.BooleanField(default=True, verbose_name=_("Is active"))
	patients = models.ManyToManyField('Patient', blank=True, related_name='doctor_patients')
	
	class Meta:
		verbose_name = _("Doctor")
		verbose_name_plural = _("Doctors")
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.full_name())
		self.code = self.get_code()
		self.is_doctor = True
		super().save(*args, **kwargs)


class Nurse(Profile):
	nurse_status = models.BooleanField(default=True, verbose_name=_("Is active"))
	patients = models.ManyToManyField('Patient', blank=True, related_name='nurse_patients')
	
	class Meta(Profile.Meta):
		verbose_name = _("Nurse")
		verbose_name_plural = _("Nurses")
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.full_name())
		self.code = self.get_code()
		self.is_nurse = True
		super().save(*args, **kwargs)
		
		
class ConsanguineRelation(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='relater_patient')
	relative = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_relative')
	relation = models.PositiveSmallIntegerField(choices=FAMILY_OPTIONS)
	confidense = models.PositiveSmallIntegerField(choices=CONFIDENCE_OPTIONS)
	
	class Meta:
		verbose_name = _('Consanguine Relation')
		verbose_name_plural = _('Consanguine Relations')
		constraints = [models.UniqueConstraint(fields=['patient', 'relative'], name='unique_patient_relative')]
		
	def __str__(self):
		for key, value in FAMILY_OPTIONS:
			if self.relation == key:
				relationship = value
		return '%s (%s)' % (self.relative.short_name(), relationship)

