from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, get_object_or_404, redirect

from .models import Livestock,Breed, ParentChild, WeightRecord, VaccinationLog
from .forms import BreedForm, ParentChildForm, LivestockForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})

    return render(request, 'authentication/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


#AREA DE LIVESTOCK 

@login_required
def livestock_list(request):
    livestock = Livestock.objects.all()
    return render(request, 'livestock/livestock_list.html', {'livestock': livestock})

@login_required
def livestock_create(request):
    form = LivestockForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = request.user
        instance.save()
        return redirect('livestock_list')
    return render(request, 'livestock/livestock_form.html', {'form': form, 'title': 'Registrar Animal'})

@login_required
def livestock_update(request, pk):
    instance = get_object_or_404(Livestock, pk=pk)
    form = LivestockForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updated_by = request.user
        instance.save()
        return redirect('livestock_list')
    return render(request, 'livestock/livestock_form.html', {'form': form, 'title': 'Editar Animal'})

@login_required
def livestock_delete(request, pk):
    instance = get_object_or_404(Livestock, pk=pk)
    instance.is_active = False
    instance.save()
    return redirect('livestock_list')


def livestock_detail(request, pk):
    animal = get_object_or_404(Livestock, pk=pk)
    madre = ParentChild.objects.filter(child=animal, relation_type='mother').first()
    padre = ParentChild.objects.filter(child=animal, relation_type='father').first()
    pesos = WeightRecord.objects.filter(livestock=animal).order_by('-recorded_at')
    vacunas = VaccinationLog.objects.filter(livestock=animal).order_by('-date')

    context = {
        'animal': animal,
        'madre': madre.parent if madre else None,
        'padre': padre.parent if padre else None,
        'pesos': pesos,
        'vacunas': vacunas
    }
    return render(request, 'livestock/livestock_detail.html', context)



# BREED 
def breed_list(request):
    breeds = Breed.objects.all()
    return render(request, 'breed/breed_list.html', {'breeds': breeds})

def breed_create(request):
    if request.method == 'POST':
        form = BreedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('breed_list')
    else:
        form = BreedForm()
    return render(request, 'breed/breed_form.html', {'form': form, 'title': 'Crear Raza'})

def breed_edit(request, pk):
    breed = get_object_or_404(Breed, pk=pk)
    if request.method == 'POST':
        form = BreedForm(request.POST, instance=breed)
        if form.is_valid():
            form.save()
            return redirect('breed_list')
    else:
        form = BreedForm(instance=breed)
    return render(request, 'breed/breed_form.html', {'form': form, 'title': 'Editar Raza'})

def breed_delete(request, pk):
    breed = get_object_or_404(Breed, pk=pk)
    if request.method == 'POST':
        breed.delete()
        return redirect('breed_list')
    return render(request, 'breed/breed_confirm_delete.html', {'breed': breed})



#PARENTCHILD
def parentchild_create(request):
    if request.method == 'POST':
        form = ParentChildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parentchild_list')
    else:
        form = ParentChildForm()
    return render(request, 'parentchild/parentchild_form.html', {'form': form, 'title': 'Registrar Parentesco'})

def parentchild_list(request):
    relaciones = ParentChild.objects.select_related('child', 'parent').all()
    return render(request, 'parentchild/parentchild_list.html', {'relaciones': relaciones})