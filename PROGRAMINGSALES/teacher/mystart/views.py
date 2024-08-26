from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



from .models import User,Students_programs,TypeProgram

# Create your views here.


def index(request):
    if request.method == 'POST':
        student = request.POST["student"]
        pas = request.POST["pas"]
        if not student or not pas:
            return render(request, "start.html",{"alert":"Complete todos los campos"})
        xuser = authenticate(username= student, password=pas)
        if xuser is not None:
            status = User.objects.get(username= xuser)
            if status.is_active:
                login(request,xuser)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, "start.html",{"message":"Acceso Restringido"} )       
        else:
            return render(request, "start.html",{"message":"Credenciales Invalidas"} )
    else:
        userx = request.user
        if userx.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        elif userx.is_anonymous:
            return render(request, "start.html" )



@login_required
def logoutV(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def home(request):
    print("inicio")
    try:
        code = Students_programs.objects.get(userx = request.user, status= True)
        print("acepto")
        return render(request, "home.html",{"enroll": code})
    except ObjectDoesNotExist:
        print("expulso")
        return render(request, "home.html")



@login_required
def createusers(request):
    print(request.user.is_superuser)
    if request.method == 'POST':
        name = request.POST["newuser"]
        pas  = request.POST["newpass"]
        email = request.POST["newemail"]
        if not name or not pas or not email:
            return render(request, "admin.html",{"message":"Datos incompletos"})
        try:
            checkuser = User.objects.get(username=name)
            if checkuser:
                return render(request, "admin.html",{"message":"Usa otro nombre de usuario"})
        except ObjectDoesNotExist:
            newuser = User.objects.create_user(username=name,password=pas, email=email)
            newuser.save()
            return render(request, "admin.html",{"message":"Created"})
    else:
        return render(request, "admin.html")
    
        #send email by 
        #email_user(subject, message, from_email=None, **kwargs)



@login_required
def lessons(request):
    userx =request.user
    return render(request, "lessons1.html")

def pruebas(request):
    ...
def options(request):
    ...