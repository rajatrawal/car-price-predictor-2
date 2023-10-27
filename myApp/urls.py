from . import views 
from django.urls import path

urlpatterns = [
    path('',views.index,name='home'),
    path('predict/',views.predict,name='predict'),
]
