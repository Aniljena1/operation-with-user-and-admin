from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from .forms import SignUpForm,EditUserProfile,EditAdminProfile
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
def Sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created Successfully')
            form.save()

    else:
        form = SignUpForm()
    return render(request,'enroll/signup.html',{'form':form})

# Login View
def user_login(request):
    if not request.user.is_authenticated: #if user not log in

        if request.method == 'POST':
            form = AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname , password=upass )
                if user is not None:
                    login(request, user)
                    messages.success(request,'Loged in Successfully')
                    return HttpResponseRedirect('/profile/')

        else:
            form = AuthenticationForm()
        return render(request, 'enroll/userlogin.html', {'form':form})

    else:
        return HttpResponseRedirect('/profile/')




# Admin Profile edit and user profile
# is_authenticated check admin is authenticated or not

def user_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            if request.user.is_superuser == True:
                form = EditAdminProfile(request.POST, instance=request.user)
                users = User.objects.all()
            else:
                form = EditUserProfile(request.POST,instance=request.user)
                users = None

            if form.is_valid():
                messages.success(request,'Profile Updated')
                form.save()
        else:
            if request.user.is_superuser == True:
                form = EditAdminProfile(instance=request.user)
                users = User.objects.all()
            else:
                form = EditUserProfile(instance=request.user)
                users = None
        context = {'name':request.user.username,'form':form,'users':users}
        return render(request,'enroll/profile.html',context)
    else:
        return HttpResponseRedirect('/login/')





#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# User Change password with old password

def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user) # it is session after change password you stay in profile page
                messages.success(request,'Password Change Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'enroll/changepassword.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


# change password without old password

def user_Forgot_Password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user) # it is session after change password you stay in profile page
                messages.success(request,'Password Change Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'enroll/forgotpassword.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def userdetail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        form = EditAdminProfile(instance=pi)
        return render(request,'enroll/userdetail.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')



