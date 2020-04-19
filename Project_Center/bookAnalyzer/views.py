#Django Libraries
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .models import  Book
from .forms import BookForm
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#Libraries
import re
import pickle
import math
import pandas as pd
import numpy as np
import json
import difflib

#load the Data
data=json.load(open("bookAnalyzer/static/bookAnalyzer/data.json"))

# Create your views here.
def home(request):
    return render(request,'bookAnalyzer/home.html')

def bookPre(request):

    if request.method == 'GET':
        return render(request,'bookAnalyzer/bookPre.html',{'form':BookForm()})
    else:
        try:
            form = BookForm(request.POST)
            newbook = form.save(commit=False)
            newbook.save()
            return HttpResponseRedirect(reverse("bookAnalyzer:bookDetails"))
        except ValueError:
            error_msg = "something went wrong!"
            return render(request,"bookAnalyzer/useraccount.html",{'form':BookForm(),'error_msg':error_msg})

def bookDetails(request):
    book = Book.objects.all()
    return render(request,'bookAnalyzer/bookDetails.html',{"book":book})




def viewBooks(request, books_pk):

    book = get_object_or_404(Book,pk=books_pk)
    words = voc(book.contents)
    bokie=vocp(book.contents)
    freqwords = pd.Series(words[0]).value_counts()
    wordsmedian = freqwords.median()
    wordcount = len(words[0])
    unwordcount = len(words[1])

    book.data=words
    book.save()
    if request.is_ajax() :
        if request.POST.get("code")=="context":
            text=request.POST.get("query",False)
            contexts=context(text,words[0])
            #return JsonResponse({"context":contexts})
            keyword=request.POST.get('query').strip()
            if keyword in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+"<br>" for x in range(0,len(key))]
                return JsonResponse({'definition':key,"context":contexts})
            elif keyword.upper in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+" <br>" for x in range(0,len(key))]
                return JsonResponse({'definition':key,"context":contexts})
            elif keyword.lower in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+" <br>" for x in range(0,len(key))]
                return JsonResponse({'definition':key,"context":contexts})
            else:
                key=difflib.get_close_matches(keyword,data.keys(),n=3,cutoff=0.7)
                return JsonResponse({'matches':key,"context":contexts})

        if request.POST.get("code")=="explore":

            niceW = freqwords[(freqwords<int(request.POST.get("up",False))) &
            (freqwords>int(request.POST.get("low",False)))]

            if request.POST.get("length",False)!="":
                length=int(request.POST.get("length",False))
                niceW=niceW[(niceW.index.map(lambda x: len(x)>length))]
            return JsonResponse({
            "Word":list(niceW.index),
            "Freq":niceW.values.tolist()
            })
        if request.POST.get("code")=="definition":
            keyword=request.POST.get('query').strip()
            if keyword in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+r"<br> " for x in range(0,len(key))]

                return JsonResponse({'definition':key})
            elif keyword.upper in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+"<br>" for x in range(0,len(key))]
                return JsonResponse({'definition':key})
            elif keyword.lower in data.keys():
                key=data[keyword]
                key=[""+str(x+1)+". "+key[x]+"<br>" for x in range(0,len(key))]
                return JsonResponse({'definition':key})
            else:
                key=difflib.get_close_matches(keyword,data.keys(),n=3,cutoff=0.7)
                return JsonResponse({'matches':key})

    return render(request,'bookAnalyzer/bookAnalysis.html',
    {
    'book':book,"words":bokie,"median":wordsmedian,
    'wordcount':wordcount,'unwordcount':unwordcount

    })



    #context=context(request.POST.get("query",False),words[0])
    #return render(request,'bookAnalyzer/context.html',{"context":context})

#FUNCTIONS
def voc(x):
    regx=re.compile(r"""[A-a-Z-z]+""")
    resultAll = regx.findall(x)
    resultUnique = list(set(resultAll))
    return [resultAll,resultUnique]
def vocp(x):
    regx=re.compile(r"""(\w+|[.!,?"";]|\s)""")
    resultAll = regx.findall(x)
    return resultAll

def vocfreq(x):
    regx=re.compile(r"""[A-a-Z-z]+""")
    resultAll = regx.findall(x)
    resultUnique = list(set(resultAll))
    freq=[resultAll.count(x) for x in resultUnique]
    freqVoc=pd.DataFrame({"Word":resultUnique,"Freq":freq})
    return freqVoc

def context(args,words):
    matchesA=[]
    for j in range(0,len(words)):
        if args.casefold()==words[j].casefold():
            try:
                before=(words[j-5]+" "+words[j-4]+" "+words[j-3]+" "+words[j-2]+" "+words[j-1])
                matchesA.append(before+" "+args+" "+words[j+1]+" "+words[j+2]+" "+words[j+3]+" "+words[j+4]+" "+words[j+5])
            except:
                next
    return matchesA

def selby(df,up,low,starts="",col1=0,col=1):
    if starts != "":
        crit1=df.iloc[:,col1].map(lambda x: x.startswith(starts))
    crit2 = df.iloc[:,col].map(lambda x: x < up)
    crit3 = df.iloc[:,col].map(lambda x: x > low)
    if starts != "":
        return df[crit1 & crit2 & crit3].to_dict()
    return df[crit2 & crit3].to_dict()
# TODO: A function that will transform a DF into dict of lists for JS API
