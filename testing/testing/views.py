from django.shortcuts import redirect, render
import cx_Oracle
from django.db import connection
from testing.forms import update_address, user_groups, nueva_cita_doc#, nueva_cita_paciente
from testing import settings
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/register/home')

def update_user_info(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == "POST":
            form = update_address(request.POST)
        else:
            form = update_address()
        return render(request, 'pruebamenus.html', {'form':form, 'usuario':request.user.username})

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
        #elif grupo == "Administrador":
         #   if request.method == "POST":
          #      form = nueva_cita_admin(request.POST)
           # else:
            #    form = nueva_cita_admin()
        #else:
         #   if request.method == "POST":
          #      form = nueva_cita_paciente(request.POST)
           # else:
            #    form = nueva_cita_paciente()
        return render(request, 'nueva_cita.html', {'form':form, 'basehtml':basehtml, 'usuario':usuario, 'grupo':grupo})

@csrf_exempt
def search_ajax(request):
    if request.POST.get('tag') == 'getstate':
        id_pais = request.POST.get('pais')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc('dientes.get_estados', [id_pais, rawCursor])

        res=rawCursor.fetchall()
    elif request.POST.get('tag') == 'getcity':
        id_estado = request.POST.get('estado')
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()

        cur.callproc('dientes.get_ciudades', [id_estado, rawCursor])

        res = rawCursor.fetchall()

    elif request.POST.get('tag') == 'savedir':
        print('Save')
        usuario = request.user.id
        celular = request.POST.get('celular')
        sexo = request.POST.get('sexo')
        calle = request.POST.get('calle')
        exterior = request.POST.get('exterior')
        ciudad = request.POST.get('ciudad')
        blood = request.POST.get('blood')

        cur = connection.cursor()
        res=''
        cur.callproc('dientes.creardireccion', [usuario, celular, ciudad, exterior, calle, sexo, blood])

    elif request.POST.get('tag') == 'updatedir':
        print('Update')
        usuario = request.user.id
        celular = request.POST.get('celular')
        sexo = request.POST.get('sexo')
        calle = request.POST.get('calle')
        exterior = request.POST.get('exterior')
        ciudad = request.POST.get('ciudad')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        blood = request.POST.get('blood')

        cur = connection.cursor()
        res=''
        cur.callproc('dientes.actualizardireccion', [usuario, nombre, apellido, correo, celular, ciudad, exterior, calle, sexo, blood])

    elif request.POST.get('tag') == 'populateuser':
        usuario = request.user.id
        cur = connection.cursor()
        rawCursor = cur.connection.cursor()
        cur.callproc('dientes.getuserinfo', [usuario, rawCursor])
        res = rawCursor.fetchall()

    elif request.POST.get('tag') == "usergroup":
        usuario = request.POST.get('usuario')
        grupo = request.POST.get('grupo')

        cur = connection.cursor()
        res=''
        cur.callproc('dientes.add_user_group', [usuario, grupo])

    elif request.POST.get('tag') == "addcita":
        grupo = request.POST.get('grupo')
        paciente = request.POST.get('paciente')
        fecha = request.POST.get('fecha')
        detalle = request.POST.get('detalle')
        doctor = request.POST.get('doctor')
        citanum = ''
        if grupo == "Doctores":
            aceptada = 1
        else:
            aceptada = 0
        cur = connection.cursor()
        res=''

        cur.callproc('dientes.add_pkg.add_cita', [citanum, paciente, doctor, fecha, detalle, 0, aceptada])

    return HttpResponse(json.dumps(res))

    #return render(request,'search_ajax.html')
