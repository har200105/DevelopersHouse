from re import L
from django.shortcuts import render,redirect

from users.utils import searchProfiles
from .models import Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def login(request):

    if request.user.is_authenticated:
        redirect('profile')

    if request.method == 'POST':

        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error('User Doesnt Exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            redirect(request.GET['next'] if 'next'  in request.GET else 'account')
        else:
            messages.error('Username or Password is Incorrect')    

    return render(request,'auth.html')

def register(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request,'User Account was created')
                login(request,user)
                redirect('profile')
            else:
                messages.error(request,'Something Went Wrong')    


    return render(request,'auth.html',{'page':page,'form':form})

def logoutUser(request):
    logout(request)
    messages.error(request,'User was logout')
    redirect('login')

def profiles(request):
    profiles,search_query = searchProfiles(request)

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query)|  
    Q(short_intro__icontains=search_query) | Q(skill__in=skills))



    context = {'profiles':profiles,'search_query':search_query}

    return render(request,'profiles.html',context)

def userProfile(request,pk):
    
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    return render(request,'userProfile.html',{'profile':profile,'topSkills':topSkills,
    'otherSkills':otherSkills})


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.projects_set.all()

    context = {'profile':profile,'skills':skills,'projects':projects}

    return render(request,'account.html',context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    print("......")
    print(profile)
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILE,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form} 
    return render(request,'profile_form.html',context)


@login_required(login_url='login')
def createSkill(request):

    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill created !!')
            return redirect('account')

    context = {'form':form}
    return render(request,'skillsForm.html',context)


@login_required(login_url='login')
def updateSkill(request,pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill updated !!')
            return redirect('account')

    context = {'form':form}
    return render(request,'skillsForm.html',context)


def deleteSkill(request,pk):
    profile = request.user.profile
    print(profile)
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill deleted !!')
        return redirect('account')
    context = {'object':skill}
    return render(request,'delete.html',context)