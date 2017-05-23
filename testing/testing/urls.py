"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
#from registro import views
from testing import views
from django.contrib.auth.views import login, logout
from django.shortcuts import redirect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register', include('registro.urls')),
    url(r'^login', login,{'template_name':'registro/login.html'}),
    url(r'^$', views.login_redirect),
    url(r'^logout/', logout, {'template_name': 'registro/logout.html'}),
    url(r'^update_user_info', views.update_user_info),
    url(r'^search_ajax/?$', views.search_ajax),
    url(r'^grupos', views.grupos_usuarios),
    url(r'^nueva_cita', views.new_app),
]
