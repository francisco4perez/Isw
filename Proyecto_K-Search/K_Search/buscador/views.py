# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def main_view(request):

	var1 = 5

	context = {'var1' : var1}

	return render(request, 'buscador/index.html',context)
