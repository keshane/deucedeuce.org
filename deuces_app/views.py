from django.http import HttpResponseRedirect
from django.shortcuts import render
import deuces_app.models
from deuces_app.forms import DeucerForm
from deuces_app.forms import EstablishmentForm
from deuces_app.forms import RestroomForm
from deuces_app.forms import ReviewForm
from django.contrib.auth.hashers import make_password
from django.urls import reverse


# Create your views here.
def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = EstablishmentForm(request.POST)
        if form.is_valid():
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
    return render(request, 'deuces_app/index.html', data)


def establishment(request, establishment_name):
    establishment = deuces_app.models.Establishment.objects.get(name=establishment_name)
    restrooms = deuces_app.models.Restroom.objects.filter(establishment__name=establishment_name)
    restroom_reviews = {}
    for restroom in restrooms:
        reviews = deuces_app.models.Review.objects.filter(restroom=restroom)
        restroom_reviews[restroom] = reviews
    data = {"restroom_reviews": restroom_reviews,
            "establishment": establishment,
            "restroom_form": RestroomForm(),
            "review_form": ReviewForm(),
    }
    return render(request, "deuces_app/establishment.html", data)


def restroom(request, establishment_name, restroom_name):
    restroom = deuces_app.models.Restroom.objects.get(establishment__name=establishment_name, name=restroom_name)
    reviews = deuces_app.models.Review.objects.filter(restroom=restroom)
    data = {
            "restroom": restroom,
            "reviews": reviews,
           }

    return render(request, "deuces_app/restroom.html", data)



def add_restroom(request, establishment_name):
    if request.method == "POST" and request.user.is_authenticated:
        form = RestroomForm(request.POST)
        if form.is_valid():
            restroom = form.save(commit=False)
            restroom.establishment = deuces_app.models.Establishment.objects.get(name=establishment_name)
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
            review.save()
    return HttpResponseRedirect(reverse("establishment", args=[establishment_name]))


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



