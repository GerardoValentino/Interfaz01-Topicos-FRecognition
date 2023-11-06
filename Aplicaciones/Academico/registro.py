from .models import Alumno, Dia, Asistencia


def ObtenerAlumnoPorNombre(nombre):
    try:
        filtered_alumn = Alumno.objects.get(nombre=nombre)
        return filtered_alumn
    except:
        print(f'No se pudo obtener el alumno {nombre}')
        return None
    

def ObtenerDiaPorFecha(dia):
    try:
        date = Dia.objects.get(fecha=dia)
        return date 
    except:
        print(f'No se pudo obtener la fecha {dia}')
        return None

def RegistrarDia(dia):
    try:
        Dia.objects.create(fecha=dia)
    except:
        print(f'No se pudo registrar el dia {dia}')

def RegistrarAsistencia(alumno, dia):
    try:
        Asistencia.objects.create(alumno=alumno, dia=dia, asistencia='0')
    except:
        print(f'No se pudo registrar la asistencia {alumno, dia}')

def ObtenerAsistencia(alumno, dia):
    try:
        asistencia = Asistencia.objects.get(alumno=alumno, dia=dia)
        return asistencia 
    except:
        print(f'No se pudo obtener la asistencia {alumno, dia}')
        return None






