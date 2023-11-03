from django.db import models

# Create your models here.

class Curso(models.Model):
    nua = models.CharField(primary_key=True,max_length=6)
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="alumnos", null=True)

    def __str__(self):
        texto = "{} ({})"
        return texto.format(self.nua, self.nombre)

class Dia(models.Model):
    fecha = models.CharField(primary_key=True,max_length=6)
    asistencia = models.CharField(max_length=100)

    def __str__(self):
        texto = "{} ({})"
        return texto.format(self.fecha, self.asistencia)

class Semana(models.Model):
    lunes = Dia
    martes = Dia
    miercoles = Dia
    jueves = Dia
    viernes = Dia

    def __str__(self):
        texto = "{} ({})"
        return texto.format(self.nua, self.nombre)