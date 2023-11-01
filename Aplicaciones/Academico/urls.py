from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('registrarAlumno/', views.registrarAlumno),
    path('eliminacionAlumno/<nua>', views.eliminarAlumno),
    path('edicionAlumno/<nua>', views.edicionAlumno),
    path('recognize/', views.recognize_view),
    path('video_procesamiento/', views.video_procesamiento),
    path('editarAlumno/', views.editarAlumno)
]