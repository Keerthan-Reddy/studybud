from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, User
from .forms import RoomForm

# Create your views here.
from django.http import HttpResponse

def loginpage(request):
    context={}
    return render(request,'base/login_register.html',context)




def home(request):
    q=request.GET.get('q')
    if q==None:
        q=''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
        )
    topic=Topic.objects.all()
    room_count=rooms.count()
    context ={'rooms': rooms,'topic':topic,'room_count':room_count} 
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)


def createroom(request):
    form = RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {"form":form}
    return render(request,'base/create_room.html',context)


def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save();
            return redirect('home')
            
    context={'form':form}
    return render(request,'base/create_room.html',context)


def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{"obj":room})
    