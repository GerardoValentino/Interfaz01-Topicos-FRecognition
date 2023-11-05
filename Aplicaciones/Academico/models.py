from django.db import models

# Create your models here.

class Alumno(models.Model):
    nua = models.CharField(primary_key=True,max_length=6)
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="alumnos", null=True)

    def __str__(self):
        texto = "{} ({})"
        return texto.format(self.nua, self.nombre)

class Dia(models.Model):
    fecha = models.CharField(primary_key=True,max_length=12)
    

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    dia = models.ForeignKey(Dia, on_delete=models.CASCADE)
    asistencia = models.CharField(max_length=3)


class Semana(models.Model):
    lunes = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='semana_lunes')
    martes = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='semana_martes')
    miercoles = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='semana_miercoles')
    jueves = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='semana_jueves')
    viernes = models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='semana_viernes')


    
class Calendario(models.Model):
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)
    