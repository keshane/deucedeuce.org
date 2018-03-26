from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("join/", views.join, name="join"),
    path("<establishment_name>/", views.establishment, name="establishment"),
]
