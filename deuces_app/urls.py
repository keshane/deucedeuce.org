from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('', views.index, name='index'),
    path("join/", views.join, name="join"),
    path("sign-in/", authviews.LoginView.as_view(), name="sign_in"),
    path("sign-out/", authviews.LogoutView.as_view(next_page="index"), name="sign_out"),
    path("<establishment_name>/", views.establishment, name="establishment"),
    path("<establishment_name>/add-restroom/", views.add_restroom, name="add_restroom"),
    path("<establishment_name>/<restroom_name>/", views.restroom, name="restroom"),
    path("<establishment_name>/<restroom_name>/add-review", views.add_review, name="add_review"),
]
