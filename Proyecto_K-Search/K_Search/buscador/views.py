# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from buscador.models import *
from django.contrib.auth.models import User #// Sistema de usuarios proporcionado por Django
from django.shortcuts import get_object_or_404, render, redirect #// Tribial de django
from django.http import HttpResponseRedirect, HttpResponse #// En caso de no querer hacer render
from django.core.urlresolvers import reverse
from datetime import datetime, date #// Para manejo de fechas
from django.contrib.auth import authenticate, login, logout #// Para autentificar los usuarios
from django.contrib.auth.decorators import login_required #// Para poner antes de las views y requerir login
from google import search,get_page



def main_view(request):

	lista_urls=[]

	if request.method == "POST":
		# Ejemplos sacando valores del formulario (de cada input)
		busqueda = request.POST.get("search")
		for elem in search(str(busqueda), stop=20):
			lista_urls.append(elem)
		context = {'lista_urls' : lista_urls}
		return render(request, 'buscador/resultados.html',context)
    		

	context = {'lista' : lista_urls}

	return render(request, 'buscador/index.html',context)
def resultados_view(request):
	request['lista']
	context={}
	return render(request, 'buscador/resultados.html',context)

'''@login_required(login_url="/")
def add_to_calendar(request, sel_g=None):

	# Variables varias
	post = 0
	conected = 0
	can_inscribe_p = 0
	can_inscribe_g = 0
	valid_date = 0

	# Autentificacion de permisos

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		up = UserProfile.objects.get(user = u)
		u_name = up.user_name
		country = up.country

		if u.has_perm("calendario.can_inscribe_g"):
			can_inscribe_g = 1

		if u.has_perm("calendario.can_inscribe_p"):
			can_inscribe_p = 1

		if request.GET.get('btn'):
			return logout_view(request)


	if not can_inscribe_g and u_name != "ADMIN":
		get_object_or_404(Calendar, pk=-1)


	# Si se utiliza el metodo POST en esta ruta

	if request.method == "POST":

		# Ejemplos sacando valores del formulario (de cada input)
		bol = request.POST.get("bol")
		sel_grade = request.POST.get("sel_cal")
		cal_name = request.POST.get("cal_name")
		programation_status = request.POST.get("programation_status")
		ejecution_status = request.POST.get("ejecution_status")

	# Hacer cosas con los valores Y...

	# Retornar resultados en el context
	context = {'grade_list' : grade_list, 'provider_list' : provider_list, 'ceco_list' : ceco_list,'conected' : conected, 'u_name' : u_name, 'country' : country, 'post' : post, 'ceco_s' : ceco_s,'c' : c, 'men' : men, 'sel_g' : sel_g}
	
	return render(request, 'calendario/add_to_calendar.html',context)
'''
