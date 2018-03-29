from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("join/", views.join, name="join"),
    path("<establishment_name>/", views.establishment, name="establishment"),
    path("<establishment_name>/add-restroom/", views.add_restroom, name="add_restroom"),
    path("<establishment_name>/<restroom_name>/add-review", views.add_review, name="add_review"),
]
