from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_alumno, name='login_alumno'),
    path('registro/', views.registro_alumno, name='registro_alumno'),
    path('home/', views.welcome_page, name='welcome'),
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('profe/', views.lista_profe, name='lista_profe'),
    path('comentarios_alumno/', views.comentarios_alumno, name='comentarios_alumno'),
    path('detalles_inscripcion/<str:nombre_usuario>/<str:nombre_curso>/', views.detalles_inscripcion, name='detalles_inscripcion'),
    path('guardar_inscripcion/', views.guardar_inscripcion, name='guardar_inscripcion'),
    path('pagina_confirmacion_inscripcion/', views.pagina_confirmacion_inscripcion, name='pagina_confirmacion_inscripcion'),
    path('perfil/', views.ver_inscripciones, name='ver_inscripciones'),
    path('pagina_error_inscripcion/', views.pagina_error_inscripcion, name='pagina_error_inscripcion'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('borrar_comentario/<int:comentario_id>/', views.borrar_comentario, name='borrar_comentario')


]
