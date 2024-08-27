from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist

from myapp.models import *

# Create your views here.


def loginV(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        userx = request.POST["myuser"]
        pas = request.POST["codigo"]
        if not userx or not pas:
            return HttpResponseRedirect(reverse('loginV'))
        there = authenticate(username=userx,password=pas)
        if there is not None:
            login(request,there)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('loginV'))

def registro(request):
    if request.method == 'POST':
        usernew = request.POST['newuser']
        code = request.POST['newcodigo']
        autho = request.POST['autho']
        if not usernew or not code or not autho:
            return HttpResponseRedirect(reverse('loginV'))
        if autho == '1017':
            new = User.objects.create_user(username=usernew, password=code)
            new.save()
            return render(request,"login.html", {"message":"Creado"})

        return HttpResponseRedirect(reverse('loginV'))





@login_required
def index(request):
    if request.method == 'GET':
        #libros = biblia.objects.all()
        data = serializers.serialize("json", biblia.objects.all())
        libros = json.loads(data)
        conjunto=[]
        for libro in libros:
            conjunto.append(libro["fields"]["libro"])
        return render(request, "index.html",{"libros":conjunto})
    else:
        return HttpResponseRedirect(reverse('loginV'))

@login_required
def logoutV(request):
    logout(request)
    return render(request, "login.html")

@login_required
def create(request):
    if request.method == 'POST':
        question = request.POST["pregunta1"].lstrip().rstrip()
        respuesta1 = request.POST["respuesta1"]
        librito = request.POST["libo"]
        cap = request.POST["cap"]
        ver = request.POST["ver"]
        if not question or not librito or not cap or not ver:
                return HttpResponseRedirect('index')
        try:
            pregunta.objects.get(pregunta=question)
            return render(request,"index.html", {"message":"La pregunta no se agregó.Ya estaba"})
        except ObjectDoesNotExist:
            libroobject= biblia.objects.get(libro=librito)
            new= pregunta.objects.create(user=User.objects.get(username=request.user), pregunta = question,respuesta= respuesta1, capitulo=cap, versiculo=ver)
            new.libro_id.add(libroobject)
            return HttpResponseRedirect('index')
        

@login_required
def guardados(request):
    if request.method == 'POST':
        libro = request.POST["search_libro"]
        cap = request.POST["cap"]
        if not cap:
            cap = 1
        try:
            libro_id = biblia.objects.get(libro=libro)
            finder = pregunta.objects.filter(libro_id=libro_id.pk,capitulo=cap)
            bible= biblia.objects.all()
            return render(request,"tabla.html",{"info":finder,"bible":bible})
        except ObjectDoesNotExist:
            return render(request,"tabla.html",{"info":finder,"bible":bible, "message":"No encontrada"})   
    else:
        questions = pregunta.objects.all().order_by("libro_id","capitulo")
        bible= biblia.objects.all()
        return render(request,"tabla.html",{"info":questions,"bible":bible})
        


