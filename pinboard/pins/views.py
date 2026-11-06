from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PinForm, RatingForm, SignUpForm
from .models import Pin, Rating


def annotated_pins():
    return Pin.objects.select_related("author").annotate(
        avg=Avg("ratings__stars"), n_ratings=Count("ratings")
    )


def pin_list(request):
    qs = annotated_pins()
    q = request.GET.get("q", "").strip()
    order = request.GET.get("orden", "recientes")
    if q:
        qs = qs.filter(title__icontains=q)
    if order == "mejores":
        qs = qs.filter(n_ratings__gt=0).order_by("-avg", "-n_ratings")
    page = Paginator(qs, 24).get_page(request.GET.get("page"))
    return render(request, "pins/pin_list.html", {"page": page, "q": q, "order": order})


def pin_detail(request, pk):
    pin = get_object_or_404(annotated_pins(), pk=pk)
    my_rating = None
    if request.user.is_authenticated:
        my_rating = Rating.objects.filter(pin=pin, user=request.user).values_list("stars", flat=True).first()
    return render(request, "pins/pin_detail.html", {"pin": pin, "my_rating": my_rating})


@login_required
def pin_create(request):
    form = PinForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        pin = form.save(commit=False)
        pin.author = request.user
        pin.save()
        messages.success(request, "Publicado.")
        return redirect(pin)
    return render(request, "pins/pin_form.html", {"form": form})


@login_required
@require_POST
def pin_delete(request, pk):
    pin = get_object_or_404(Pin, pk=pk, author=request.user)
    pin.delete()
    messages.success(request, "Publicación eliminada.")
    return redirect("pin_list")


@login_required
@require_POST
def pin_rate(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    if pin.author_id == request.user.id:
        messages.error(request, "No puedes puntuar tu propia publicación.")
        return redirect(pin)
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            pin=pin, user=request.user, defaults={"stars": form.cleaned_data["stars"]}
        )
        messages.success(request, "Gracias por tu puntuación.")
    else:
        messages.error(request, "Elige entre 1 y 5 estrellas.")
    return redirect(pin)


def user_profile(request, username):
    from django.contrib.auth.models import User
    owner = get_object_or_404(User, username=username)
    pins = annotated_pins().filter(author=owner)
    return render(request, "pins/profile.html", {"owner": owner, "pins": pins})


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("pin_list")
    return render(request, "registration/signup.html", {"form": form})
