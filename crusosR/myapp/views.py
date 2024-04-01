from django.shortcuts import render, redirect
from .models import Cursos, Profesor, Alumno, Comentario, CursoInscrito
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404


def login_alumno(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home/')  # Redirige al dashboard del alumno o a donde desees
        else:
            # Usuario no válido
            return render(request, 'login_alumno.html', {'error_message': 'Credenciales inválidas.'})
    else:
        return render(request, 'login_alumno.html')


def registro_alumno(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        
        user = User.objects.create_user(username=username, password=password, email=email)
        
     
        alumno = Alumno.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            nombre_usuario=username,
            contraseña=password,
            email=email
        )

        return redirect('login_alumno')
    else:
        return render(request, 'registro_alumno.html')



def welcome_page(request):
    # Supongamos que obtienes el objeto alumno de alguna manera
    alumno = Alumno.objects.get(pk=1)  # Esto es solo un ejemplo, debes obtener el alumno de la manera correcta en tu aplicación
    return render(request, 'welcome.html', {'alumno': alumno})



def lista_cursos(request):
    cursos = Cursos.objects.all()
    tipos = Cursos.objects.values_list('tipo', flat=True).distinct()
    años = Cursos.objects.values_list('años', flat=True).distinct()

    tipo_filtrado = request.GET.get('tipo')
    años_filtrados = request.GET.get('años')
    search_query = request.GET.get('search')

    if tipo_filtrado:
        cursos = cursos.filter(tipo=tipo_filtrado)
    if años_filtrados:
        cursos = cursos.filter(años=años_filtrados)
    if search_query:
        cursos = cursos.filter(nombre__icontains=search_query)

    return render(request, 'cursos.html', {'cursos': cursos, 'tipos': tipos, 'años': años})



def detalles_inscripcion(request, nombre_usuario, nombre_curso):
    return render(request, 'detalles_inscripcion.html', {'nombre_usuario': nombre_usuario, 'nombre_curso': nombre_curso})



def guardar_inscripcion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        nombre_curso = request.POST.get('nombre_curso')
        
        # Obtener la instancia del modelo Alumno correspondiente al nombre de usuario
        alumno = Alumno.objects.get(nombre_usuario=nombre_usuario)
        
        # Verificar si el alumno ya está inscrito en este curso
        if CursoInscrito.objects.filter(alumno=alumno, nombre_curso=nombre_curso).exists():
            # Si ya está inscrito, redirigir a alguna página de error o a donde desees
            return redirect('pagina_error_inscripcion')
        
        # Si el alumno no está inscrito, crear una nueva instancia de CursoInscrito y guardarla
        CursoInscrito.objects.create(alumno=alumno, nombre_curso=nombre_curso)
        
        # Envío de correo electrónico de confirmación
        subject = 'Confirmación de Inscripción'
        message = 'Hola,\n\nYa estás inscrito.\n'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [alumno.email]  # Aquí asumo que el modelo Alumno tiene un campo "email"
        
        send_mail(subject, message, email_from, recipient_list)
        
        return redirect('pagina_confirmacion_inscripcion')
    else:
        return redirect('inicio')
    
    
def pagina_confirmacion_inscripcion(request):
    return render(request, 'pagina_confirmacion_inscripcion.html')


def pagina_error_inscripcion(request):
    return render(request, 'pagina_error_inscripcion.html')


import os

def obtener_ruta_imagen(nombre_profesor):
    ruta_carpeta_imagenes = r'C:\Users\crist\Desktop\cusoR-main\crusosR\myapp\static\img'
    nombre_archivo_imagen = nombre_profesor.lower() + '.png'  # Suponiendo que los nombres de archivo son los nombres de los profesores en minúsculas seguidos de ".png"
    ruta_imagen = os.path.join(ruta_carpeta_imagenes, nombre_archivo_imagen)
    return ruta_imagen

def lista_profe(request):
    # Obtener todos los profesores y todos los cursos
    profesores = Profesor.objects.all()
    cursos = Cursos.objects.all()

    # Obtener tipos únicos de cursos
    tipos_cursos = cursos.values_list('tipo', flat=True).distinct()

    # Obtener parámetros de filtrado
    nombre_filtrado = request.GET.get('nombre_curso')
    descripcion_filtrada = request.GET.get('descripcion_curso')
    tipo_filtrado = request.GET.get('tipo_curso')

    # Filtrar profesores según los parámetros de filtrado
    if nombre_filtrado:
        profesores = profesores.filter(cursos__nombre=nombre_filtrado)
    
    if descripcion_filtrada:
        profesores = profesores.filter(cursos__descripcion=descripcion_filtrada)
    
    if tipo_filtrado:
        profesores = profesores.filter(cursos__tipo=tipo_filtrado)

    return render(request, 'profes.html', {'profesores': profesores, 'tipos_cursos': tipos_cursos})
                  
                  

def comentarios_alumno(request):
    comentarios = Comentario.objects.all()
    
    if request.method == 'POST':
        # Si se envía un formulario POST, primero verificamos si es para agregar un nuevo comentario o dar like a uno existente
        if 'texto' in request.POST:  # Si hay un campo de texto, significa que se está agregando un nuevo comentario
            texto = request.POST.get('texto')
            usuario = request.user
            alumno, creado = Alumno.objects.get_or_create(nombre_usuario=usuario.username)
            Comentario.objects.create(alumno=alumno, texto=texto)
            return redirect('comentarios_alumno')
        elif 'like' in request.POST:  # Si hay un botón de like, significa que se está dando like a un comentario existente
            comentario_id = request.POST.get('comentario_id')
            comentario = Comentario.objects.get(pk=comentario_id)
            comentario.toggle_like(request.user)
            return redirect('comentarios_alumno')

    return render(request, 'comentarios_alumno.html', {'comentarios': comentarios})

def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    if comentario.alumno.nombre_usuario != request.user.username:
        return redirect('comentarios_alumno')  # O mostrar algún mensaje de error
    
    if request.method == 'POST':
        comentario.texto = request.POST.get('texto')
        comentario.save()
        return redirect('ver_inscripciones')
    else:
        return render(request, 'editar_comentario.html', {'comentario': comentario})

def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    if request.method == 'POST':
        comentario.delete()  # Eliminar el comentario si se recibe una solicitud POST
        return redirect('ver_inscripciones')  # Redirigir a la vista de inscripciones después de borrar
    
    return render(request, 'delete_comentario.html', {'comentario': comentario})

def ver_inscripciones(request):
    usuario = request.user

    alumno = Alumno.objects.get(nombre_usuario=usuario.username)

    # Filtrar las inscripciones del usuario actual
    perfil = CursoInscrito.objects.filter(alumno__nombre_usuario=usuario.username)

    # Obtener los comentarios del alumno
    comentarios_alumno = Comentario.objects.filter(alumno=alumno)

    return render(request, 'perfil.html', {'alumno': alumno, 'perfil': perfil, 'comentarios_alumno': comentarios_alumno})