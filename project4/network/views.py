from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from django.core.paginator import Paginator


from .models import Posters,Reactions,Follows
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt







def index(request):
    posters = Posters.objects.all().order_by("-created")
    paginator = Paginator(posters,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{"page_obj": page_obj, "posters":posters})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def creator(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("index"))
    text = request.POST["textP"]
    if len(text)> 0:
        Posters.objects.create(userx=request.user,poster=text,created=datetime.now(),edited=datetime.now(), EditBool=False )
    return HttpResponseRedirect(reverse("index"))

@login_required
def liker(request, code):
    if request.user.is_anonymous:
        return JsonResponse({"response": "anonimous user dont"},safe=False)

    try:
        response = Reactions.objects.get(post_number=code,userx=request.user)
        response.delete()
        quantity = Reactions.objects.filter(post_number=code)
        return JsonResponse({"response": len(quantity)},safe=False)

    except ObjectDoesNotExist:
        like= Reactions.objects.create(likes = 1, userx=request.user)    
        like.post_number.add(code)
        quantity = Reactions.objects.filter(post_number=code)
        return JsonResponse({"response": len(quantity)},safe=False)
    
@csrf_exempt
@login_required
def editer(request, code):
    if request.method == 'POST':
        data = json.loads(request.body)
        if len(data)> 0:
            if data.get("newtext")is not None:
                Posters.objects.filter(pk=code).update(poster= data["newtext"],edited=datetime.now(),EditBool=True)
                post = serializers.serialize('json',Posters.objects.filter(pk=code))
                return JsonResponse(json.loads(post), safe= False)
        else:
            return JsonResponse({"save":"not"}, safe= False)
    else:
        post = serializers.serialize('json',Posters.objects.filter(pk=code))
        return JsonResponse(json.loads(post), safe= False)
    
def profile(request,code):

    fulano = str(request.user)
    use = User.objects.get(username=code)
    FBool= False
    quantity_followers = 0
    quantity_following = 0
    try:
        fllwrs = Follows.objects.filter(userx=use,FollowBool=True)
        print(len(fllwrs))
        quantity_followers = len(fllwrs)

    except ObjectDoesNotExist:
        pass
    try:
        flls = Follows.objects.filter(followers=use,FollowBool=True)
        quantity_following = len(flls)

    except ObjectDoesNotExist:
        pass


    if fulano != 'AnonymousUser':
        try:
            flls= Follows.objects.get(userx=use,followers=request.user)
            print(flls.FollowBool)
            if flls.FollowBool == True:
                FBool = True
            
        except ObjectDoesNotExist:
            pass


        posters = Posters.objects.filter(userx=use.pk).order_by("-created")
        paginator = Paginator(posters, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html",{"page_obj":page_obj,"code":code,"FBool": FBool,"qfr": quantity_followers,"qfs":quantity_following})
        
    else:
        posters = Posters.objects.filter(userx=use.pk).order_by("-created")
        paginator = Paginator(posters, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html",{"page_obj":page_obj,"code":code,"FBool": FBool,"qfr": quantity_followers,"qfs":quantity_following})
        
    
@csrf_exempt
@login_required
def follow(request,code):
    toFollw= User.objects.get(username=code)
    try:
        fll = Follows.objects.get(userx= toFollw, followers= request.user)
        if fll.FollowBool == True:
            fll.FollowBool = False
            fll.save()
            return JsonResponse({"follow": False},safe=False)
        else:
            fll.FollowBool = True
            fll.save()
            return JsonResponse({"follow": True},safe=False)
        
    except ObjectDoesNotExist:
        flls= Follows.objects.create(userx=toFollw, FollowBool=True,quantityF= +1)
        flls.followers.add(request.user)
        return JsonResponse({"follow":True},safe=False)

@login_required  
def followp(request):
    fllw = Follows.objects.filter(followers=request.user, FollowBool=True).values('userx')
    medio = []
    if len(fllw)== 1:
        for i in range(len(fllw)):
            posters = Posters.objects.filter(userx=fllw[i]["userx"]).order_by('-created')
            if i == 0:
                medio = posters
    else:
        for i in range(len(fllw)):
            posters = Posters.objects.filter(userx=fllw[i]["userx"])
            if i == 0:
                medio = posters
            else:
                medio = medio.union(posters).order_by('-created')

    paginator = Paginator(medio, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/followp.html",{"page_obj":page_obj})

