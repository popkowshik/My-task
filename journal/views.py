from django.shortcuts import render, redirect

from .forms import Createuserform, LoginForm, ThoughtForm, updateuserform, updateprofileform

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required 

from django.contrib import messages

from . models import Thought, Profile

from django.contrib.auth.models import User

from django.core.mail import send_mail

from django.conf import settings


def homepage(request):
    
    return render(request,'journal/index.html')

def register(request):

    form = Createuserform()

    if request.method == "POST":

        form = Createuserform(request.POST)

        if form.is_valid():

            current_user = form.save(commit=False)

            form.save()

            profile = Profile.objects.create(user=current_user)

            send_mail("Welcome to the edenthought", "congratulations for signin to your account", settings.DEFAULT_FROM_EMAIL, [current_user.email])

            messages.success(request, "User created account")

            return redirect('my-login')
        
    context = {'registration': form}
    
    return render(request,'journal/register.html',context)

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')

    context = {'loginform':form}

    return render(request,'journal/my-login.html',context)



def user_logout(request):

    auth.logout(request)

    return redirect("")


@login_required(login_url='my-login')
def dashboard(request):

    profile_pic = Profile.objects.get(user=request.user)

    context = {'profilepic':profile_pic}

    return render(request,'journal/dashboard.html', context)




@login_required(login_url='my-login')
def create_thought(request):

    form = ThoughtForm()

    if request.method == 'POST':

        form = ThoughtForm(request.POST)

        if form.is_valid():

            thought = form.save(commit=False)

            thought.user = request.user

            thought.save()

            return redirect('my-thought')
        
    context = {'createthoughtform':form}

    return render(request,'journal/create-thought.html',context)


@login_required(login_url='my-login')
def my_thought(request):

    current_user = request.user.id

    thought = Thought.objects.all().filter(user=current_user)

    context = {'allthoughts':thought}


    return render(request,'journal/my-thought.html', context)


@login_required(login_url='my-login')
def update_thought(request, pk):

    try:

        thought = Thought.objects.get(id=pk)

    except:

        return redirect('my-thoughts')

    form = ThoughtForm(instance=thought)

    if request.method == 'POST':

        form = ThoughtForm(request.POST, instance=thought)

        if form.is_valid():

            form.save()

            return redirect('my-thought')
        
    context = {'updatethought': form}

    return render(request,'journal/update-thought.html', context)



@login_required(login_url='my-login')
def delete_thought(request, pk):

    try:

        thought = Thought.objects.get(id=pk, user=request.user)

    except:

        return redirect('my-thought')
    
    if request.method == 'POST':

        thought.delete()

        return redirect('my-thought')


    return render(request,'journal/delete-thought.html')


@login_required(login_url='my-login')
def profile_management(request):

    form = updateuserform(instance = request.user)

    profile = Profile.objects.get(user = request.user)

    form_2 = updateprofileform(instance=profile)

    if request.method == 'POST':

        form = updateuserform(request.POST, instance=request.user)

        form_2 = updateprofileform(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            form.save()

            return redirect('dashboard')
        
        if form_2.is_valid():

            form_2.save()

            return redirect('dashboard')

    context = {'userupdateform':form, 'profileupdateform':form_2}

    return render(request,'journal/profile-management.html',context)


@login_required(login_url='my-login')
def delete_account(request):

    if request.method == 'POST':

        deleteuser = User.objects.get(username=request.user)

        deleteuser.delete()

        return redirect("")

    return render(request,'journal/delete-account.html',)
