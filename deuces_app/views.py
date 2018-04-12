from django.http import HttpResponseRedirect
from django.shortcuts import render
import deuces_app.models
from deuces_app.forms import DeucerForm
from deuces_app.forms import EstablishmentForm
from deuces_app.forms import RestroomForm
from deuces_app.forms import ReviewForm
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db import transaction


# Create your views here.
def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = EstablishmentForm(request.POST)
        if form.is_valid():
            deucer = deuces_app.models.Deucer.objects.get(user=request.user)
            deucer.points += 10
            with transaction.atomic():
                deucer.save()
                form.save()
            return HttpResponseRedirect("/")
    else:
        establishments = deuces_app.models.Establishment.objects.all()
        restrooms = deuces_app.models.Restroom.objects.all()
        reviews = deuces_app.models.Review.objects.all()
        deucers = deuces_app.models.Deucer.objects.all()
        data = {'establishments': establishments,
            'restrooms': restrooms,
            'reviews': reviews,
            'deucers': deucers,
            "user": request.user,
            }
        if request.user.is_authenticated:
            data["form"] = EstablishmentForm()
            data["user_info"] = request.user
            data["deucer_points"] = deuces_app.models.Deucer.objects.get(user=request.user).points
    return render(request, 'deuces_app/index.html', data)


def establishment(request, establishment_name):
    establishment = deuces_app.models.Establishment.objects.get(name=establishment_name)
    restrooms = establishment.restroom_set.all()
    sum_of_restrooms_average_ratings = 0
    restrooms_with_more_than_zero_ratings = 0

    for restroom in restrooms:
        all_reviews = restroom.review_set.all()
        rating_average = 0
        # avoids divide by 0
        if len(all_reviews) > 0:
            rating_average = sum(review.rating.value for review in all_reviews) / len(all_reviews)
            rating_average = round(rating_average, 1)
            sum_of_restrooms_average_ratings += rating_average
            restrooms_with_more_than_zero_ratings += 1
        restroom.rating_average = rating_average

    if restrooms_with_more_than_zero_ratings > 0:
        establishment.rating_average = round(sum_of_restrooms_average_ratings / restrooms_with_more_than_zero_ratings, 1)
    else:
        establishment.rating_average = 0

    data = {"establishment": establishment,
            "restroom_form": RestroomForm(),
            "restrooms": restrooms,

    }

    if request.user.is_authenticated:
        data["user_info"] = request.user
        data["deucer_points"] = request.user.deucer_set.all()[0].points
    return render(request, "deuces_app/establishment.html", data)


def restroom(request, establishment_name, restroom_name):
    restroom = deuces_app.models.Restroom.objects.get(establishment__name=establishment_name, name=restroom_name)
    reviews = deuces_app.models.Review.objects.filter(restroom=restroom)
    rating_average = 0
    if len(reviews) > 0:
        rating_average = sum(review.rating.value for review in reviews) / len(reviews)
        rating_average = round(rating_average, 1)
    data = {
            "restroom": restroom,
            "reviews": reviews,
            "review_form": ReviewForm(),
            "rating_average": rating_average,
           }
    if request.user.is_authenticated:
        data["user_info"] = request.user
        data["deucer_points"] = request.user.deucer_set.all()[0].points
    return render(request, "deuces_app/restroom.html", data)


def add_restroom(request, establishment_name):
    if request.method == "POST" and request.user.is_authenticated:
        form = RestroomForm(request.POST)
        if form.is_valid():
            restroom = form.save(commit=False)
            restroom.establishment = deuces_app.models.Establishment.objects.get(name=establishment_name)
            deucer = deuces_app.models.Deucer.objects.get(user=request.user)
            deucer.points += 5
            with transaction.atomic():
                deucer.save()
                restroom.save()
                form.save_m2m()
    return HttpResponseRedirect(reverse("establishment", args=[establishment_name]))


def add_review(request, establishment_name, restroom_name):
    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            deucer = deuces_app.models.Deucer.objects.get(user=request.user)
            review.restroom = deuces_app.models.Restroom.objects.get(name=restroom_name)
            review.deucer = deucer
            deucer.points += 2
            with transaction.atomic():
                deucer.save()
                review.save()
    return HttpResponseRedirect(reverse("restroom", args=[establishment_name, restroom_name]))


def join(request):
    if request.method == "POST":
        form = DeucerForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(form.cleaned_data["password"])
            new_user.save()
            new_deucer = deuces_app.models.Deucer(user=new_user, points=0)
            new_deucer.save()
            return HttpResponseRedirect("/")
    else:
        form = DeucerForm()
    return render(request, "deuces_app/join.html", {"form": form})



