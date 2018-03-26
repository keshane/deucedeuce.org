from django.http import HttpResponseRedirect
from django.shortcuts import render
import deuces_app.models
from deuces_app.forms import DeucerForm
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):
    establishments = deuces_app.models.Establishment.objects.all()
    restrooms = deuces_app.models.Restroom.objects.all()
    reviews = deuces_app.models.Review.objects.all()
    deucers = deuces_app.models.Deucer.objects.all()
    data = {'establishments': establishments,
            'restrooms': restrooms,
            'reviews': reviews,
            'deucers': deucers,
           }
    return render(request, 'deuces_app/index.html', data)


def establishment(request, establishment_name):
    establishment = deuces_app.models.Establishment.objects.get(name=establishment_name)
    reviews = deuces_app.models.Review.objects.filter(restroom__establishment__name=establishment_name)
    data = {"reviews": reviews,
            "establishment": establishment}
    return render(request, "deuces_app/establishment.html", data)


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



