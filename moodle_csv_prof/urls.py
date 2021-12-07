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
import core.views, prof.views, direct.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aplicación core
    path('login/', core.views.login_view, name='login'), 
    path('logout/', core.views.logout_view, name='logout'),
    path('register/', core.views.register, name='register'), 
    path('', core.views.index, name='index'),
    path('help/', core.views.help, name='help'),
    path('update/', core.views.update, name='update'),
    path('del_global_df/', core.views.del_global_df, name='del_global_df'),
    # Aplicación prof
    path('data_analysis/', prof.views.data_analysis, name='data_analysis'),
    path('general/', prof.views.general_analysis, name='general_analysis'),
    path('participants/', prof.views.part_analysis, name='part_analysis'),
    # Aplicación direct
    path('data_analysis_direct/', direct.views.data_analysis_direct, name='data_analysis_direct'),
    path('general_direct/', direct.views.general_analysis_direct, name='general_analysis_direct'),
    path('participants_direct/', direct.views.part_analysis_direct, name='part_analysis_direct'),
    path('cursos_direct/', direct.views.cursos_direct, name='cursos_direct')

    #path('accounts/', include('django.contrib.auth.urls')),
]
