# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

admin.site.register(Institucion)
admin.site.register(Area)
admin.site.register(PaginaDeConfianza)
admin.site.register(Tag)