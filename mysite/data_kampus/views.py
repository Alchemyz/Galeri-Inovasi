from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Berita,Banner
from django.contrib import messages
from .forms import RegistrasiForm, KomentarForm, UserEditForm, ProfilEditForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    berita = Berita.objects.all()
    banner = Banner.objects.all()
    return render(request, 'themes/homepage.html',{
        'is_home' : True,
        'berita': berita,
        'banner' : banner
    })

def detail_berita(request, slug_berita):
    berita = get_object_or_404(Berita, slug=slug_berita)
    
    komentar_list = berita.komentar.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
            
        komentar_form = KomentarForm(request.POST)
        if komentar_form.is_valid():
            komentar = komentar_form.save(commit=False)
            
            komentar.inovasi = berita  
            
            komentar.penulis = request.user
            
            komentar.save()
            
            return redirect('detail_berita', slug_berita=berita.slug)
    else:
        komentar_form = KomentarForm()
    context = {
        'berita': berita,
        'komentar_list': komentar_list,
        'komentar_form': komentar_form,
    }
    
    return render(request, 'themes/detail_berita.html', context)


@login_required 
def like_inovasi_view(request, inovasi_id):
    berita = get_object_or_404(Berita, id=inovasi_id)
    
    if berita.likes.filter(id=request.user.id).exists():
        berita.likes.remove(request.user)
    else:
        berita.likes.add(request.user)
        
    return redirect('detail_berita', slug_berita=berita.slug)



def register_view(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = RegistrasiForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, 'Registrasi berhasil! Anda sekarang sudah login.')
            return redirect('home') 
    else:
        form = RegistrasiForm()
        
    return render(request, 'themes/register.html', {'form': form})


@login_required 
def profil_view(request):
    
    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = ProfilEditForm(request.POST, 
                                request.FILES, 
                                instance=request.user.profil)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('home') 

    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfilEditForm(instance=request.user.profil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'themes/profil.html', context)