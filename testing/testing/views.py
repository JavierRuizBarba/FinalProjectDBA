from django.shortcuts import redirect, render
import cx_Oracle
from django.db import connection
from testing.forms import update_address, user_groups, nueva_cita_doc, nueva_cita_paciente, nueva_cita_admin, forma_horarios_Inicio, forma_horarios_Fin
from testing.forms import forma_tratamientos, tratamientos_pacientes
from testing import settings
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import django_tables2 as tables
from django.db import models
from django_tables2 import RequestConfig, A
from django.utils.html import format_html
from registro import  models

def getTable3(cursor):
    exptData = dictfetchall(cursor)
    attrs = {}
    cols=exptData[0]
    for item in cols:
        attrs[str(item)] = tables.Column()
    attrs['class'] = "paleblue"
    myTable = type('myTable', (tables.Table,), attrs)
    return myTable(exptData)

def getTable(cursor, metodo):
    exptData = dictfetchall(cursor)
    class NameTable(tables.Table):
        if metodo == 'tablapacientes':
            PACIENTE_ID = tables.Column()
            PACIENTE = tables.Column()
        elif metodo == 'tablacitas':
            ID_CITA = tables.Column()
            PACIENTE = tables.Column()
            DENTISTA = tables.Column()
            FECHA_HORA = tables.LinkColumn('editar_cita')
            ACEPTADA = tables.Column()
            DETALLE = tables.Column()
            ASISTIO = tables.Column()
        elif metodo == 'tablatratamientos':
            ID_TRATAMIENTO = tables.Column()
            NOMBRE = tables.Column()
            ESPECIALIDAD = tables.Column()
            COSTO = tables.Column()
			
        class Meta:
            attrs={"class":"paleblue", "id":"tablamamalona"}

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
        return redirect('/register/home')

def update_user_info(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Paciente"
        else:
            grupo = str(groups[0])
        if request.method == "POST":
            form = update_address(request.POST)
        else:
            form = update_address()
        return render(request, 'pruebamenus.html', {'form':form, 'usuario':request.user.username, 'grupo':grupo})

def grupos_usuarios(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        grupo = str(groups[0])
        if grupo != "Administrador":
            return redirect('/register/home')
        else:
            if request.method == "POST":
                form = user_groups(request.POST)
            else:
                form = user_groups()
            return render(request, 'user_groups.html', {'form':form})

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
                grupo="Paciente"
            else:
                grupo = str(groups[0])
            if grupo == "Doctores":
                basehtml = 'base.html'
                if request.method == "POST":
                    form = nueva_cita_doc(request.POST)
                else:
                    form = nueva_cita_doc()
            elif grupo == "Paciente":
                basehtml = 'basepaciente.html'
                if request.method == "POST":
                    form = nueva_cita_paciente(request.POST)
                else:
                    form = nueva_cita_paciente()
            elif grupo == "Administrador":
                basehtml = 'base.html'
                if request.method == "POST":
                    form = nueva_cita_admin(request.POST)
                else:
                    form = nueva_cita_admin()
        return render(request, 'nueva_cita.html', {'form':form, 'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})

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
                grupo="Paciente"
            else:
                grupo = str(groups[0])
            if grupo == "Doctores":
                basehtml = 'base.html'
                if request.method == "POST":
                    form = nueva_cita_doc(request.POST)
                else:
                    form = nueva_cita_doc()
            elif grupo == "Paciente":
                basehtml = 'basepaciente.html'
                if request.method == "POST":
                    form = nueva_cita_paciente(request.POST)
                else:
                    form = nueva_cita_paciente()
            elif grupo == "Administrador":
                basehtml = 'base.html'
                if request.method == "POST":
                    form = nueva_cita_admin(request.POST)
                else:
                    form = nueva_cita_admin()
        return render(request, 'editar_cita.html', {'form':form, 'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})

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
            basehtml = 'base.html'
            proc = 'dientes.get_pkg.get_cita_doctor'

        elif grupo == "Pacientes":
            basehtml = 'basepaciente.html'
            proc = 'dientes.get_pkg.get_cita_p'

        cur.callproc(proc, [rawCursor, usuario])
        res = rawCursor.fetchall()
        if not res:
            citas = None
            return render(request, 'todas_citas.html', {'citas':citas,'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})
        else:
            cur.callproc(proc, [rawCursor, usuario])
            tablaFinal = getTable(rawCursor, "tablacitas")
            RequestConfig(request).configure(tablaFinal)


        return render(request, 'todas_citas.html', {'citas':tablaFinal, 'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})

def citas_confirmar(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo = "Pacientes"
        else:
            grupo = str(groups[0])
        if grupo == "Doctores":
            basehtml = 'base.html'
            proc = 'dientes.get_pkg.get_cita_na_doctor'
        elif grupo == "Pacientes":
            basehtml = 'basepaciente.html'
            proc = 'dientes.get_pkg.get_cita_na_p'

        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc(proc, [rawCursor, usuario])

        tablaFinal = getTable(rawCursor, "tablacitas")
        RequestConfig(request).configure(tablaFinal)
    return render(request, 'citas_confirmar.html', {'citas':tablaFinal, 'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})

def horario_vista(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.id
        groups = request.user.groups.all()
        if not groups:
            grupo="Paciente"
        else:
            grupo = str(groups[0])
        if grupo == "Doctores":
            basehtml = 'base.html'
            if request.method == "POST":
                form1 = forma_horarios_Inicio(request.POST)
                form2 = forma_horarios_Fin(request.POST)
            else:
                form1 = forma_horarios_Inicio()
                form2 = forma_horarios_Fin()
            return render(request, 'horarios.html', {'form1': form1, 'form2': form2, 'usuario': usuario, 'grupo': grupo, 'basehtml': basehtml})
        elif grupo == "Paciente":
            return redirect('/register/home')

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
            basehtml = 'base.html'
            cur = connection.cursor()
            rawCursor = cur.connection.cursor()
            if grupo == "Doctores":
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
                    return render(request, 'lista_pacientes.html', {'pacientes':tablaFinal, 'basehtml':basehtml})
        else:
            return redirect('/register/home')

def tratamientos(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        groups = request.user.groups.all()
        if not groups:
            grupo = "Paciente"
        else:
            grupo = str(groups[0])

        basehtml = 'base.html'
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
        if request.method == "POST":
            form = forma_tratamientos(request.POST)
        else:
            form = forma_tratamientos()

    return render(request, 'lista_tratamientos.html', {'tratamientos':tablaFinal, 'basehtml':basehtml, 'grupo': grupo, 'form':form})

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
            return redirect("/register/home")
        else:
            if request.method == "POST":
                form = tratamientos_pacientes(request.user, request.POST)
            else:
                form = tratamientos_pacientes(request.user)
        return render(request, 'asignar_tratamiento.html', {'form':form, 'usuario':usuario})



@csrf_exempt
def search_ajax(request):
    if request.POST.get('tag') == 'getstate':
        id_pais = request.POST.get('pais')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc('dientes.get_pkg.get_estados', [id_pais, rawCursor])

        res=rawCursor.fetchall()
    elif request.POST.get('tag') == 'getcity':
        id_estado = request.POST.get('estado')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

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
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_address_id', [usuario, rawCursor])
        addressid = rawCursor.fetchall()
        res = ''
        if not addressid:
            cur.callproc('dientes.add_pkg.add_user_info', [usuario, nombre, apellido, correo, ciudad, calle, exterior, sexo, celular, blood])
        else:
            addressid = addressid[0]
            addressid = addressid[0]
            cur.callproc('dientes.EDIT_pkg.EDIT_user_info',
                         [usuario, nombre, apellido, correo, ciudad, calle, exterior, sexo, celular, blood, addressid])

    elif request.POST.get('tag') == 'populateuser':
        usuario = request.user.id
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_user_info', [usuario, rawCursor])
        res = rawCursor.fetchall()

    elif request.POST.get('tag') == "usergroup":
        usuario = request.POST.get('usuario')
        grupo = request.POST.get('grupo')

        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        res=''
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
        citanum = ''
        if grupo == "Doctores" or grupo == "Administrador":
            aceptada = 1
        else:
            aceptada = 0
        cur = connection.cursor()
        res=''

        cur.callproc('dientes.add_pkg.add_cita', [citanum, paciente, doctor, fecha, detalle, 0, aceptada])

    elif request.POST.get('tag') == "gethorario":
        usuario = request.POST.get('usuario')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

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

        res=''
        cur = connection.cursor()
        horario_id = ''
        print(existe)
        if existe == "false":
            print('agregar')
            cur.callproc('dientes.add_pkg.add_horario', [horario_id, usuario, lunes, martes, miercoles, jueves, viernes, sabado, domingo])
        else:
            print('modify')
            cur.callproc('dientes.edit_pkg.edit_horarios', [lunes, martes, miercoles, jueves, viernes, sabado, domingo, 1, usuario])

    elif request.POST.get('tag') == 'dynamichorarios':
        doctor = request.POST.get('doctor')
        dia = request.POST.get('dia')

        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.get_pkg.get_horario_dia', [doctor, dia, rawCursor])

        res=dictfetchall(rawCursor)

        res = res[0]
        res = res[dia.upper()]

    elif request.POST.get('tag') == 'aceptarcita':
        cur = connection.cursor()
        citaid = request.POST.get('citasids')
        res=''
        values = [int(x) for x in citaid.split(',') if x]
        for item in values:
            cur.callproc('dientes.edit_pkg.edit_cita_aceptar', [item])

    elif request.POST.get('tag') == 'gettreatmentcost':
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc('dientes.get_pkg.get_tratamientos', [rawCursor])

        res=rawCursor.fetchall()
        res2=[]

        for item in res:
            res2.append((item[0],item[3]))
        res = res2

    elif request.POST.get('tag') == 'asignartratamiento':
        cur = connection.cursor()
        id_tratamiento_paciente=0
        tratamiento = request.POST.get('tratamiento')
        doctor = request.POST.get('doctor')
        paciente = request.POST.get('paciente')
        citas = request.POST.get('citas')
        dia = request.POST.get('dia')
        hora = request.POST.get('hora')
        res = ''
        cur.callproc('dientes.add_pkg.add_tratamiento_paciente', [id_tratamiento_paciente, tratamiento, paciente, doctor, citas, dia, hora])

    return HttpResponse(json.dumps(res))



    #return render(request,'search_ajax.html')
