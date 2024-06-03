from django import forms
from django.contrib.auth.models import User
from .models import Proyecto

class FormCrearProyecto(forms.ModelForm):
    profesores = forms.ModelChoiceField(queryset=User.objects.none(), required=False, label='Profesor Patrocinador')

    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'tema', 'patrocinio', 'profesores')
        labels = {
            'nombre_proyecto': 'Nombre Proyecto',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormCrearProyecto, self).__init__(*args, **kwargs)
        if user and not user.groups.filter(name='Profesor').exists():
            self.fields['patrocinio'].widget = forms.HiddenInput()
            self.fields['profesores'].widget = forms.HiddenInput()
        self.fields['profesores'].queryset = User.objects.filter(groups__name='Profesor')
        self.user = user

    def save(self, commit=True):
        proyecto = super().save(commit=True)
        if self.user:
            proyecto.estudiante = self.user
        if commit:
            proyecto.save()
        return proyecto

class ProyectoPatrocinioForm(forms.Form):
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.none(), label='Seleccione un proyecto')
    patrocinar = forms.BooleanField(required=False, label='¿Desea patrocinar este proyecto?')

    def __init__(self, *args, **kwargs):
        profesor = kwargs.pop('profesor', None)
        super(ProyectoPatrocinioForm, self).__init__(*args, **kwargs)
        self.fields['proyecto'].queryset = Proyecto.objects.all()
        self.profesor = profesor

    def save(self):
        proyecto = self.cleaned_data['proyecto']
        patrocinar = self.cleaned_data['patrocinar']
        if patrocinar:
            proyecto.profesor_patrocinador = self.profesor
            proyecto.save()
        return proyecto

class ProyectoModificarForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto', 'tema', 'patrocinio']

    def __init__(self, *args, **kwargs):
        super(ProyectoModificarForm, self).__init__(*args, **kwargs)
        self.fields['patrocinio'].widget.attrs['disabled'] = 'disabled'
