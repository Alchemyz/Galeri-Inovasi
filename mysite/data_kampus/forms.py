from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil, Komentar 

class RegistrasiForm(UserCreationForm):
   
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan alamat email'
        })
    )
    
  
    nama_lengkap = forms.CharField(
        label='Nama Lengkap',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan nama lengkap Anda'
        })
    )
    
    institusi = forms.CharField(
        label='Institusi',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Asal institusi/universitas (Opsional)'
        })
    )
    
    no_hp = forms.CharField(
        label='No. HP',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contoh: 081234567890 (Opsional)'
        })
    )
    
    foto_profil = forms.ImageField(
        label='Foto Profil',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'nama_lengkap', 'institusi', 'no_hp', 'foto_profil')
       

    def __init__(self, *args, **kwargs):
        super(RegistrasiForm, self).__init__(*args, **kwargs)
        
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Konfirmasi Password'
        for field_name in ['username', 'password1', 'password2']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        
        user = super(RegistrasiForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            
            user.save()
            
            profil = user.profil 
            profil.nama_lengkap = self.cleaned_data.get('nama_lengkap')
            profil.institusi = self.cleaned_data.get('institusi')
            profil.no_hp = self.cleaned_data.get('no_hp')
            
            
            if 'foto_profil' in self.cleaned_data and self.cleaned_data['foto_profil']:
                profil.foto_profil = self.cleaned_data['foto_profil']
            
        
            profil.save()

        return user

class KomentarForm(forms.ModelForm):
     class Meta:
        model = Komentar
        fields = ['isi_komentar']
        widgets = {
            'isi_komentar': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tulis komentar Anda...'})
        }


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Masukkan email Anda'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Masukkan username'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilEditForm(forms.ModelForm):
    nama_lengkap = forms.CharField(
        label='Nama Lengkap',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan nama lengkap Anda'
        })
    )
    
    institusi = forms.CharField(
        label='Institusi',
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Asal institusi/universitas'
        })
    )
    
    no_hp = forms.CharField(
        label='No. HP',
        required=False,  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contoh: 081234567890'
        })
    )
    
    foto_profil = forms.ImageField(
        label='Foto Profil',
        required=False,  
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profil
        fields = ['nama_lengkap', 'institusi', 'no_hp', 'foto_profil']