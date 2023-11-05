from .models import Alumno, Dia, Asistencia


def ObtenerAlumnoPorNombre(nombre):
    try:
        filtered_alumn = Alumno.objects.get(nombre=nombre)
        return filtered_alumn
    except:
        return None
    

def ObtenerDiaPorFecha(dia):
    try:
        date = Dia.objects.get(fecha=dia)
        return date or None
    except:
        return None

def RegistrarDia(dia):
    Dia.objects.create(fecha=dia)

def RegistrarAsistencia(alumno, dia):
    Asistencia.objects.create(alumno=alumno, dia=dia, asistencia='1')

def ObtenerAsistencia(alumno, dia):
    try:
        asistencia = Asistencia.objects.get(alumno=alumno, dia=dia, asistencia='1')
        return asistencia or None
    except:
        return None






