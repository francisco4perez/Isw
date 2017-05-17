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
from google import google


def fecha_a_datetime(fecha):
	lista = map(int,fecha.split("-"))
	return datetime(lista[0],lista[1],lista[2])

# ---------------------------------------------
@login_required(login_url="/")
def index(request):

	# Verificacion de usuario
	conected = 0
	es_admin = 0
	can_crud_contenidos = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("calendario.can_crud_contenidos"):
			can_crud_contenidos = 1

		if u_name == "ADMIN":
			es_admin = 1


		if request.GET.get('salir'):
			return logout_view(request)


	# Busqueda

	resultados=[]

	if request.method == "POST":

		busqueda = request.POST.get("search")
		resultados = google.search(busqueda,2)

		context = {'resultados' : resultados, 'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos, "es_admin":es_admin}
		return render(request, 'buscador/resultados.html',context)

    		
	context = {'lista' : resultados, 'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos, "es_admin":es_admin}

	return render(request, 'buscador/index.html',context)


def login_view(request):

	if request.user:
		logout(request)


	men = ""

	if request.method == "POST":

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect("/buscador/")

		else:
			men = "EL USUARIO Y PASSWORD INGRESADOS NO SON VALIDOS"

	context = {"men":men}
	return render(request, 'buscador/login.html',context)



def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")



def registro_view(request):

	men = ""

	nombres_instituciones = []
	instituciones = Institucion.objects.all()

	for ins in instituciones:
		nombres_instituciones.append(ins.nombre_institucion)


	# Verificacion de usuario
	conected = 0
	es_admin = 0
	can_crud_contenidos = 0
	u_name = ""

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("calendario.can_crud_contenidos"):
			can_crud_contenidos = 1

		if request.user.username == "ADMIN":
			es_admin = 1


		if request.GET.get('salir'):
			return logout_view(request)



	if request.method == "POST":

		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		institucion = request.POST['institucion']
		tipo_usuario = 1

		fecha_nacimiento = fecha_a_datetime(request.POST['fecha_nacimiento'])

		if es_admin:

			tipo_usuario = request.POST['tipo_usuario']

			if tipo_usuario == "Profesor":
				tipo_usuario = 0

		# Verificacion de informacion ingresada

		username_search = User.objects.filter(username = username)

		if len(username_search) == 0:

			if fecha_nacimiento < datetime.now():

				if institucion in nombres_instituciones:

					user = User.objects.create_user(username, email, password)
					user.save()

					up = UserProfile(user=user, institucion=institucion, tipo_usuario = tipo_usuario,fecha_nac=fecha_nacimiento.date())
					up.save()

					return HttpResponseRedirect("/buscador")

				else:
					men = "INSTITUCION INGRESADA INVALIDA"

			else:
				men = "FECHA INGRESADA INVALIDA"

		else:
			men = "NOMBRE DE USARIO YA EXISTENTE"

	context={'men' : men, 'instituciones' : instituciones, 'conected' : conected, "es_admin":es_admin, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos}

	return render(request, 'buscador/registro.html',context)



@login_required(login_url="/")
def resultados_view(request):

	# Verificacion de usuario
	conected = 0
	can_crud_contenidos = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("calendario.can_crud_contenidos"):
			can_crud_contenidos = 1


		if request.GET.get('salir'):
			return logout_view(request)



	context={'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos}

	return render(request, 'buscador/resultados.html',context)








'''




conected = 0
	can_inscribe_p = 0
	can_inscribe_g = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		up = UserProfile.objects.get(user = u)
		u_name = up.user_name

		if u.has_perm("calendario.can_inscribe_g"):
			can_inscribe_g = 1

		if u.has_perm("calendario.can_inscribe_p"):
			can_inscribe_p = 1


		
		if request.GET.get('btn'):
			return logout_view(request)















@login_required(login_url="/")
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
