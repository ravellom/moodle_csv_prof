##Rendering Data-Frame to html template in table view using Django Framework


## views.py
from django.shortcuts import HttpResponse
import pandas as pd
  
def Table(request):
    df = pd.read_csv("tableview/static/csv/20_Startups.csv")
    #'tableview/static/csv/20_Startups.csv' is the django 
    # directory where csv file exist.
    # Manipulate DataFrame using to_html() function
    geeks_object = df.to_html()
  
    return HttpResponse(geeks_object)

#### urls.py
 """
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name ='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name ='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tableview import views
  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Table, name ="table"),
]


###############

#views.py

# Write Python3 code here
from django.shortcuts import render
import pandas as pd
import json
  
# Create your views here.
def Table(request):
    df = pd.read_csv("tableview/static/csv/20_Startups.csv")
  
    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
  
    return render(request, 'table.html', context)


 ##  table.html (‘Bootstrap HTML Template’)

<!-- Write HTML code here -->
<!DOCTYPE html>
<html lang="en">
<head>
  <title>TableView - Startup</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
</head>
<body>
  
<div class="container">
  <h2 class="text-center"><u>20 - Startups Table</u></h2><br>            
  <table class="table table-dark table-striped">
    <thead>
      <tr>
        <th>R&D Spend</th>
        <th>Administration</th>
        <th>Marketing Spend</th>
        <th>State</th>
        <th>Profit</th>
      </tr>
    </thead>
    <tbody>
    <!-- jinja2 Technique -->
    {% if d %}  
    {% for i in d %}
      <tr>
        <td>{{i.RD_Spend}}</td>
        <td>{{i.Administration}}</td>
        <td>{{i.Marketing_Spend}}</td>
        <td>{{i.State}}</td>
        <td>{{i.Profit}}</td>
      </tr>
    {% endfor %}
    {% endif %}
    </tbody>
  </table>
</div>
  
</body>
</html>