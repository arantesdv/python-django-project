import uuid
from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from aurora.apps.core.models import CreationModificationDateBase, MetaTagsBase

GENDER_OPTIONS = (
	('N', 'Nenhuma resposta'),
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

RELATIONSHIP_OPTIONS = (
	(1, 'Outro'),
	(2, 'Amizade'),
	(3, 'Familiar/Segundo Grau'),
	(4, 'Familiar/Conjugal'),
	(5, 'Familiar/Primeiro grau'),
)

CONFIDENCE_OPTIONS = (
	(1, 'Mínima'),
	(2, 'Baixa'),
	(3, 'Moderada'),
	(4, 'Elevada'),
	(5, 'Máxima'),
)


class Profile(CreationModificationDateBase, MetaTagsBase):
	f_name = models.CharField(max_length=50, verbose_name=_("First name"))
	l_name = models.CharField(max_length=50, verbose_name=_("Last name"))
	bdate = models.DateField(default='1978-09-07', verbose_name=_("Birth date"))
	gender = models.CharField(max_length=1, choices=GENDER_OPTIONS, default='M', verbose_name=_("Gender"))
	email = models.EmailField(default='arantesdv@me.com')
	phone = models.CharField(max_length=20, default='+5562', verbose_name=_("Phone number"))
	address = models.CharField(max_length=200, default='Rua Rodrigues Tomaz 95 Jundiaí', verbose_name=_("Address"))
	city = models.CharField(max_length=100, default='Anápolis', verbose_name=_("City"))
	state = models.CharField(max_length=2, choices=BRAZILIAN_STATES, default='GO', verbose_name=_("State"))
	slug = models.SlugField(default="")
	
	class Meta:
		abstract = True
		constraints = [models.UniqueConstraint(fields=['f_name', 'l_name', 'bdate', 'gender'],
		                                       name='unique_person_%(class)s')]
		verbose_name = _("Person")
		verbose_name_plural = _("People")
	
	def __str__(self):
		return '%s %s' % (self.f_name, self.l_name)
	
	def get_age(self):
		year = timedelta(days=365)
		today = date.today()
		years = int((today - self.bdate) / year)
		months = ((today - self.bdate) / year) - years
		if years >= 2:
			years_age = '%i anos' % years
		elif years >= 1:
			years_age = '%i ano' % years
		else:
			years_age = ''
		if months >= 2:
			months_age = '%i meses' % months
		elif months >= 1:
			months_age = '%i meses' % months
		else:
			months_age = ''
		
		return '%s %s' % (years_age, months_age)
	
	def full_name(self):
		return '%s %s' % (self.f_name, self.l_name)
	
	def short_name(self):
		return self.f_name
	
	def get_code(self):
		initial_1 = self.f_name.split()
		initial_1 = initial_1[0][0]
		initial_2 = self.l_name.split()
		initial_2 = initial_2[-1][0]
		number = self.bdate.strftime("%Y%m%d")
		code = str(number) + initial_1 + initial_2
		return code


class Patient(Profile):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Patient user"), primary_key=True)
	is_patient = models.BooleanField(default=True, editable=False, verbose_name=_("Is patient"))
	is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
	relatives = models.ManyToManyField('Patient', blank=True, related_name='patient_relatives')
	doctors = models.ManyToManyField('Doctor', blank=True, related_name='patient_doctors')
	code = models.CharField(max_length=12, blank=True, default="")
	
	class Meta(Profile.Meta):
		verbose_name = _("Patient")
		verbose_name_plural = _("Patients")
		
	def save(self, *args, **kwargs):
		code = str(self.bdate.strftime("%Y%m%d").replace("-", "")) + self.f_name.split()[0][0] + self.l_name.split()[-1][0] + self.gender[0]
		self.code = code
		self.slug = slugify(self.full_name())
		self.user = User.objects.create(username=self.code, first_name=self.f_name, last_name=self.l_name, email=self.email)
		super().save(*args, **kwargs)
		


class Doctor(Profile):
	user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, verbose_name=_("Doctor user"))
	is_doctor = models.BooleanField(default=True, editable=False, verbose_name=_("Is doctor"))
	is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
	patients = models.ManyToManyField('Patient', blank=True, related_name='doctor_patients')
	
	class Meta(Profile.Meta):
		verbose_name = _("Doctor")
		verbose_name_plural = _("Doctors")
		
	def save(self,  *args, **kwargs):
		self.slug = slugify(self.full_name())
		super().save(*args, **kwargs)

class Nurse(Profile):
	user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, verbose_name=_("Nurse user"))
	is_nurse = models.BooleanField(default=True, editable=False, verbose_name=_("Is nurse"))
	is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
	patients = models.ManyToManyField('Patient', blank=True, related_name='nurse_patients')
	
	class Meta(Profile.Meta):
		verbose_name = _("Nurse")
		verbose_name_plural = _("Nurses")
		
	def save(self,  *args, **kwargs):
		self.slug = slugify(self.full_name())
		super().save(*args, **kwargs)