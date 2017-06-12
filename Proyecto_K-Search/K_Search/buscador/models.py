# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
#from .UserProfile.models import UserProfile
#import sys
#sys.path.append('./UserProfile')
#from UserProfile import UserProfile

#-------------------------------------


class Contenido(models.Model):
	tipo_contenido = models.CharField(max_length = 30)
	descripcion_contenido = models.CharField(max_length = 150, default = "")
	info = models.CharField(max_length = 500)

	area = models.ForeignKey("Area")

	def __str__(self):
		return self.info



class PaginaDeConfianza(models.Model):
	dominio = models.CharField(max_length = 200,unique=True)
	fecha_pagina = models.DateField(default=timezone.now)

	def __str__(self):
		return self.dominio


class RatingPagina(models.Model):
	rating = models.IntegerField(default=0)
	
	user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
	pagina_confianza = models.ForeignKey("PaginaDeConfianza", on_delete=models.CASCADE)

	def __str__(self):
		return self.rating


class Feedback(models.Model):
	descripcion_feedback = models.CharField(max_length = 100)
	
	user = models.ForeignKey("UserProfile")
	area = models.ForeignKey("Area")

	def __str__(self):
		return self.descripcion_feedback


class Area(models.Model):
	nombre_area = models.CharField(max_length = 100)
	descripcion_area = models.CharField(max_length = 200)

	paginas_de_confianza = models.ManyToManyField("PaginaDeConfianza")

	def __str__(self):
		return self.nombre_area


class Inscription(models.Model):
	fecha_inscripcion = models.DateField()
	
	user = models.ForeignKey("UserProfile")
	area = models.ForeignKey("Area")

	def __str__(self):
		return self.fecha_inscripcion



class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tipo_usuario = models.IntegerField(default=1)
	institucion = models.CharField(max_length = 100, default="USM")
	fecha_nac = models.DateField()

	user_ratings = models.ManyToManyField("RatingPagina")

	def __str__(self):
		return self.user.username

	class Meta:

		permissions = (
            ("can_crud_contenidos",               "Can do crud for contents"),
        )


class Institucion(models.Model):
	nombre_institucion = models.CharField(max_length = 100)

	def __str__(self):
		return self.nombre_institucion


class Tags(models.Model):
	nombre_tag = models.CharField(max_length = 40)

	def __str__(self):
		return self.nombre_tag
