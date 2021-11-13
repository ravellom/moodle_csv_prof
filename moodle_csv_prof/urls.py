"""moodle_csv_prof URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', reviews.views.login_view, name='login'), 
    path('logout/', reviews.views.logout_view, name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', reviews.views.index, name='index'),
    path('data_analysis/', reviews.views.data_analysis, name='data_analysis'),
    path('general/', reviews.views.general_analysis, name='general_analysis'),
    path('participants/', reviews.views.part_analysis, name='part_analysis'),
    path('activities/', reviews.views.act_analysis, name='act_analysis'),
    path('help/', reviews.views.help, name='help')
   #url('data_analysis/', views.data_analysis, name='data_analysis'),
]
