import os
import django

# Establece la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UG.settings")
django.setup()

from Aplicaciones.Academico.models import Curso

# Consulta a la base de datos para obtener todos los registros del modelo
registros = Curso.objects.all()
registros_lista = list(registros.values())

for registro in registros_lista:
    print(registro)
