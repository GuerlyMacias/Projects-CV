from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
from django.http import HttpResponseRedirect
import markdown
import random




def index(request):
        if request.method == "POST":
            query = request.POST.get("q",None)
            return HttpResponseRedirect(reverse("entries:search",args=[query]))
        else:
            return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
        
def entry(request,title):
    titles= util.list_entries()
    for one in titles:
        print(one)
        if title.lower() in one.lower():
            print(one)
            info = util.get_entry(title)
            info = markdown.markdown(info)
            return render(request, "encyclopedia/entry.html",{"info":info,"x":title})
    return HttpResponseRedirect(reverse("entries:apology", args=["Page Not found"]))
        

def search(request,q):
        titles = util.list_entries()
        if q in titles:
            query = util.get_entry(q)
            titulo = markdown.markdown(query)
            return render(request, "encyclopedia/entry.html",{"info":titulo,"x":q})
        else:
            recomendations= list()
            for title in titles:
                if q.lower() in title.lower():
                    recomendations.append(title)
            return render(request, "encyclopedia/search.html",{"entries":recomendations})
                
                

def create(request):
    if request.method == 'POST':
        titli = request.POST.get("title",None)
        descrip = request.POST.get("description",None)

        titles = util.list_entries()
        for one in titles:
            if titli.lower() == one.lower():
                return render(request,"encyclopedia/creates.html",{"error":"Page Already Exist"})
                
        util.save_entry(titli,descrip)
        return HttpResponseRedirect(reverse("entries:entry",args=[titli]))       
                
    else:
        return render(request, "encyclopedia/creates.html")



def edit(request):
    if request.method == "POST":
        tin = request.POST.get("tin",None)
        new= request.POST.get("new",None)
        entry = util.get_entry(tin)
        tan = request.POST.get("tan",None)
        if not tan:
            return render(request, "encyclopedia/edit.html",{"description": entry, "title": tin})
        else:
            util.save_entry(new,tan)
            return HttpResponseRedirect(reverse("entries:entry",args=[new]))
        
    else:
        return render(request,"encyclopedia/edit.html")
    
def random_page(request):
    titles = util.list_entries()
    one = random.choice(titles)
    return HttpResponseRedirect(reverse("entries:entry",args=[one]))

def apology(request,info):
    return render(request, "encyclopedia/apology.html",{"info": info})