"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # import settings to access static file settings
from django.conf.urls.static import static # needed to serve static files during development and tells django where to find them

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hw/', include('hw.urls')),
    path('quotes/', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('mini_insta/', include('mini_insta.urls')), # NEW URL for the mini instagram app
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # configuring static files serving
