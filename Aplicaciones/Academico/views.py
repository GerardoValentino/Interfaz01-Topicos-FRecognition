from django.shortcuts import render, redirect
from .models import Curso
# from django.contrib import messages

# Create your views here.

def home(request):
    alumnosListados = Curso.objects.all()
    #messages.success(request, '¡Alumnos Listados!')
    return render(request, "gestionAlumnos.html", {"alumnos": alumnosListados})

def registrarAlumno(request):
    nua = request.POST['txtNUA']
    nombre = request.POST['txtNombre']

    alumno = Curso.objects.create(nua=nua, nombre=nombre)
    return redirect('/')

def eliminarAlumno(request, nua):
    alumno = Curso.objects.get(nua=nua)
    alumno.delete()
    return redirect('/')

def edicionAlumno(request, nua):
    alumno = Curso.objects.get(nua=nua)
    return render(request, "edicionAlumno.html", {"alumno": alumno})

def editarAlumno(request):
    nua = request.POST['txtNUA']
    nombre = request.POST['txtNombre']
    alumno = Curso.objects.get(nua=nua)
    alumno.nua = nua
    alumno.nombre = nombre 
    alumno.save()
    return redirect('/')

