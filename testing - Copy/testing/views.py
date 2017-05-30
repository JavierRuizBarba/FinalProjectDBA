from django.shortcuts import redirect, render
import cx_Oracle
from django.db import connection
from testing.forms import update_address, user_groups, nueva_cita_doc, nueva_cita_paciente, nueva_cita_admin, \
    forma_horarios_Inicio, forma_horarios_Fin
from testing.forms import forma_tratamientos, doc_tratamientos_pacientes, admn_tratamientos_pacientes, forma_pagos, \
    forma_tipo_cambio
from testing import settings
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import django_tables2 as tables
from django.db import models
from django_tables2 import RequestConfig, A
from django.utils.html import format_html
from registro import models


def getTable3(cursor):
    exptData = dictfetchall(cursor)
    attrs = {}
    cols = exptData[0]
    for item in cols:
        attrs[str(item)] = tables.Column()
    attrs['class'] = "paleblue"
    myTable = type('myTable', (tables.Table,), attrs)
    return myTable(exptData)


def getTable(cursor, metodo):
    exptData = dictfetchall(cursor)

    class NameTable(tables.Table):
        if metodo == 'tablapacientes':
            ID = tables.Column()
            PACIENTE = tables.Column()
        elif metodo == 'tablacitas':
            ID_CITA = tables.Column()
            PACIENTE = tables.Column()
            DENTISTA = tables.Column()
            FECHA_HORA = tables.Column()
            ACEPTADA = tables.Column()
            DETALLE = tables.Column()
            ASISTIO = tables.Column()
        elif metodo == 'tablatratamientos':
            ID_TRATAMIENTO = tables.Column()
            NOMBRE = tables.Column()
            ESPECIALIDAD = tables.Column()
            COSTO = tables.Column()
        elif metodo == 'tablaabonos':
            ID_ABONOS = tables.Column()
            PACIENTE = tables.Column()
            NOMBRE = tables.Column(verbose_name="TRATAMIENTO")
            FECHA = tables.Column(verbose_name="FECHA LIMITE DE PAGO")
            COSTO = tables.Column()
            PAGADO = tables.Column()

        class Meta:
            attrs = {"class": "table table-hover table-vcenter", "id": "tablamamalona"}

    table = NameTable(exptData)
    return table


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/home')


def update_user_info(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Paciente"
            basehtml = 'bases/basepaciente.html'
        else:
            grupo = str(groups[0])
        if grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
        if request.method == "POST":
            form = update_address(request.POST)
        else:
            form = update_address()
        return render(request, 'pruebamenus.html',
                      {'form': form, 'usuario': request.user.username, 'basehtml': basehtml, 'grupo': grupo})


def grupos_usuarios(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        grupo = str(groups[0])
        if grupo != "Administrador":
            return redirect('/home')
        else:
            basehtml = 'bases/baseadministrador.html'
            if request.method == "POST":
                form = user_groups(request.POST)
            else:
                form = user_groups()
            return render(request, 'user_groups.html', {'form': form, 'basehtml': basehtml})


def new_app(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_address_id', [usuario, rawCursor])
        res = rawCursor.fetchall()
        if not res:
            return redirect('/update_user_info')
        else:
            if not groups:
                grupo = "Pacientes"
            else:
                grupo = str(groups[0])
            if grupo == "Doctores":
                basehtml = 'bases/basedentista.html'
                if request.method == "POST":
                    form = nueva_cita_doc(request.POST)
                else:
                    form = nueva_cita_doc()
            elif grupo == "Pacientes":
                basehtml = 'bases/basepaciente.html'
                if request.method == "POST":
                    form = nueva_cita_paciente(request.POST)
                else:
                    form = nueva_cita_paciente()
            elif grupo == "Administrador":
                basehtml = 'bases/baseadministrador.html'
                if request.method == "POST":
                    form = nueva_cita_admin(request.POST)
                else:
                    form = nueva_cita_admin()
        return render(request, 'nueva_cita.html',
                      {'form': form, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})


def edit_app(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_address_id', [usuario, rawCursor])
        res = rawCursor.fetchall()
        if not res:
            return redirect('/update_user_info')
        else:
            if not groups:
                grupo = "Pacientes"
            else:
                grupo = str(groups[0])
            if grupo == "Doctores":
                basehtml = 'bases/basedentista.html'
                if request.method == "POST":
                    form = nueva_cita_doc(request.POST)
                else:
                    form = nueva_cita_doc()
            elif grupo == "Pacientes":
                basehtml = 'bases/basepaciente.html'
                if request.method == "POST":
                    form = nueva_cita_paciente(request.POST)
                else:
                    form = nueva_cita_paciente()
            elif grupo == "Administrador":
                basehtml = 'baseadinistrador.html'
                if request.method == "POST":
                    form = nueva_cita_admin(request.POST)
                else:
                    form = nueva_cita_admin()
        return render(request, 'editar_cita.html',
                      {'form': form, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})


def todas_citas(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        if grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
            proc = 'dientes.get_pkg.get_cita_doctor'
            cur.callproc(proc, [rawCursor, usuario])
        elif grupo == "Pacientes":
            basehtml = 'bases/basepaciente.html'
            proc = 'dientes.get_pkg.get_cita_p'
            cur.callproc(proc, [rawCursor, usuario])
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
            proc = 'dientes.get_pkg.get_cita_a'
            cur.callproc(proc, [rawCursor])

        res = rawCursor.fetchall()
        if not res:
            citas = None
            return render(request, 'todas_citas.html',
                          {'citas': citas, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})
        else:
            if grupo == "Administrador":
                cur.callproc(proc, [rawCursor])
            else:
                cur.callproc(proc, [rawCursor, usuario])
            tablaFinal = getTable(rawCursor, "tablacitas")
            RequestConfig(request).configure(tablaFinal)

        return render(request, 'todas_citas.html',
                      {'citas': tablaFinal, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})


def citas_confirmar(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        if grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
            proc = 'dientes.get_pkg.get_cita_na_doctor'
            cur.callproc(proc, [rawCursor, usuario])
        elif grupo == "Pacientes":
            basehtml = 'bases/basepaciente.html'
            proc = 'dientes.get_pkg.get_cita_na_p'
            cur.callproc(proc, [rawCursor, usuario])
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
            proc = 'dientes.get_pkg.get_cita_a_na'
            cur.callproc(proc, [rawCursor])

        res = rawCursor.fetchall()
        if not res:
            citas = None
            return render(request, 'citas_confirmar.html',
                          {'citas': citas, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})
        else:
            if grupo == "Administrador":
                cur.callproc(proc, [rawCursor])
            else:
                cur.callproc(proc, [rawCursor, usuario])
            tablaFinal = getTable(rawCursor, "tablacitas")
            RequestConfig(request).configure(tablaFinal)

        return render(request, 'citas_confirmar.html',
                      {'citas': tablaFinal, 'basehtml': basehtml, 'usuario': usuario, 'grupo': grupo})


def horario_vista(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Paciente"
        else:
            grupo = str(groups[0])
        if grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
            if request.method == "POST":
                form1 = forma_horarios_Inicio(request.POST)
                form2 = forma_horarios_Fin(request.POST)
            else:
                form1 = forma_horarios_Inicio()
                form2 = forma_horarios_Fin()
            return render(request, 'horarios.html',
                          {'form1': form1, 'form2': form2, 'usuario': usuario, 'grupo': grupo, 'basehtml': basehtml})
        elif grupo == "Paciente" or grupo == "Administrador":
            return redirect('/home')


def pacientes(request):
    def __init__(self, *args, **kwargs):
        super(pacientes, self).__init__(*args, **kwargs)

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Paciente"
        else:
            grupo = str(groups[0])
        if grupo == "Doctores" or grupo == "Administrador":
            cur = connection.cursor()
            rawCursor = cur.connection.cursor()
            if grupo == "Doctores":
                basehtml = 'bases/basedentista.html'
                doctor = request.user.id
                cur.callproc('dientes.get_pkg.get_pacientes_doctor', [doctor, rawCursor])
                res = rawCursor.fetchall()
                if not res:
                    tablaFinal = None
                    return render(request, 'lista_pacientes.html', {'pacientes': tablaFinal, 'basehtml': basehtml})
                else:
                    cur.callproc('dientes.get_pkg.get_pacientes_doctor', [doctor, rawCursor])
                    tablaFinal = getTable(rawCursor, "tablapacientes")
                    RequestConfig(request).configure(tablaFinal)
                    return render(request, 'lista_pacientes.html', {'pacientes': tablaFinal, 'basehtml': basehtml})
            elif grupo == "Administrador":
                basehtml = 'bases/baseadministrador.html'
                cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
                res = rawCursor.fetchall()
                if not res:
                    tablaFinal = None
                    return render(request, 'lista_pacientes.html', {'pacientes': tablaFinal, 'basehtml': basehtml})
                else:
                    cur.callproc('dientes.get_pkg.get_paciente_cita', [rawCursor])
                    tablaFinal = getTable(rawCursor, "tablapacientes")
                    RequestConfig(request).configure(tablaFinal)
                    return render(request, 'lista_pacientes.html', {'pacientes': tablaFinal, 'basehtml': basehtml})
        else:
            return redirect('/home')


def tratamientos(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        if grupo == "Pacientes":
            basehtml = 'bases/basepaciente.html'
        elif grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])
        res = rawCursor.fetchall()

        if not res:
            tablaFinal = None
        else:
            cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])
            tablaFinal = getTable(rawCursor, "tablatratamientos")
            RequestConfig(request).configure(tablaFinal)

    return render(request, 'lista_tratamientos.html',
                  {'tratamientos': tablaFinal, 'basehtml': basehtml, 'grupo': grupo})


def nuevo_tratamiento(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        if grupo == "Pacientes" or grupo == "Doctores":
            return redirect('/home')
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
            if request.method == "POST":
                form = forma_tratamientos(request.POST)
                if form.is_valid():
                    cur = connection.cursor()
                    nombre = request.POST.get("Nombre")
                    costo = request.POST.get("Costo")
                    especialidad = request.POST.get("Especialidad")
                    cur.callproc('dientes.add_pkg.add_tratamiento', [nombre, costo, especialidad])
                    cur.close()
                    return redirect('/home')
            else:
                form = forma_tratamientos()
            return render(request, 'nuevo_tratamiento.html', {'form': form, 'basehtml': basehtml})


def asignar_tratamientos(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        if grupo == "Pacientes":
            return redirect("/home")
        elif grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
            if request.method == "POST":
                form = doc_tratamientos_pacientes(request.user, request.POST)
            else:
                form = doc_tratamientos_pacientes(request.user)
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
            if request.method == "POST":
                form = admn_tratamientos_pacientes(request.user, request.POST)
            else:
                form = admn_tratamientos_pacientes(request.user)
        return render(request, 'asignar_tratamiento.html', {'form': form, 'usuario': usuario, 'basehtml': basehtml})


def verabonos(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
            basehtml = 'bases/basepaciente.html'
        else:
            grupo = str(groups[0])
            basehtml = 'bases/baseadministrador.html'
        if grupo == "Doctores":
            return redirect('/home')
        else:
            cur = connection.cursor()
            rawCursor = cur.connection.cursor()

            cur.callproc('dientes.get_pkg.get_abono', [usuario, grupo, rawCursor])
            res = rawCursor.fetchall()
            if not res:
                tablaFinal = None
            else:
                cur.callproc('dientes.get_pkg.get_abono', [usuario, grupo, rawCursor])
                tablaFinal = getTable(rawCursor, "tablaabonos")
                RequestConfig(request).configure(tablaFinal)

    return render(request, 'verabonos.html', {'basehtml': basehtml, 'grupo': grupo, 'tablaFinal': tablaFinal})


def hacerpagos(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
            basehtml = 'bases/baseadministrador.html'
        if grupo == "Doctores" or grupo == "Pacientes":
            return redirect('/home')
        else:
            if request.method == "POST":
                form = forma_pagos(request.POST)
            else:
                form = forma_pagos()
        return render(request, 'hacerpagos.html', {'form': form, 'basehtml': basehtml})


def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        userid = request.user.id
        group = request.user.groups.all()
        if not group:
            grupo = "Pacientes"
        else:
            grupo = str(group[0])
        if grupo == "Doctores":
            basehtml = 'bases/basedentista.html'
        elif grupo == "Administrador":
            basehtml = 'bases/baseadministrador.html'
        else:
            basehtml = 'bases/basepaciente.html'
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_address_id', [userid, rawCursor])
        res = rawCursor.fetchall()
        if not res:
            return redirect('/update_user_info')
        else:
            cur.callproc('dientes.get_pkg.get_user', [userid, rawCursor])
            res = rawCursor.fetchall()
            for item in res:
                username = item[0]
                name = item[1]
                lastname = item[2]
            cur.callproc('dientes.get_pkg.get_user_home', [userid, rawCursor])
            res = rawCursor.fetchall()
            for item in res:
                name = item[0]
                email = item[1]
                calle = item[2]
                numero = item[3]
                ciudad = item[4]
                entidad = item[5]
                pais = item[6]
                celular = item[7]
                sexo = item[8]
                tipo_sangre = item[9]
            if grupo == "Doctores":
                cur.callproc('dientes.get_pkg.get_cita_cuenta_d', [rawCursor, userid])
                res = rawCursor.fetchall()
                for item in res:
                    cuenta = item[0]
                cur.callproc('dientes.get_pkg.get_pago_semana_d', [userid, rawCursor])
                res = rawCursor.fetchall()
                for item in res:
                    pagos_d = item[0]
                return render(request, 'registro/Home.html',
                              {'pagos_d':pagos_d,'cuenta':cuenta,'sexo': sexo, 'correo': email, 'calle': calle, 'numero': numero, 'ciudad': ciudad,
                               'entidad': entidad, 'pais': pais, 'celular': celular, 'tipo_sangre': tipo_sangre,
                               'username': username, 'nombre': name, 'apellido': lastname, 'grupo': grupo,
                               'basehtml': basehtml})
            elif grupo == "Administrador":
                cur.callproc('dientes.get_pkg.get_pago_semana', [rawCursor])
                res = rawCursor.fetchall()
                for item in res:
                    pagos_t = item[0]
                cur.callproc('dientes.get_pkg.get_cita_cuenta_a', [rawCursor])
                res = rawCursor.fetchall()
                for item in res:
                    cuenta = item[0]
                return render(request, 'registro/Home.html',
                              {'pagos_t':pagos_t,'cuenta':cuenta,'sexo': sexo, 'correo': email,
                               'calle': calle, 'numero': numero, 'ciudad': ciudad,
                               'entidad': entidad, 'pais': pais, 'celular': celular, 'tipo_sangre': tipo_sangre,
                               'username': username, 'nombre': name, 'apellido': lastname, 'grupo': grupo,
                               'basehtml': basehtml})
            else:
                cur.callproc('dientes.get_pkg.get_next_cita_p', [rawCursor, userid])
                res = rawCursor.fetchall()
                for item in res:
                    name_dent = item[1]
                    fecha = item[2]
                    detalle = item[3]
                cur.callproc('dientes.get_pkg.get_next_abono_p', [userid, rawCursor])
                res = rawCursor.fetchall()
                for item in res:
                    nom_trat = item[1]
                    fecha_ab = item[2]
                    costo = item[3]
                    pago = item[4]

                return render(request, 'registro/Home.html',
                              {'nom_trat': nom_trat, 'fecha_ab': fecha_ab, 'costo': costo, 'pago': pago,
                               'name_dent': name_dent, 'fecha': fecha, 'detalle': detalle, 'sexo': sexo,
                               'correo': email,
                               'calle': calle, 'numero': numero, 'ciudad': ciudad,
                               'entidad': entidad, 'pais': pais, 'celular': celular, 'tipo_sangre': tipo_sangre,
                               'username': username, 'nombre': name, 'apellido': lastname, 'grupo': grupo,
                               'basehtml': basehtml})


def agregartipocambio(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
            basehtml = 'bases/baseadministrador.html'
        if grupo == "Doctores" or grupo == "Pacientes":
            return redirect('/home')
        else:
            if request.method == "POST":
                form = forma_tipo_cambio(request.POST)
                if form.is_valid():
                    cur = connection.cursor()
                    tipocambio = request.POST.get('Tipo_Cambio')
                    print(tipocambio)
                    # cur.callproc('dientes.add_pkg.add_cambio', [tipocambio])
                    # cur.close()
                    return redirect('/home')
            else:
                form = forma_tipo_cambio()
        return render(request, 'agregartipocambio.html', {'form': form, 'basehtml': basehtml})


@csrf_exempt
def search_ajax(request):
    cur = connection.cursor()
    rawCursor = cur.connection.cursor()
    res = ''
    if request.POST.get('tag') == 'getstate':
        id_pais = request.POST.get('pais')
        cur.callproc('dientes.get_pkg.get_estados', [id_pais, rawCursor])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == 'getcity':
        id_estado = request.POST.get('estado')
        cur.callproc('dientes.get_pkg.get_ciudades', [id_estado, rawCursor])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == 'savedir':
        usuario = request.user.id
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        ciudad = request.POST.get('ciudad')
        calle = request.POST.get('calle')
        exterior = request.POST.get('exterior')
        sexo = request.POST.get('sexo')
        celular = request.POST.get('celular')
        blood = request.POST.get('blood')
        cur.callproc('dientes.get_pkg.get_address_id', [usuario, rawCursor])
        addressid = rawCursor.fetchall()
        if not addressid:
            cur.callproc('dientes.add_pkg.add_user_info',
                         [usuario, nombre, apellido, correo, ciudad, calle, exterior, sexo, celular, blood])
        else:
            addressid = addressid[0]
            addressid = addressid[0]
            cur.callproc('dientes.EDIT_pkg.EDIT_user_info',
                         [usuario, nombre, apellido, correo, ciudad, calle, exterior, sexo, celular, blood, addressid])
    elif request.POST.get('tag') == 'populateuser':
        usuario = request.user.id
        cur.callproc('dientes.get_pkg.get_user_info', [usuario, rawCursor])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == "usergroup":
        usuario = request.POST.get('usuario')
        grupo = request.POST.get('grupo')
        cur.callproc('dientes.get_pkg.get_user_group', [usuario, rawCursor])
        grupoid = rawCursor.fetchall()
        if not grupoid:
            print('NOT')
            cur.callproc('dientes.add_pkg.add_user_group', [usuario, grupo])
        else:
            grupoid = grupoid[0]
            grupoid = grupoid[0]
            cur.callproc('dientes.edit_pkg.edit_user_group', [grupoid, grupo])
    elif request.POST.get('tag') == "addcita":
        grupo = request.POST.get('grupo')
        paciente = request.POST.get('paciente')
        fecha = request.POST.get('fecha')
        detalle = request.POST.get('detalle')
        doctor = request.POST.get('doctor')
        citanum = 0
        if grupo == "Doctores" or grupo == "Administrador":
            aceptada = 1
        else:
            aceptada = 0
        cur.callproc('dientes.functionality.cita_rep', [fecha, citanum, rawCursor])
        res = rawCursor.fetchall()
        res = res[0]
        if res[0] == 1:
            cur.callproc('dientes.add_pkg.add_cita', [citanum, paciente, doctor, fecha, detalle, 0, aceptada])
    elif request.POST.get('tag') == "gethorario":
        usuario = request.POST.get('usuario')
        cur.callproc('dientes.get_pkg.get_horario_doc', [usuario, rawCursor])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == "addhorario":
        usuario = request.POST.get('usuario')
        lunes = request.POST.get('lunes')
        martes = request.POST.get('martes')
        miercoles = request.POST.get('miercoles')
        jueves = request.POST.get('jueves')
        viernes = request.POST.get('viernes')
        sabado = request.POST.get('sabado')
        domingo = request.POST.get('domingo')
        existe = request.POST.get('exists')
        horario_id = ''
        if existe == "false":
            cur.callproc('dientes.add_pkg.add_horario',
                         [horario_id, usuario, lunes, martes, miercoles, jueves, viernes, sabado, domingo])
        else:
            cur.callproc('dientes.edit_pkg.edit_horarios',
                         [lunes, martes, miercoles, jueves, viernes, sabado, domingo, 1, usuario])
    elif request.POST.get('tag') == 'dynamichorarios':
        doctor = request.POST.get('doctor')
        dia = request.POST.get('dia')
        cur.callproc('dientes.get_pkg.get_horario_dia', [doctor, dia, rawCursor])
        res = dictfetchall(rawCursor)
        res = res[0]
        res = res[dia.upper()]
    elif request.POST.get('tag') == 'aceptarcita':
        citaid = request.POST.get('citasids')
        values = [int(x) for x in citaid.split(',') if x]
        for item in values:
            cur.callproc('dientes.edit_pkg.edit_cita_aceptar', [item])
    elif request.POST.get('tag') == 'gettreatmentcost':
        cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])
        res = rawCursor.fetchall()
        res2 = []
        for item in res:
            res2.append((item[0], item[3]))
        res = res2
    elif request.POST.get('tag') == 'asignartratamiento':
        id_tratamiento_paciente = 0
        tratamiento = request.POST.get('tratamiento')
        doctor = request.POST.get('doctor')
        paciente = request.POST.get('paciente')
        citas = request.POST.get('citas')
        dia = request.POST.get('dia')
        hora = request.POST.get('hora')
        cur.callproc('dientes.add_pkg.add_tratamiento_paciente',
                     [id_tratamiento_paciente, tratamiento, paciente, doctor, citas, dia, hora])
    elif request.POST.get('tag') == 'populatecita':
        cita = request.POST.get('cita')
        cur.callproc('dientes.get_pkg.get_cita_with_id', [rawCursor, cita])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == 'editcita':
        grupo = request.POST.get('grupo')
        paciente = request.POST.get('paciente')
        fecha = request.POST.get('fecha')
        detalle = request.POST.get('detalle')
        doctor = request.POST.get('doctor')
        citanum = request.POST.get('citanum')
        cur.callproc('dientes.functionality.cita_rep', [fecha, citanum, rawCursor])
        res = rawCursor.fetchall()
        res = res[0]
        if res[0] == 1:
            print(citanum)
            cur.callproc('dientes.edit_pkg.edit_cita', [citanum, paciente, doctor, fecha, detalle, 0, 1, 0])
    elif request.POST.get('tag') == 'pagopaciente':
        doctor = request.POST.get('doctor')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc('dientes.get_pkg.get_pacientes_doctor', [doctor, rawCursor])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == 'pagotratamiento':
        paciente = request.POST.get('paciente')
        cur.callproc('dientes.get_pkg.get_tratamiento_paciente', [rawCursor, paciente])
        res = rawCursor.fetchall()
    elif request.POST.get('tag') == 'addpago':
        doctor = request.POST.get('doctor')
        paciente = request.POST.get('paciente')
        tratamiento = request.POST.get('tratamiento')
        total = request.POST.get('total')
        tipopago = request.POST.get('tipopago')
        pago = 0
        cur.callproc('dientes.add_pkg.add_pagos', [pago, doctor, paciente, total, tipopago, tratamiento, rawCursor])
        res = rawCursor.fetchall()
        res = res[0]
        res = res[0]
    elif request.POST.get('tag') == 'addtipocambio':
        tipocambio = request.POST.get('tipocambio')
        cur.callproc('dientes.add_pkg.add_cambio', [tipocambio])

    return HttpResponse(json.dumps(res))


def perfil(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_address_id', [usuario, rawCursor])
        res = rawCursor.fetchall()
        if not res:
            return redirect('/update_user_info')
        else:
            if not groups:
                grupo = "Pacientes"
            else:
                grupo = str(groups[0])
            if grupo == "Doctores":
                basehtml = 'bases/basedentista.html'
            elif grupo == "Pacientes":
                basehtml = 'bases/basepaciente.html'
            elif grupo == "Administrador":
                basehtml = 'bases/baseadministrador.html'
        cur.callproc('dientes.get_pkg.get_user', [usuario, rawCursor])
        res = rawCursor.fetchall()
        for item in res:
            username = item[0]
            name = item[1]
            lastname = item[2]
        cur.callproc('dientes.get_pkg.get_user_home', [usuario, rawCursor])
        res = rawCursor.fetchall()
        for item in res:
            name = item[0]
            email = item[1]
            calle = item[2]
            numero = item[3]
            ciudad = item[4]
            entidad = item[5]
            pais = item[6]
            celular = item[7]
            sexo = item[8]
            tipo_sangre = item[9]

    return render(request, 'perfil.html',
                  {'sexo': sexo, 'correo': email, 'calle': calle, 'numero': numero, 'ciudad': ciudad,
                   'entidad': entidad, 'pais': pais, 'celular': celular, 'tipo_sangre': tipo_sangre,
                   'username': username, 'nombre': name, 'apellido': lastname, 'grupo': grupo, 'basehtml': basehtml})


    # return render(request,'search_ajax.html')
