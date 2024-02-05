from django.shortcuts import render
from books.models import Book
from django.db.models import Q
from books.forms import Bookform
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request,'home.html')
@login_required
def addbook(request):
    if(request.method=="POST"):
        t = request.POST['t']
        a = request.POST['a']
        p = request.POST['p']
        f = request.FILES['f']
        i = request.FILES['i']
        b = Book.objects.create(title=t,author=a,price=p,pdf=f,cover=i)
        b.save()
        return viewbook(request)
    return render(request,'addbook.html')



@login_required
def bookdetail(request,p):
    b=Book.objects.get(id=p)

    return render(request,'book.html',{'b':b})
@login_required
def bookdelete(request,p):
    b=Book.objects.get(id=p)
    b.delete()
    return viewbook(request)
@login_required
def bookedit(request,p):
    b = Book.objects.get(id=p)
    if (request.method == "POST"):  # after submission
        form = Bookform(request.POST,request.FILES,instance=b)  # creates form object initialized with values inside request.post
        if form.is_valid():
            form.save()  # save the form object inside db table
            return viewbook(request)

    form=Bookform(instance=b)
    return render(request,'edit.html',{'form':form})
@login_required
def addbook1(request):
    if(request.method=="POST"): #after submission
        form=Bookform(request.POST) #creates form object initialized with values inside request.post
        if form.is_valid():
            form.save()  #save the form object inside db table
            return viewbook(request)
    form=Bookform()   #empty form object with no values
    return render(request, 'addbook1.html',{'form':form})
@login_required
def search(request):
    query=""
    b=None
    if(request.method=="POST"):
        query=request.POST['q']
        if(query):
            b=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request,'search.html',{'query':query,'b':b})

def fact(request):
    if (request.method=="POST"):
        num=int(request.POST['n'])
        f=1
        for i in range(1,num+1):
            f=f*i

        return render(request,'fact.html',{'fact':f})
    return render(request, 'fact.html')

@login_required
def viewbook(request):
    k=Book.objects.all()
    return render(request,'viewbook.html',{'b':k})
