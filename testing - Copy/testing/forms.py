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

    Nombre = forms.CharField(max_length=100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class':'form-control'}))

    Apellido = forms.CharField(max_length=100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class':'form-control'}))

    Correo = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Correo', 'class':'form-control'}))

    Paises = forms.ChoiceField(choices=res, required = True, widget=forms.Select(attrs={ 'class':'form-control'}))

    Estados = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': 'Estado','class':'form-control'}))

    Ciudades = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': 'Estado','class':'form-control'}))

    Direccion = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Dirección', 'class':'form-control'}))

    Numero_Exterior = forms.IntegerField(required=True, max_value=10000, widget=forms.TextInput(attrs={'placeholder': 'Numero Exterior', 'class':'form-control'}))

    Sexo = forms.ChoiceField(choices={('M','Masculino'),('F', 'Femenino')}, required=True, widget=forms.Select(attrs={'placeholder': 'Sexo','class':'form-control'}))

    Celular = forms.IntegerField(max_value=10000000000, required=True, widget=forms.TextInput(attrs={'placeholder': 'Celular', 'class':'form-control'}))

    cur.callproc('dientes.get_pkg.get_blood',[rawCursor])
    res=rawCursor.fetchall()

    Tipo_Sangre = forms.ChoiceField(choices=res, required=True, widget=forms.Select(attrs={'placeholder': 'Tipo de Sangre','class':'form-control'}))


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


    Pacientes = forms.ChoiceField(choices=res, required=True, widget=forms.Select(attrs={'placeholder': 'Paciente', 'class':'form-control'}))
    Detalle = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Detalle', 'class':'form-control'}), required = True)
    Fecha = forms.DateField(widget=DateInput(), required=True)
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

    Doctores = forms.ChoiceField(choices=res2, required=True, widget=forms.Select(attrs={'placeholder': 'Doctor','class':'form-control'}))
    Detalle = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Detalle', 'class':'form-control', 'rows':'5'}), required = True)
    Fecha = forms.DateField(widget= DateInput(), required=True)
    Hora = forms.DateField(widget= forms.DateInput(attrs={'class':'timepicker'}), required=True)


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

    Doctores = forms.ChoiceField(choices=res2, required=True, widget=forms.Select(attrs={'placeholder': 'Doctor','class':'form-control'}))

    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
    res = rawCursor.fetchall()

    Pacientes = forms.ChoiceField(choices=res, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    Detalle = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Detalle', 'class':'form-control', 'rows':'5'}), required = True)
    Fecha = forms.DateField(widget= DateInput(), required=True)
    Hora = forms.DateField(widget= forms.DateInput(attrs={'class':'timepicker'}), required=True)

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

class forma_tratamientos(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forma_tratamientos, self).__init__(*args, **kwargs)
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_especialidades', [rawCursor])
    res = rawCursor.fetchall()

    Nombre = forms.CharField(max_length=100, required = True)

    Especialidad = forms.ChoiceField(choices=res, required = True)

    Costo = forms.CharField(required=True)

class doc_tratamientos_pacientes(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(doc_tratamientos_pacientes, self).__init__(*args, **kwargs)

    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
    res = rawCursor.fetchall()

    Pacientes = forms.ChoiceField(choices=res, required=True)

    cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])

    res = rawCursor.fetchall()
    res2 = []

    for item in res:
        res2.append((item[0],item[1]))
    Tratamientos = forms.ChoiceField(choices=res2, required = True)
    Costo = forms.DecimalField(disabled=True, required=True)
    Citas = forms.IntegerField(required=True)
    dias = [(0,'Seleccione un día'),('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes'), ('Sabado','Sabado'), ('Domingo','Domingo')]
    Dia = forms.ChoiceField(choices=dias)
    Hora_Preferencia = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)

class admn_tratamientos_pacientes(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(doc_tratamientos_pacientes, self).__init__(*args, **kwargs)

    cur = connection.cursor()
    rawCursor = cur.connection.cursor()

    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
    res = rawCursor.fetchall()

    Pacientes = forms.ChoiceField(choices=res, required=True)

    cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])

    res = rawCursor.fetchall()
    res2 = []

    for item in res:
        res2.append((item[0],item[1]))
    Tratamientos = forms.ChoiceField(choices=res2, required = True)
    Costo = forms.DecimalField(disabled=True, required=True)
    Citas = forms.IntegerField(required=True)
    dias = [(0,'Seleccione un día'),('Lunes','Lunes'), ('Martes','Martes'), ('Miercoles','Miercoles'), ('Jueves','Jueves'), ('Viernes','Viernes'), ('Sabado','Sabado'), ('Domingo','Domingo')]
    Dia = forms.ChoiceField(choices=dias)
    Hora_Preferencia = forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}), required=True)

class forma_pagos(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forma_pagos, self).__init__(*args, **kwargs)

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
    Pacientes = forms.ChoiceField(required=True)
    Tratamiento = forms.ChoiceField(required=True)
    Total = forms.FloatField(required=True)

    cur.callproc('dientes.get_pkg.get_tipo_pago', [rawCursor])
    res = rawCursor.fetchall()

    Tipo_Pago = forms.ChoiceField(choices=res, required=True)

class forma_tipo_cambio(forms.Form):
    Tipo_Cambio = forms.DecimalField(required=True, decimal_places=2)