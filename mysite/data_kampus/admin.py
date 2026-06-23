from django.contrib import admin
from .models import Berita, Banner, Kategori, Profil

# Register your models here.
@admin.register(Berita)
class BeritaAdmin (admin.ModelAdmin):
    list_display = ('judul', 'tanggal')
    prepopulated_fields = {'slug': ('judul',)}
    search_fields = ('judul', 'inovator')
    list_filter = ('tanggal',)

@admin.register(Banner)
class BannerAdmin (admin.ModelAdmin):
     list_display = ('judul', 'tanggal')
     


@admin.register(Kategori)
class KategoriAdmin (admin.ModelAdmin):
     list_display = ('nama',)
     prepopulated_fields = {'slug': ('nama',)}

@admin.register(Profil)
class Profil (admin.ModelAdmin):
     list_display =('nama_lengkap',)