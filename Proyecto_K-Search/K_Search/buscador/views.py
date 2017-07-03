# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import html2text
import numpy as np
import urllib
import sys
import re
import urlparse
import urllib2

from bs4 import BeautifulSoup
from django.shortcuts import render
from buscador.models import *
from django.contrib.auth.models import User, Group, Permission #// Sistema de usuarios proporcionado por Django
from django.shortcuts import get_object_or_404, render, redirect #// Tribial de django
from django.http import HttpResponseRedirect, HttpResponse #// En caso de no querer hacer render
from django.core.urlresolvers import reverse
from datetime import datetime, date #// Para manejo de fechas
from django.contrib.auth import authenticate, login, logout #// Para autentificar los usuarios
from django.contrib.auth.decorators import login_required #// Para poner antes de las views y requerir login
from google import google

reload(sys)  
sys.setdefaultencoding('utf8')
# -----------------------------------------------------------
# Objeto contenido, definido para ser mas practico en el template
class contenido(object):
	def __init__(self, text,index):
		super(contenido, self).__init__()
		self.text = text
		self.index = index

# Objeto Informacion, que contiene la informacion (contenidos e imagenes) de una url
class Informacion(object):
	def __init__(self, contenidos,imagenes,index):
		super(Informacion, self).__init__()
		self.contenidos = contenidos
		self.imagenes = imagenes
		self.index = index


class Pagina_Rating(object):
	def __init__(self, pagina,rating):
		super(Pagina_Rating, self).__init__()
		self.pagina = pagina
		self.rating = rating

		


# Funcion que retorna true o false si la seccion ingresada es una lista muy larga
def lista_larga(seccion):
	return len(seccion.split(" * ")) > 7

# Funcion que verifica si la url corresponde a una pagina que realmente existe
def existe_pagina(url):
	if url[:4] != "http":
		url = "http://"+url
	try:
	    urllib2.urlopen(url)
	    return True
	except Exception as e:
	    return False


# Funcion que extrae contenidos relevantes (solo texto) dada una url
def contenidos_relevantes(url):
	html = urllib.urlopen(url).read()
	h = html2text.HTML2Text()
	h.ignore_links = True

	try:
		html_text = h.handle(html)
	except UnicodeDecodeError, e:
		reload(sys)
		sys.setdefaultencoding('latin-1')
		html_text = h.handle(html)

	secciones = html_text.split("#")
	num_secciones = len(secciones)

	largos = []
	for secc in secciones:
		largos.append(len(secc))

	contenido_relevantes = []
	con = 0
	prom = np.mean(largos)
	for l in largos:
		if (l > prom*0.8):
			seccion = secciones[con]
			if not lista_larga(seccion):
				contenido_relevantes.append(seccion)
		con+=1

	return contenido_relevantes


# Funcion que extrae los links de imagen de una url
def extraer_links_imagenes(url):
	con = 0
	links = []
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)
	imgs = soup.findAll('img',{"src":True})

	res = urlparse.urlparse(url)
	url_base = res.netloc
	
	LIMITE = 10

	for img in imgs:
		if(con <= LIMITE):
			src = img["src"]

			if len(src) != 0:

				if src[0] == "/" and src[:2] != "//":
					if len(url_base) > 0:
						src = "http://"+url_base+src

				elif url[-4:] == ".php" or url[-5:] == ".html":

					if(len(urlparse.urlparse(src).netloc) == 0):
						path = res.path
						src = "http://"+url_base+"/".join(path.split("/")[:-1])+"/"+src

				links.append(src)
				con+=1

	return links


# Funcion que convierte una fecha en string a un objeto datetime
def fecha_a_datetime(fecha):
	lista = map(int,fecha.split("-"))
	return datetime(lista[0],lista[1],lista[2])
# -------------------------------------------------------------------------
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

		if u.has_perm("buscador.can_crud_contenidos"):
			can_crud_contenidos = 1

		if u_name == "ADMIN":
			es_admin = 1


		if request.GET.get('salir'):
			return logout_view(request)


	# Busqueda

	resultados=[]

	if request.method == "POST":

		busqueda = request.POST.get("search")
		request.session["busqueda"] = busqueda
		resultados = google.search(busqueda,2)

		b = Busqueda(texto_buscado=busqueda)
		b.save()

		lista_urls = []
		for res in resultados:
			lista_urls.append(res.link)

		request.session["resultados"] = lista_urls

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

		if u.has_perm("buscador.can_crud_contenidos"):
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

			elif tipo_usuario == "Alumno":
				tipo_usuario = 1

		# Verificacion de informacion ingresada

		username_search = User.objects.filter(username = username)

		if len(username_search) == 0:

			if fecha_nacimiento < datetime.now():

				if institucion in nombres_instituciones:

					user = User.objects.create_user(username, email, password)
					user.save()

					up = UserProfile(user=user, institucion=institucion, tipo_usuario = tipo_usuario,fecha_nac=fecha_nacimiento.date())
					up.save()

					alumnos_group = Group.objects.get(name="Alumnos")
					profesores_group = Group.objects.get(name="Profesores")

					if(tipo_usuario == 0):
						user.groups.add(profesores_group)
					elif(tipo_usuario == 1):
						user.groups.add(alumnos_group)

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
	es_admin = 0
	conected = 0
	can_crud_contenidos = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("buscador.can_crud_contenidos"):
			can_crud_contenidos = 1

		if request.user.username == "ADMIN":
			es_admin = 1

		if request.GET.get('salir'):
			return logout_view(request)


	if request.method == "POST":

		links = request.session["resultados"]
		ids_links_selected = request.POST.getlist("seleccion-link")

		lista_contenidos = []
		lista_links_imagenes = []

		texto_contenidos = []
		url_imgs = []

		for i in ids_links_selected:
			url_link = links[int(i)]
			contenidos = contenidos_relevantes(url_link)
			links_imagenes = extraer_links_imagenes(url_link)

			for cont in contenidos:
				texto_contenidos.append((cont,url_link))

				obj_cont = contenido(cont,len(lista_contenidos))
				lista_contenidos.append(obj_cont)

			for link in links_imagenes:
				url_imgs.append((link,url_link))

				obj_cont = contenido(link,len(lista_links_imagenes))
				lista_links_imagenes.append(obj_cont)


		request.session["texto_contenidos"] = texto_contenidos
		request.session["url_imgs"] = url_imgs

		context={'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos,"es_admin":es_admin,
		"contenidos":lista_contenidos,"contenidos":lista_contenidos,"range_contenidos":range(len(lista_contenidos)),
		"links_imagenes":lista_links_imagenes,"range_links_imagenes":range(len(lista_links_imagenes))}

		return render(request, 'buscador/extraccion-contenidos.html',context)


	context={'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos}

	return render(request, 'buscador/resultados.html',context)




@login_required(login_url="/")
def extraccion_contenidos(request):

	# Verificacion de usuario
	es_admin = 0
	conected = 0
	can_crud_contenidos = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("buscador.can_crud_contenidos"):
			can_crud_contenidos = 1

		if request.user.username == "ADMIN":
			es_admin = 1

		if request.GET.get('salir'):
			return logout_view(request)


	if request.method == "POST":
		
		texto_contenidos = request.session["texto_contenidos"]
		links_imagenes = request.session["url_imgs"]

		ids_selected_contents = request.POST.getlist("contenidos")
		ids_selected_imgs = request.POST.getlist("imagenes")

		busqueda = request.session["busqueda"]
		t = Tag.objects.get(nombre_tag="SIN TAG")

		for i in ids_selected_contents:
			contenido, link = texto_contenidos[int(i)]
			c = Contenido(tipo_contenido="texto",info=contenido,dominio_fuente=link, busqueda=busqueda, tag=t)
			c.save()

		for i in ids_selected_imgs:
			url_img, link = links_imagenes[int(i)]
			c = Contenido(tipo_contenido="imagen",info=url_img,dominio_fuente=link, busqueda=busqueda, tag=t)
			c.save()


		return HttpResponseRedirect("/buscador/ver-contenidos/")




	context={'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos, "es_admin":es_admin}

	return render(request, 'buscador/extraccion-contenidos.html',context)





@login_required(login_url="/")
def ver_contenidos(request):

	# Verificacion de usuario
	es_admin = 0
	conected = 0
	can_crud_contenidos = 0

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("buscador.can_crud_contenidos"):
			can_crud_contenidos = 1

		if request.user.username == "ADMIN":
			es_admin = 1

		if request.GET.get('salir'):
			return logout_view(request)


	contenidos = Contenido.objects.filter(tipo_contenido="texto")
	imagenes = Contenido.objects.filter(tipo_contenido="imagen")

	range_contenidos = range(len(contenidos))
	range_links_imagenes = range(len(imagenes))

	tags = Tag.objects.all()



	if request.method == "POST":

		print "EN EL POST!"

		cambio_tag = request.POST['cambio_tag']
		print cambio_tag
		t = Tag.objects.get(nombre_tag=cambio_tag)

		ids_selected_contents = request.POST.getlist("contenidos_ver")
		ids_selected_imgs = request.POST.getlist("imagenes_ver")

		print ids_selected_contents
		print ids_selected_imgs

		for ide in ids_selected_contents:
			cont = contenidos[int(ide)-1]
			cont.tag = t
			cont.save()

		for ide in ids_selected_imgs:
			image = imagenes[int(ide)-1]
			image.tag = t
			image.save()

	context={"imagenes":imagenes,"contenidos":contenidos,'conected' : conected, 'u_name' : u_name,
	 'can_crud_contenidos' : can_crud_contenidos, "es_admin":es_admin, "range_contenidos":range_contenidos,
	 "range_links_imagenes":range_links_imagenes,"tags":tags}

	return render(request, 'buscador/ver_contenidos.html',context)





@login_required(login_url="/")
def paginas_de_confianza(request):

	# Verificacion de usuario
	es_admin = 0
	conected = 0
	can_crud_contenidos = 0
	men = ""

	if request.user.is_authenticated():
		conected = 1

		u = request.user
		u_name = u.username

		if u.has_perm("buscador.can_crud_contenidos"):
			can_crud_contenidos = 1

		if request.user.username == "ADMIN":
			es_admin = 1

		if request.GET.get('salir'):
			return logout_view(request)

	paginas_de_confianza = PaginaDeConfianza.objects.all()
	up = UserProfile.objects.get(user=u)
	paginas_rating = []

	#ratings_actuales = []

	for pagina in paginas_de_confianza:

		rating = RatingPagina.objects.filter(user=up,pagina_confianza=pagina)

		if(len(rating)==0):
			pag_rat = Pagina_Rating(pagina,0)
			paginas_rating.append(pag_rat)
			#ratings_actuales.append(0)

		else:
			r = rating[0]
			pag_rat = Pagina_Rating(pagina,r.rating)
			paginas_rating.append(pag_rat)
			#ratings_actuales.append(r.rating)


	if request.method == "POST":

		delete_dominio = request.POST.get('delete_id')
		change_rating = request.POST.get("change_rating")
		print change_rating
		
		if delete_dominio == "" or delete_dominio == None:

			if(change_rating != None and len(change_rating) > 1):

				changed_rating_ids = set(map(int,change_rating.split(","))[1:])
				ratings_nuevos = request.POST.getlist("input_rate")

				for ide in changed_rating_ids:
					pagina = paginas_de_confianza[ide-1]
					ratings_user = RatingPagina.objects.filter(user=up,pagina_confianza=pagina)

					if(len(ratings_user) == 0):
						r = RatingPagina(rating=ratings_nuevos[ide-1],user=up,pagina_confianza=pagina)
						r.save()
					else:
						r = ratings_user[0]
						r.rating = ratings_nuevos[ide-1]
						r.save()

				return HttpResponseRedirect("/buscador/paginas-de-confianza/")

			else:
				# Añadir Pagina de confianza
				url = request.POST['url']

				if existe_pagina(url):

					pags = PaginaDeConfianza.objects.filter(dominio=url)

					if len(pags) == 0:
						pag = PaginaDeConfianza(dominio=url)
						pag.save()
						return HttpResponseRedirect("/buscador/paginas-de-confianza/")
					else:
						men = "YA EXISTE LA PAGINA DE CONFIANZA INGRESADA"
				else:
					men = "LA PAGINA DE CONFIANZA INGRESADA NO ES VALIDA"

		else:

			deleted_page = PaginaDeConfianza.objects.get(dominio=delete_dominio)
			deleted_page.delete()
			return HttpResponseRedirect("/buscador/paginas-de-confianza/")


	context={'conected' : conected, 'u_name' : u_name, 'can_crud_contenidos' : can_crud_contenidos,
	 "es_admin":es_admin,"paginas_rating":paginas_rating, "men":men}

	return render(request, 'buscador/paginas_de_confianza.html',context)