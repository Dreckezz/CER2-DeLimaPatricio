from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import FormCrearProyecto, ProyectoPatrocinioForm, ProyectoModificarForm
from .models import Proyecto

def inicio(request):
    data = {}
    user = request.user

    # Manejo del formulario de autenticación
    if request.method == 'POST':
        login = AuthenticationForm(request, data=request.POST)
        if login.is_valid():
            user = login.get_user()
            login(request, user)
            data['mensaje'] = 'Sesión iniciada con éxito'
        else:
            data['mensaje'] = 'Usuario o contraseña incorrecta'
    
    # Obtener proyectos basados en el filtro
    filtroPatrocinio = request.GET.get('filtro')
    proyectos = Proyecto.objects.all()
    if filtroPatrocinio == 'con':
        proyectos = Proyecto.objects.filter(patrocinio=True)
    elif filtroPatrocinio == 'sin':
        proyectos = Proyecto.objects.filter(patrocinio=False)

    # Procesamiento del formulario de patrocinio
    patrocinar_form = ProyectoPatrocinioForm(request.POST or None)
    if patrocinar_form.is_valid() and user.is_authenticated:
        proyecto = patrocinar_form.save(profesor=user if patrocinar_form.cleaned_data['patrocinar'] else None)
        data['patrocinar'] = proyecto
    data['patrocinar_form'] = patrocinar_form

    # Creación de proyecto si el usuario es un estudiante autenticado
    if user.is_authenticated and user.groups.filter(name='Estudiante').exists() and request.method == 'POST':
        crear_proyecto_form = FormCrearProyecto(request.POST, user=user)
        if crear_proyecto_form.is_valid():
            crear_proyecto_form.save()
        else:
            data['crearProyecto'] = crear_proyecto_form

    # Modificación de proyecto
    modificar_proyecto_form = ProyectoModificarForm(request.POST or None, instance=None)
    if modificar_proyecto_form.is_valid() and user.is_authenticated:
        proyecto_modificado = modificar_proyecto_form.save()
        data['proyecto_modificado'] = proyecto_modificado
    data['modificar_proyecto_form'] = modificar_proyecto_form

    # Renderiza el template con los datos actualizados
    data['login_form'] = AuthenticationForm()
    data['proyectos'] = proyectos
    return render(request, 'app/inicio.html', data)

