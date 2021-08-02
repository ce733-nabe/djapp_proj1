from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'effi'
urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('showall/', views.showall, name='showall'),
]