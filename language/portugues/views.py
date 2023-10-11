from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
import random
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
import json

import os
from django.conf import settings
from django.http import HttpResponse, Http404

import random
import re



from datetime import datetime
from .models import User,Profile,Approval,Lessons,Exams,Tester,Tips,Whyter,Reactions

from django.core.paginator import Paginator
from django.shortcuts import render





@login_required
def index(request):
    if request.method == 'POST':
        tip = request.POST['tip']
        if len(tip)== 0:
            return HttpResponseRedirect(reverse('index'))
        Tips.objects.create(tipers=tip,created=datetime.now())
        return HttpResponseRedirect(reverse('index'))
    else:
        try:
            tips = Tips.objects.all().order_by('-created')
        except ObjectDoesNotExist:
            tips = None
        try:
            whytext = Whyter.objects.get(userx = request.user)

        except ObjectDoesNotExist:
            whytext = False


        paginator = Paginator(tips, 3) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "portugues/index.html", {"page_obj": page_obj,"whytext":whytext})


def view_login(request):
    if request.method == 'POST':
        name = request.POST['userx']
        passw = request.POST['passw']
        if not name or not passw:
            return render(request, "portugues/login.html",{"message":"REVER AS INFORMAÇÕES"})

        userx = authenticate(request,username=name, password=passw)
        if userx is not None:
            login(request, userx)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "portugues/login.html",{"message":"REVER AS INFORMAÇÕES"})
    else:
        return render(request, "portugues/login.html")
    
@login_required    
def view_register(request):
    try:
        userchecker = User.objects.all()
        return render(request, "portugues/register.html",{"info":userchecker})
    except ObjectDoesNotExist:
        return render(request, "portugues/register.html")

@login_required
def view_logout(request):
    logout(request)
    return HttpResponseRedirect('login')


@login_required
#Me falata comprobar email.
def saver(request):
    if request.method != 'POST':
        return HttpResponseRedirect('view_register')
    userx= request.user
    if userx.is_superuser:
        mailt= request.POST['emailx']
        username= request.POST['username']
        if not mailt or not username:
            return render(request, "portugues/register.html",{"messagem": "Precisa verificar informações"})
        letter = ["P","O","R","T","U","G","U","E","S"]
        letcode = random.choice(letter)
        code = random.randint(1000,10000)

        codex = letcode + str(code)

        try:
            newUser =User.objects.create_user(username,mailt,codex)
            try:
                tylesson = Lessons.objects.get(number_lesson=1)
                lessn = Approval.objects.create(lessonUser=newUser,bool_lesson_app = True)
                lessn.number_lesson.add(tylesson)
                return render(request, "portugues/register.html",{"messagem": f"Código único de acesso: {codex}"})
            except ObjectDoesNotExist:
                return render(request, "portugues/register.html",{"messagem": f"Código único de acesso: {codex}"})

                
        except IntegrityError:
            return render(request, "portugues/register.html",{"messagem": "Nome de usuário já utilizado"})
        
        
    else:
        return HttpResponseRedirect('view_register')


    
@login_required
def deregister(request):
    if request.method != 'POST':
        return render(request, "portugues/register.html",{"messagem": "Error"})
    
    deuser = request.POST['deuser']
    try:
        finder = User.objects.get(username=deuser)
        finder.delete()
        return render(request, "portugues/register.html",{"messagem": "Usuário excluído"})
    except ObjectDoesNotExist:
        return render(request, "portugues/register.html",{"messagem": "Usar usuários registrados"})

@login_required
def superus(request):
    if request.method != 'POST':
        return render(request, "portugues/register.html",{"messagel": "Error"})
    supemail= request.POST['supemail']
    superuse = request.POST['superuse']
    passsuper = request.POST['passsuper']
    if not supemail or not superuse or not passsuper:
        return render(request, "portugues/register.html",{"messagel": "Precisa verificar informações"})
    try:
        User.objects.create_user(superuse,supemail,passsuper,is_superuser =True)
        return render(request, "portugues/register.html",{"messagel": "Super usuario registrado"})
    except IntegrityError:
        return render(request, "portugues/register.html",{"messagel": "Nome de usuário já utilizado, Precisa excluir"})


@login_required
def profile(request):
    try:
        profile = Profile.objects.get(userx=request.user)
    except ObjectDoesNotExist:
        profile = False
    try:
        aproving = Tester.objects.get(userx = request.user)
        
    except ObjectDoesNotExist:
        aproving = 'Sem informação'
    try:
        quanty = Lessons.objects.all()
        totaLesson = len(quanty)

        Gooding = Approval.objects.filter(lessonUser=request.user,bool_lesson_app=True)
        totalGood = len(Gooding)

        if totaLesson == 0:
            raise ObjectDoesNotExist

        
        avance = totalGood / totaLesson * 100

        if len(Gooding) == 1:
            avance = 0
    except ObjectDoesNotExist:
        avance = 0
    

    
    return render(request, "portugues/profile.html",{"profile": profile, "aprove": aproving,"avance":round(avance)})
    

    





@login_required
def profilephoto(request,code):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("index"))
    country = request.POST['pais']
    country = str(country).capitalize().strip()
    photo = request.FILES['filet']
    newphoto= Profile.objects.create(userx=request.user, photo= photo,country=country)
    return HttpResponseRedirect(reverse("profile"))


@login_required
def entrylessons(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse(view_register))
    index = request.POST['number_lesson']
    title = request.POST['title']
    theoric = request.POST['theoric']
    urlx = request.POST['urlx']
    videox = request.POST['videox']

    filex = request.FILES['filex']

    
    if not index or not title or not theoric or not urlx or not videox:
        return render(request, "portugues/register.html",{"message": "Todos os campos devem ser preenchidos"})
    try:
        Lessons.objects.create(number_lesson=index,title=title,theoric=theoric,urlx=urlx,videox=videox,filex=filex)
        return render(request,"portugues/register.html",{"message": "Salvou"})
    except IntegrityError:
        return render(request,"portugues/register.html",{"message": "O número da lição já existe"})

@login_required  
def lessons(request):
    info = Lessons.objects.all()
    return render(request, "portugues/lessons.html",{"info":info})

@login_required
def seelessons(request, code):
    lesson = serializers.serialize('json',Lessons.objects.filter(number_lesson=code))
    return JsonResponse(json.loads(lesson),safe=False)

@login_required
def aproval(request,code,userr):
    userx = User.objects.get(username=userr)
    if userx.is_superuser:
        return JsonResponse({"data": "exists"},safe=False)
    try:
        permited = Approval.objects.get(lessonUser = userx, number_lesson=code,bool_lesson_app= True)
        return JsonResponse({"data": True},safe=False)
    
    except ObjectDoesNotExist:
        return JsonResponse({"data": False},safe=False)
    
@login_required    
def pdfproof(request,code):
    archivo = Lessons.objects.get(number_lesson=code)
    pathfile = str(archivo.filex)
    file_path = os.path.join(settings.MEDIA_ROOT, pathfile)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def deletelessons(request):
    lessons = Lessons.objects.all()
    lessons.delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
def choosetest(request):
    lessons = Lessons.objects.all()
    return render(request, "portugues/choosetest.html",{"lessons": lessons})

@login_required
def teste(request,code):
    return render(request,"portugues/teste.html",{"code":code})

@login_required
def entryExam(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('view_register'))
    
    lessonx=  request.POST['lesson']
    question = request.POST['question']
    correct = request.POST['correct']
    falseone = request.POST['falseone']
    falsetwo = request.POST['falsetwo']

    if not lessonx or not question or not correct or not falseone or not falsetwo:
        return render(request, "portugues/register.html",{"messagex":"Precisa completar information"})
    
    lesson_object = Lessons.objects.get(number_lesson=lessonx)
    Exams.objects.create(lesson=lesson_object,question=question,correct=correct,false_one=falseone,false_two=falsetwo)
    return HttpResponseRedirect(reverse('register'))

@login_required
def getExam(request,code):
    exams = Exams.objects.filter(lesson=code)
    if len(exams) < 1 :
        return JsonResponse({"DATAX": False},safe=False)
    exam = random.choice(exams)
    toShow = Exams.objects.get(pk=exam.pk)
    question = toShow.question
    resorted = [toShow.correct,toShow.false_one,toShow.false_two]
    random.shuffle(resorted)

    colors = ['#1e96fc','#9ef01a','#ffff3f']
    color = random.choice(colors)
    return JsonResponse({"question":question, "answers1": resorted[0],"answers2":resorted[1],"answers3":resorted[2],"color":color,"pk":exam.pk},safe=False)

        


@login_required
def goexam(request,code):
    userx = request.user
    if userx.is_superuser:
        return JsonResponse({"DataFound": True},safe=False)
    try:
        Approval.objects.get(lessonUser=request.user,number_lesson=code,bool_lesson_app=True )
        return JsonResponse({"DataFound": True},safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"DataFound": False},safe=False)



@login_required
def check_answer(request,answer,pk):
    check = Exams.objects.get(pk=pk)
    if check.correct == answer:
        return JsonResponse({"ansDel": True })
    else:
        return JsonResponse({"ansDel": False})
    
@login_required
def positive(request,quantity,lessonx):
    userx = request.user
    if userx.is_superuser:
        return JsonResponse({"type":"SuperUser"},safe=False)
    try:
        number = lessonx + 1
        obje = Lessons.objects.get(number_lesson=number)
        tal = Approval.objects.create(lessonUser= userx,bool_lesson_app= True)
        tal.number_lesson.add(obje)
        try:
            average = Tester.objects.get(userx=userx)
            total = average.number_questions + 8
            rigths = average.right_answer + quantity
            save_average = Tester.objects.filter(userx=userx)
            save_average.update(number_questions=total,right_answer=rigths)
            return JsonResponse({"type":"SavedInfoExistent"},safe=False)
        
        except ObjectDoesNotExist:
            Tester.objects.create(userx=userx, number_questions=8,right_answer=quantity)
            return JsonResponse({"type":"SavedInfoNew"},safe=False)
    
    except ObjectDoesNotExist:
        return JsonResponse({"type":"No Info"},safe=False)


    
def negative(request,quantity):
    try:
        testw = Tester.objects.get(userx=request.user)
        totalQ = testw.number_questions + 8
        totalR = testw.right_answer + quantity
        testT = Tester.objects.filter(userx=request.user)
        testT.update(number_questions=totalQ,right_answer=totalR)
        return JsonResponse({"info":"Updated"},safe= False)
    except ObjectDoesNotExist:
        Tester.objects.create(userx=request.user,number_questions=8, right_answer=quantity)
        return JsonResponse({"info":"Saved"},safe= False)


def why(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    text = request.POST['why']
    text = str(text).upper().strip()
    Whyter.objects.create(userx=request.user,why=text)
    return HttpResponseRedirect(reverse('index'))

def passchange(request):
    userx = request.POST['chnageuser']
    old = request.POST['old']
    new = request.POST['new']

    if not userx or not old or not new:
        return render(request, "portugues/register.html",{"messagem":"Não salvou. Verifique as informações"})
    
    macth = re.fullmatch(r"C\d?\d?\d?\d?",new)

    if macth:
        confirm_user = authenticate(username=userx,password=old)
        if confirm_user == None:
            return render(request,"portugues/register.html",{"messagem":"A senha atual não está correta"})
        changer = User.objects.get(username=userx)
        changer.set_password(new)
        changer.save()
        return render(request,"portugues/register.html",{"messagem":"Salvou"})
    else:
        return render(request,"portugues/register.html",{"messagem":"A senha deve começar com “C” e seguir 4 números"})
    

def liker(request,code):
    post = Tips.objects.get(pk=code)
    try:
        chek = Reactions.objects.get(tip=post,userx=request.user)
        chek.delete()
        quantity = Reactions.objects.filter(tip=code)

        return JsonResponse({"like":len(quantity)},safe=False)
    except ObjectDoesNotExist:
        react = Reactions.objects.create(ReactBool=True)
        react.userx.add(request.user)
        react.tip.add(post)
        quantity = Reactions.objects.filter(tip=code)

        return JsonResponse({"like":len(quantity)},safe=False)

def lessonsJS(request):
    lessonT = serializers.serialize('json',Lessons.objects.all())
    return JsonResponse(json.loads(lessonT),safe=False)

def testJS(request):
    teses = serializers.serialize('json',Exams.objects.all())
    return JsonResponse(json.loads(teses),safe=False)

def userJS(request):
    student = serializers.serialize('json',User.objects.all())
    return JsonResponse(json.loads(student),safe=False)


def quantyAprov(request,userX):
    userL = User.objects.get(username=userX)
    aprovacion = Approval.objects.filter(lessonUser=userL)
    return JsonResponse({"lessonAprob":len(aprovacion)},safe=False)

def testingStudent(request,userP):
    userT = User.objects.get(username = userP)
    quanties = serializers.serialize('json',Tester.objects.filter(userx =userT))
    return JsonResponse(json.loads(quanties),safe=False)


def tipsJS(request):
    tiper = serializers.serialize('json',Tips.objects.all().order_by('-created'))
    return JsonResponse(json.loads(tiper),safe=False)

def reacter(request,code):
    reacted = Reactions.objects.filter(tip=code)
    return JsonResponse({"reacts":len(reacted)},safe=False)


def consultas(request):
    return render(request, "portugues/consultas.html")
    


def deleting(request, dicas):
    dica = Tips.objects.get(pk=dicas)
    dica.delete()
    return JsonResponse({"state":"Deleted"},safe=False)

def mywhy(request):
    whyp = Whyter.objects.get(userx = request.user)
    print(whyp.why)
    return JsonResponse({"why":whyp.why},safe=False)