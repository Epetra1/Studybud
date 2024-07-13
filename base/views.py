from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import topic, rooms, message, User




from .forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_page(request):
    post='login'
    if request.user.is_authenticated:
        return redirect('/')
    else:
        
        if request.method == 'POST':
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            try:
                abc = User.objects.get(email = email)
            except:
                messages.error(request, "user doesnot exist")
            abc = authenticate(request, email = email, password = password)
            if abc is not None:
                login(request,abc)
                return redirect ('home')
            else:
                messages.error(request, 'username or password is not correct')
    context = {'post':post}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    
    logout(request)
    return redirect('home')

def register_user(request):
     post = 'register'
     if request.user.is_authenticated:
        return redirect('/')
     if request.method =='POST':
         form = MyUserCreationForm(request.POST)
         if form.is_valid():
             user = form.save(commit=False)
             user.username = user.username.lower()
             user.save()
             login(request,user)
             print('its registered'
             )
             return redirect('home')
         
         else:
             messages.error(request,'an error was occured')
     form = MyUserCreationForm()
     context =  {'form':form, 'post': post}
     
     return render ( request, 'base/login_register.html',context )




    

def home(requeset):
    #q is for topic link in left where it says 'browse topic'
    q = requeset.GET.get('q') if requeset.GET.get('q')!=None else ''
    print(q)
    room = rooms.objects.filter(topic__name__icontains=q )

    #s is for serch ingine
    s = requeset.GET.get('s') if requeset.GET.get('s')!=None else '' 
    if s:
       
        room = rooms.objects.filter(Q(topic__name__icontains=s) | Q(name__icontains=s) | Q(description__icontains = s) | Q(user__username__icontains=s) )

    topics = topic.objects.all()[0:5]
    room_messages = message.objects.filter(room__topic__name__icontains= q)
    rooms_count = rooms.objects.count()
   
    

    
    context = {'roome':room ,'topics':topics, 'room_messages':room_messages, 'rooms_count': rooms_count}
    for r in room:
        print (r.topic.name)
    return render(requeset, 'base/home.html', context)


def room(requeset, pk):
    room = rooms.objects.get(id = pk)
    room_messages= room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if requeset.method =='POST':
        messagee = message.objects.create(
            user = requeset.user,
            room = room,
            body = requeset.POST.get('body')


        )
        room.participants.add(requeset.user)
        
        
       
        return redirect ('room', pk = room.id, )
    context = {'participants': participants ,'r':room, 'room_messages':room_messages }
    return render(requeset , 'base/room.html',context)
    
def profile(request,pk):
    user = get_object_or_404(User, id=pk)
    rooms = user.rooms_set.all()
    room_messages = user.message_set.all()
    topics = topic.objects.all()
    context = {'user': user, 'roome':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request , 'base/profile.html', context )        

def edit_user(request):
    form = UserForm(instance = request.user)
    if request.method =='POST':
        form = UserForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid:
            form.save()
            return redirect('profile', pk=request.user.id)
        
    context = {'form': form}
         



    return render(request, 'base/edit_user.html', context)
        



   


@login_required(login_url='login_page')
def room_create(request):

    form = RoomForm()
    topics = topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topicse,created = topic.objects.get_or_create(name = topic_name)
        rooms.objects.create(
            user = request.user,
            topic = topicse,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            )
        
        

   
        # form = RoomForm(request.POST)
        # if form.is_valid():

        #     room = form.save()
        #     room.user = request.user
        #     room.save()
        #     print(request.POST)
        return redirect('/')
    submit = 'Create Room'
    context = {'form': form, 'topic':topics,'submit': submit}
    return render (request, 'base/room_create.html', context)

@login_required(login_url='login_page')
def room_update(request, pk):
    topics= topic.objects.all() 
    room = rooms.objects.get(id = pk)
    form = RoomForm(instance = room)
    if request.user != room.user:
        
        return HttpResponse('You need to be host to edit <a href="/"> return to home </a>')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        topic_name = request.POST.get('topic')
        topicse, created = topic.objects.get_or_create(name = topic_name)
        room.topic= topicse
        room.user = request.user
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('/')
    submit = 'Update Room'
    context = {'form' : form, 'room':room, 'topic':topics, 'submit': submit}
    return render (request, 'base/room_create.html', context)



@login_required(login_url = 'login_page')
def room_delete(request,pk):
    room = rooms.objects.get(id = pk)
    if request.user != room.user:
        
        return HttpResponse('You need to be host to delete <a href="/"> return to home </a>')
    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'base/delete.html', {'obj' : room})


@login_required(login_url = 'login_page')
def delete_message(request,pk):
    messages = message.objects.get(id = pk)
    room_id = messages.room.id
    if request.user != messages.user:
        
        return HttpResponse('You need to be host to delete <a href="/"> return to home </a>')
    if request.method == 'POST':
        messages.delete()
        return redirect(f'/room/{room_id}/')

    return render(request, 'base/delete.html', {'obj' : messages})

def topics(request):
    s = request.GET.get('s') if request.GET.get('s')!=None else '' 
    if s:
        topics = topic.objects.filter(name__icontains = s)
    else: 
        topics = topic.objects.all()
    context = {'topics': topics}
    return render(request,'base/topics.html', context )

def activity(request):
    messag = message.objects.all()[0:2]

    context= {'messag':messag}
    return render (request, 'base/activity.html', context )
# Create your views here.
