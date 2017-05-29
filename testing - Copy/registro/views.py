from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from registro.forms import UserRegistration
from django.conf import settings
from django.db import connection
import cx_Oracle
# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegistration()
    return render(request, 'registro/registro.html', {'form':form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        user = request.user.id
        group = request.user.groups.all()
        print(group)
        if not group:
            grupo = ""
        else:
            grupo = str(group[0])
        if grupo == "Doctores":
            basehtml = 'base.html'
        else:
            basehtml = 'basepaciente.html'
        cursor = connection.cursor()
        rawCursor = cursor.connection.cursor()
        cursor.callproc('dientes.get_pkg.get_user', [user, rawCursor])
        res = rawCursor.fetchall()
        for item in res:
            username = item[0]
            name = item[1]
            lastname = item[2]

    return render(request, 'registro/Home.html', {'username':username, 'nombre':name, 'apellido':lastname, 'grupo':grupo, 'basehtml':basehtml})
