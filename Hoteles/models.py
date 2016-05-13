from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hotel(models.Model):
    Nombre = models.CharField(max_length = 32)
    Categ = models.CharField(max_length = 32)
    SubCateg = models.IntegerField()
    Descrip = models.TextField(default = "")
    Direccion = models.TextField(default = "")
    Url = models.TextField()
    telefono = models.IntegerField()

class Imagen(models.Model):
    Url = models.TextField()
    Hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)

class Comentario(models.Model):
    User =  models.CharField(max_length = 32)
    Date = models.DateField(auto_now=False, auto_now_add=False, default = date.today)
    body = models.TextField(default = "")
    Hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)

class Hotel_selecc (models.Model):
    User = models.CharField(max_length = 32)
    Hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)

class CSS (models.Model):
    User: models.CharField(max_length = 32)
    Letra: models.IntegerField()
    Color: models.CharField(max_length = 32, default = 'black')

class Titulo(models.Model):
    User: models.CharField(max_length = 32)
    body: models.TextField()
