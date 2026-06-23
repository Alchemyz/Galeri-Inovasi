from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='themes/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    path('', include('data_kampus.urls')),
    
]

urlpatterns += i18n_patterns(path("admin/", admin.site.urls), path("", include("cms.urls")))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)