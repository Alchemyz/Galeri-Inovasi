from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    slug= models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug= models.SlugField(unique=True, blank=True)
    isi = models.TextField()
    potensi = models.TextField(null=True, blank=True)
    inovator = models.CharField(max_length=200, null=True, blank=True)
    institusi = models.CharField(max_length=100, null=True, blank=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    gambar = models.ImageField(upload_to= 'berita/', blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_inovasi', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.judul
    
class Banner(models.Model):
    judul=models.CharField(max_length=100)
    gambar=models.ImageField(upload_to='banner/', blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    link_video = models.URLField(blank=True, null=True)


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=200)
    institusi = models.CharField(max_length=200, blank=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True, verbose_name="No.HP")
    foto_profil = models.ImageField(upload_to='foto_profil/', default='default.jpeg')

    def __str__(self):
        return f'profil {self.user.username}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profil'):
        instance.profil.save()

class Komentar(models.Model):
    inovasi = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='komentar')
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    isi_komentar = models.TextField()
    tanggal_komentar = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tanggal_komentar']

    def __str__(self):
        return f'Komentar oleh {self.penulis.username}'
