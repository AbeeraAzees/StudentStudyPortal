from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')
@login_required
def notes(request):
    if request.method =="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username}successfully")  
    else:
      form = NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
class NotesDetailView(generic.DetailView):
    model=Notes
@login_required
def homework(request):
    form=Homeworform()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done =True
    else:
        homework_done=False    
    context={'homeworks':homework,'homeworks_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context) 
@login_required
def todo(request):
    if request.method =='POST':
        form= TodoForm(request.POST)
        if form.is_valid():
            try:
                finished =request.POST["is_finished"]
                if finished== 'on':
                   finished = True
                else:
                    finished= False
            except:
                finished=False           
            todos=Todo(
            user=request.user,
            title=request.POST['title'],
            is_finished=finished
           ) 
            todos.save()
            messages.success(request,f"Todo added from {request.user.username}!!")
    else:
        form=TodoForm()        
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True
    else:
         todos_done=False    
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)
@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
       todo.is_finished= False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')  
@login_required
def delete_todo(request,pk=None): 
    Todo.objects.get(id=pk).delete() 
    return redirect("todo")  

def books(request):
    if request.method == "POST":
        form=DashboardFom(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeinfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeinfo'].get('count'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                }
           
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context) 

    else:    
        form=DashboardFom()
    context={'form':form}
    return render(request,"dashboard/books.html",context) 
# ***********************************dictionary*********************************************    
def dictionary(request):
     if request.method == "POST":
        form=DashboardFom(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':''
            } 
        return render(request,"dashboard/dictionary.html",context)
     else:   
       form=DashboardFom()
       context={'form':form}
       return render(request,"dashboard/dictionary.html",context)
     

    #  **************************************Wiki************************************
def wiki(request):
       if request.method=='POST':
           text=request.POST['text']
           form=DashboardFom(request.POST)
           search=wiki.page(text)
           context={
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary
               } 
           return render(request,"dashboard/wiki.html",context)
       else:
           form=DashboardFom()
           context={
                'form':form,
           }
           return render(request,"dashboard/wiki.html",context)
@login_required
def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Acccount created for{username}")
            return redirect("login")
    else:       
        form=UserRegistrationForm
    context={
        'form':form
    }
    return render(request,"dashboard/register.html",context)
           


