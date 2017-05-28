from django import forms
from django.db import models
from django.forms import ModelForm
from django.db import connection
from functools import partial

import cx_Oracle

DateInput = partial(forms.DateInput, {'class':'datepicker'})

class update_address(forms.Form):
    def __init__(self, *args, **kwargs):
        super(update_address, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_country', [rawCursor])
    res = rawCursor.fetchall()

    Nombre = forms.CharField(max_length=100, required = True)

    Apellido = forms.CharField(max_length=100, required = True)

    Correo = forms.CharField(max_length=100, required=True)

    Paises = forms.ChoiceField(choices=res, required = True)

    Estados = forms.ChoiceField(required=True)

    Ciudades = forms.ChoiceField(required=True)

    Direccion = forms.CharField(max_length=100, required=True)

    Numero_Exterior = forms.IntegerField(required=True, max_value=10000)

    Sexo = forms.ChoiceField(choices={('M','Masculino'),('F', 'Femenino')}, required=True)

    Celular = forms.IntegerField(max_value=10000000000, required=True)

    cur.callproc('dientes.get_pkg.get_blood',[rawCursor])
    res=rawCursor.fetchall()

    Tipo_Sangre = forms.ChoiceField(choices=res, required=True)

class user_groups(forms.Form):
    def __init__(self, *args, **kwargs):
        super(user_groups, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_usernames', [rawCursor])

    res = rawCursor.fetchall()

    Usuarios = forms.ChoiceField(choices=res, required=True)

    cur.callproc('dientes.get_pkg.get_groups', [rawCursor])

    res = rawCursor.fetchall()

    Grupos = forms.ChoiceField(choices=res,required=True)

class nueva_cita_doc(forms.Form):
    def __init__(self, *args, **kwargs):
        super(nueva_cita_doc, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
    res = rawCursor.fetchall()
    res2 = []
    i=0
    for item in res:
        nombre = item[1] + ' ' + item[2]
        res2.append((item[0], nombre))


    Pacientes = forms.ChoiceField(choices=res2, required=True)
    Detalle = forms.CharField(widget=forms.Textarea, required = True)
    Fecha = forms.DateField(widget= DateInput(), required=True)
    Hora = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}), required=True)

class nueva_cita_paciente(forms.Form):
    def __init__(self, *args, **kwargs):
        super(nueva_cita_paciente, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_doctor', [rawCursor])

    res = rawCursor.fetchall()
    res2 = []
    i=0
    for item in res:
        nombre = item[1] + ' ' + item[2]
        res2.append((item[0], nombre))

    Doctores = forms.ChoiceField(choices=res2, required=True)
    Detalle = forms.CharField(widget=forms.Textarea, required = True)
    Fecha = forms.DateField(widget=DateInput(), required=True)
    Hora = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}), required=True)

class nueva_cita_admin(forms.Form):
    def __init__(self, *args, **kwargs):
        super(nueva_cita_admin, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_doctor', [rawCursor])

    res = rawCursor.fetchall()
    res2 = []
    i = 0
    for item in res:
        nombre = item[1] + ' ' + item[2]
        res2.append((item[0], nombre))

    Doctores = forms.ChoiceField(choices=res2, required=True)

    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
    res = rawCursor.fetchall()
    res2 = []
    i = 0
    for item in res:
        nombre = item[1] + ' ' + item[2]
        res2.append((item[0], nombre))
    Pacientes = forms.ChoiceField(choices=res2, required=True)
    Detalle = forms.CharField(widget=forms.Textarea, required=True)
    Fecha = forms.DateField(widget=DateInput(), required=True)
    Hora = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)

class forma_horarios_Inicio(forms.Form):
    Lunes_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Martes_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Miercoles_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Jueves_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Viernes_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Sabado_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Domingo_Inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)

class forma_horarios_Fin(forms.Form):
    Lunes_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Martes_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Miercoles_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Jueves_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Viernes_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Sabado_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
    Domingo_Fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)
