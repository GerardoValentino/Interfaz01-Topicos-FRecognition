from django.db import models

# Create your models here.

class Curso(models.Model):
    nua=models.CharField(primary_key=True,max_length=6)
    nombre=models.CharField(max_length=100)

    def __str__(self):
        texto = "{} ({})"
        return texto.format(self.nua, self.nombre)