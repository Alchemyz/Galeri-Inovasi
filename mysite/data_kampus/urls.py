from django.contrib import admin
from django.urls import path
from data_kampus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('berita/<slug:slug_berita>/', views.detail_berita, name='detail_berita'),
    path('register/', views.register_view, name='register'),
    path('like/inovasi/<int:inovasi_id>/', views.like_inovasi_view, name='like_inovasi'),
    path('profil/', views.profil_view, name='profil'),
]