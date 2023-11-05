from django.shortcuts import render, redirect
from .models import Alumno
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .registro import *
import datetime

from .face_recog import extrae_rostros, recognize_person
# from django.contrib import messages

# Create your views here.

def home(request):
    alumnosListados = Alumno.objects.all()
    return render(request, "gestionAlumnos.html", {"alumnos": alumnosListados})

def registrarAlumno(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            nua = request.POST['txtNUA']
            nombre = request.POST['txtNombre']
            foto = request.FILES['fotoAlumno']

            alumno = Alumno.objects.create(nua=nua, nombre=nombre, foto=foto)
            alumno.foto.delete(save=True)
            newName = nombre.replace(' ', '_') + '.jpg'
            alumno.foto.save(newName, foto)
            extrae_rostros(newName)
            return redirect('/')
        except MultiValueDictKeyError as e:
            print(f'Error: {e}')
            return HttpResponse("Error: El campo 'fotoAlumno' no se encuentra en request.FILES.")
    else:
        return HttpResponse("El formulario no se envió correctamente.")


def eliminarAlumno(request, nua):
    alumno = Alumno.objects.get(nua=nua)
    alumno.delete()
    return redirect('/')

def edicionAlumno(request, nua):
    alumno = Alumno.objects.get(nua=nua)
    return render(request, "edicionAlumno.html", {"alumno": alumno})

def editarAlumno(request):
    nua = request.POST['txtNUA']
    nombre = request.POST['txtNombre']
    alumno = Alumno.objects.get(nua=nua)
    alumno.nua = nua
    alumno.nombre = nombre 
    alumno.save()
    return redirect('/')

def recognize_view(request):
    return render(request, 'recognize.html')

def video_procesamiento(request):
    if request.method == 'POST':
        try:
            print(request.FILES)
            foto = request.FILES['recognocer']
            with open('media/input/person.jpg', 'wb') as archivo:
                for chunk in foto.chunks():
                    archivo.write(chunk)

            persona = recognize_person('person.jpg').replace('_', ' ')
            alumno = ObtenerAlumnoPorNombre(persona)

            if not alumno:
                return HttpResponse(persona)

            fecha_actual = datetime.datetime.now()
            fecha_formateada = fecha_actual.strftime("%d-%m-%Y")
            dia = ObtenerDiaPorFecha(fecha_formateada)

            if not dia:
                RegistrarDia(dia)
                dia = ObtenerDiaPorFecha(fecha_formateada)
                print(f'El dia se ha registrado ==> {dia}')
                
            asistencia = ObtenerAsistencia(alumno, dia)

            if not asistencia:
                RegistrarAsistencia(alumno, dia)
                print(f'Creando asistencia para {alumno}')
            return HttpResponse(persona)

        except MultiValueDictKeyError as e:
            print(f'Error: {e}')
            return HttpResponse("Error: Error al manejar el formulario")
    else:
        return HttpResponse("El request no es de tipo POST")