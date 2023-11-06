from django.shortcuts import render, redirect
from .models import Alumno
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .registro import *
import datetime
from openpyxl import Workbook
from django.http.response import HttpResponse

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

def diasSemanaActual():
    # Obtiene la fecha actual
    fecha_actual = datetime.date.today()

    # Obtiene el número del día de la semana (0=domingo, 1=lunes, ..., 6=sábado)
    numero_dia_semana = fecha_actual.weekday()

    # Calcula la fecha del primer día de la semana (lunes)
    primer_dia_semana = fecha_actual - datetime.timedelta(days=numero_dia_semana)

    # Calcula las fechas de los días de la semana actual
    fechas_semana_actual = [primer_dia_semana + datetime.timedelta(days=i) for i in range(7)]

    return fechas_semana_actual


def crearAsistenciaSemana(alumno : Alumno):
    # Muestra las fechas de la semana actual
    for fecha in diasSemanaActual():
        dia = ObtenerDiaPorFecha(fecha)
        if not dia:
            RegistrarDia(fecha)
            dia = ObtenerDiaPorFecha(fecha)
        RegistrarAsistencia(alumno, dia)

def video_procesamiento(request):
    if request.method == 'POST':
        response = ''
        try:
            print(request.FILES)
            foto = request.FILES['recognocer']
            with open('media/input/person.jpg', 'wb') as archivo:
                for chunk in foto.chunks():
                    archivo.write(chunk)

            persona = recognize_person('person.jpg').replace('_', ' ')
            alumno = ObtenerAlumnoPorNombre(persona)

            if not alumno:
                return HttpResponse('Persona no reconocida')

            fecha_actual = datetime.date.today()
            #fecha_formateada = fecha_actual.strftime("%d-%m-%Y")
            dia = ObtenerDiaPorFecha(fecha_actual)

            if not dia:
                RegistrarDia(fecha_actual)
                dia = ObtenerDiaPorFecha(fecha_actual)
                print(f'El dia se ha registrado ==> {dia}')
                
            asistencia = ObtenerAsistencia(alumno, dia)

            if not asistencia:
                crearAsistenciaSemana(alumno)
                print(f'Creando la asistencia de la semana para {alumno}')
                asistencia = ObtenerAsistencia(alumno, dia)

            if asistencia.asistencia == '0':
                asistencia.asistencia = '1'
                asistencia.save()
                response = f'Se registro la asistencia para el alumno {alumno.nombre}'
            else:
                response = f'El alumno {alumno.nombre} ya tiene registrada una asistencia'
            return HttpResponse(response)
            

        except MultiValueDictKeyError as e:
            print(f'Error: {e}')
            return HttpResponse("Error: Error al manejar el formulario")
    else:
        return HttpResponse("El request no es de tipo POST")

def verReporte(request):
    dias = Dia.objects.filter(fecha__in=diasSemanaActual()) 
    registros = Alumno.objects.all()
    asistencias = []
    print(f'DIAS ===> {dias}')
    print(f'REGISTROS ===> {registros}')
    for i in registros:
        asistencia = Asistencia.objects.filter(alumno=i, dia__in=dias)
        if not asistencia:
            crearAsistenciaSemana(i)
            asistencia = Asistencia.objects.filter(alumno=i, dia__in=dias)
        print('******************************************')
        print(f'Alumno {i.nombre}')

        asistenciaAlumno = []
        asistenciaAlumno.append(i.nombre)

        for a in asistencia:
            print(f'{a.dia.fecha}: {a.asistencia}')
            asistenciaAlumno.append(a.asistencia)
        
        asistencias.append(asistenciaAlumno)

    return render(request, "reporte.html", {'dias': dias, 'asistencias': asistencias})
