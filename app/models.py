from django.db import models
from django.conf import settings

class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=100, unique=True, default='Nombre')
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, related_name='proyectos_creados', on_delete=models.CASCADE)
    tema = models.CharField(max_length=100)
    patrocinio = models.BooleanField(default=False)
    profesor_patrocinador = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='proyectos_patrocinados', on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo proyecto
            self.estudiante = kwargs.pop('user', None)  # Asignar al usuario que lo crea como estudiante
        elif self.patrocinio and 'user' in kwargs:  # Si el proyecto ya existe y se activa el patrocinio
            self.profesor_patrocinador = kwargs['user']  # Asignar al usuario que realiza el cambio
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
