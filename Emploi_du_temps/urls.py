from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.schedule_view, name='schedule_view'),
]