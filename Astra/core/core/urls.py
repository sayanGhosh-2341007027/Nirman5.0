"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from nome.views import home, sign, login, PredictUnderstaffed, predict_page,staff,dashboard,staffmanagement,attendance,salary
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', home, name='home'),
    path('sign/', sign, name='sign'),
    path('login/', login, name='login'),
    path('predict/', predict_page, name='predict'),
    path('staff/', staff, name='staff'),
    path('dashboard/', dashboard, name='dashboard'),
    path('staffmanagement/', staffmanagement, name='staffmanagement'),
    path('attendance/', attendance, name='attendance'),
    path('dashboard/attendance/', attendance, name='attendance'),
    path('admin/', admin.site.urls),
    path('salary/', salary, name='salary'),
    # ML endpoint — CORRECT URL
    path("ml/", csrf_exempt(PredictUnderstaffed.as_view()), name="ml_api"),
]
# staffmgmt/urls.py





