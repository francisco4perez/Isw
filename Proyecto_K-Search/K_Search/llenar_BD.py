from django.db import models
from buscador.models import *
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime
import subprocess

print "------------- LLENANDO LA BASE DE DATOS -------------------"

print "Instituciones"

instituciones = ["FEDERICO SANTA MARIA"]

for inst_name in instituciones:

      inst = Institucion(nombre_institucion=inst_name)
      inst.save()


print "Paginas de Confianza"

paginas = ["http://www.howstuffworks.com/","http://www.lawebdefisica.com/",
"http://www.livescience.com/","https://www.nasa.gov/","https://www.sciencedaily.com/"]

for pagina in paginas:

      p = PaginaDeConfianza(dominio=pagina)
      p.save()


print "Areas"

areas = ["FISICA","MATEMATICA","INGENIERIA DE SOFTWARE","HUMANISTICA"]

for area in areas:

	paginas_bd = PaginaDeConfianza.objects.all()

	a = Area(nombre_area=area,descripcion_area="Area con fundamentos en "+area)
	a.save()
	a.paginas_de_confianza.set(paginas_bd)
	a.save()

# Users
print "Users"

# Usuarios iniciales
usernames = ["Goku","Alphy","Juan"]
emails = ["asd@asd.com","alfredo.silva.13@sansano.usm.cl","juan.escalona.13@sansano.usm.cl"]
passwords = ["12345","12345","12345"]

institucion = "FEDERICO SANTA MARIA"
fecha_nacimiento = datetime.now()

for i in range(len(usernames)):
      user = User.objects.create_user(usernames[i], emails[i], passwords[i])
      user.save()

      up = UserProfile(user=user, institucion=institucion, fecha_nac=fecha_nacimiento.date())
      up.save()

# Creacion super usuario ADMIN
print "------------------Creacion ADMIN-----------------------"
print "Por favor ingresar el nombre: ADMIN y cualquier contrasenia!"
subprocess.call(['./manage.py', "createsuperuser"])

admin = User.objects.get(username="ADMIN")

ad = UserProfile(user=admin, institucion=institucion, fecha_nac=fecha_nacimiento.date())
ad.save()



# Groups (De permisos)
print "Groups"

alumnos_group = Group(name="Alumnos")
profesores_group = Group(name="Profesores")

alumnos_group.save()
profesores_group.save()

# Permissions (Poner mas permisos)
print "Permisos"

p_can_crud_contenidos = Permission.objects.get(codename="can_crud_contenidos")

p_can_crud_contenidos.save()

profesores_group.permissions.add(p_can_crud_contenidos)
#alumnos_group.permissions.add(p_can_crud_contenidos)

# ADMIN tiene todos los permisos existentes
u_s = User.objects.get(username="ADMIN")
u_s.groups.add(alumnos_group,profesores_group)

print "All Done! Bye, for now."