from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cursos(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    decribcion = models.CharField(max_length=255)
    años = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='profesor_images/', null=True, blank=True)
    cursos = models.ForeignKey(Cursos, on_delete=models.CASCADE)

    def __str__(self):
        return {self.nombre}

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()
    nombre_usuario = models.CharField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=255)
    cursos_inscritos = models.ManyToManyField(Cursos)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Comentario(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comentarios_likes', blank=True)

    def __str__(self):
        return f"Comentario de {self.alumno.nombre} {self.alumno.apellido}"

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def can_edit(self, user):
        return user == self.alumno.nombre_usuario

    def delete_comment(self):
        self.delete()
    
class CursoInscrito(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    nombre_curso = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.alumno} - {self.nombre_curso}"