from django.db import models
from django.contrib.auth.models import User

# Create your Models here.
class Partido(models.Model):
	nombre = models.CharField(max_length=120)
	def __unicode__(self):
                return self.nombre

class Senador(models.Model):
	nombre = models.CharField(max_length=120)
	#foto = models.CharField(max_length=120)
	partido = models.ForeignKey(Partido)
	def __unicode__(self):
                return self.nombre

class Estado(models.Model):
        nombre = models.CharField(max_length=120)
        def __unicode__(self):
                return self.nombre

class Proyecto(models.Model):
	numero = models.CharField(max_length=120)
	nombre = models.CharField(max_length=120)
	fechaRadicacion = models.DateField()
	descripcion = models.CharField(max_length=120)
	estado = models.ForeignKey(Estado)
	ponentes = models.ManyToManyField(Senador)
	def __unicode__(self):
		return self.nombre

class Articulo(models.Model):
	nombre = models.CharField(max_length=200)
	texto = models.TextField()
	proyecto = models.ForeignKey(Proyecto)
	def __unicode__(self):
                return self.nombre

# ToDo: cambiar esto a singular
class Observaciones(models.Model):
	autor = models.ForeignKey(User)
	texto = models.TextField()
	fecha = models.DateField()
	articulo = models.ForeignKey(Articulo)
	def __unicode__(self):
                return str(self.autor.username)+" - "+self.texto[0:20]


