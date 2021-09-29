"""adocao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import index, home, create, store, detail, edit, update, remove
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adotar/', home, name='home'),
    path('', index),
    path('adotar/detalhes/<int:id>/', detail),
    path('adotar/detalhes/', detail),
    path('adotar/editar/<int:id>/', edit, name='edit'),
    path('adotar/atualizar/<int:id>/', update, name='update'),
    path('adotar/remover/<int:id>/', remove, name='remove'),
    path('adotar/cadastro/', create),
    path('adotar/cadastrar', store)
]
