from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request, 'account/index.html', {'posts':posts})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'account/login.html', {'error':'username or password is incorrect!'})

    else:
        return render(request, 'account/login.html')



def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmpassword']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'account/register.html', {'error':'Username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'], email=request.POST['email'])
                auth.login(request, user)
                return redirect('login')


        else:
            return render(request, 'account/register.html', {'error':'Password doesn\'t matched'})

    else:
        return render(request, 'account/register.html')




@login_required(login_url='/login')

def dashboard(request):
    posts = Post.objects.filter(userid= request.user)
    return render(request, 'account/deshboard.html', {'posts':posts})

@login_required(login_url='/login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')


@login_required(login_url='/login')
def create(request):
    if request.method == 'POST':
        title     = request.POST['title']
        body      = request.POST['description']
        userid    = request.user

        savepost  = Post(title=title, body=body, userid=userid)
        savepost.save()
        return redirect('dashboard')


    else:
        return render(request, 'account/create.html')        



def deletes(request):
    if request.method == 'POST':
        ids = request.POST['delete']
        ddelt = Post.objects.get(id=ids)
        ddelt.delete()
        return redirect('dashboard')

    else:



        return redirect('dashboard')         
