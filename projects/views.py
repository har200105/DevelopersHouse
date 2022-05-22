from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from projects.utils import searchProjects
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def projects(request):

    projects,search_query = searchProjects(request)
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(projects,results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects = paginator.page(page)    
    except EmptyPage:
        page=0
        projects = paginator.page(page)     


    leftIndex =  (int(page) - 4)    
    
    if leftIndex < 1:
        leftIndex = 1


    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1   

    custom_range = range(leftIndex,rightIndex)    
          

    context = {'projects': projects,'search_query':search_query,'paginator':paginator
    , 'custom_range':custom_range
    }
    return render(request, 'projects.html', context)


def project(request, pk):

    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        messages.success('Your Review was sent successfully')
        return redirect('project',pk=project.id)
    # tags = project.tags.all()
    context = {'project': project,'form':form}

    return render(request, 'project.html', context)

@login_required(login_url='login')
def createProject(request):

    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            return redirect('account')
            
    context = {'form': form}

    return render(request, 'project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}

    return render(request, 'project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):

    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def createSkill(request):
    context = {}
    return render(request,'skillsForm.html',context)
