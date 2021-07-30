from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'effi'
urlpatterns = [
    path('', TemplateView.as_view(template_name='effi/index.html'), name='index'),
    path('upload/', views.upload, name='upload'),
]