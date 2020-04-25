from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
	context = {}
	return render(request, 'core/home.html', context)


def thanks(request):
	context = {}
	return render(request, 'core/thanks.html', context)