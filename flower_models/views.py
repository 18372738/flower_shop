from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserForm
from .models import Bouquet
from django.contrib import messages


# TODO
def index(request):
    bouquets = Bouquet.objects.prefetch_related('event')
    bouquet_serialized = []
    for bouguet in bouquets:
        bouquet_serialized.append({
            'id': bouguet.id,
            'title': bouguet.title,
            'price': bouguet.price,
            "images": bouguet.photo.url,
        })

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка успешно создана')
            return redirect(reverse('flower_models:index'))
        context = {'form': form, 'bouquets': bouquet_serialized}
        return render(request, 'flowers_models/index.html', context)
    context = {
        'form': UserForm(),
        'bouquets': bouquet_serialized
    }
    print(bouquet_serialized)
    return render(request, 'flowers_models/index.html', context)



# TODO
def card(request):
    return render(request, 'flowers_models/card.html')


# TODO
def consultation(request):
    return render(request, 'flowers_models/consultation.html')


# TODO
def order(request):
    return render(request, 'flowers_models/order.html')


# TODO
def order_step(request):
    return render(request, 'flowers_models/order-step.html')


# TODO
def quiz(request):
    return render(request, 'flowers_models/quiz.html')


# TODO
def result(request):
    return render(request, 'flowers_models/result.html')

# TODO
def catalog(request):
    bouquets = Bouquet.objects.prefetch_related('event')
    bouquet_serialized = []
    for bouguet in bouquets:
        bouquet_serialized.append({
            'id': bouguet.id,
            'title': bouguet.title,
            'price': bouguet.price,
            "images": bouguet.photo.url,
        })
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка успешно создана')
            return redirect(reverse('flower_models:index'))
        context = {'form': form, 'bouquets': bouquet_serialized}
        return render(request, 'flowers_models/index.html', context)
    context = {
        'form': UserForm(),
        'bouquets': bouquet_serialized
    }
    return render(request, 'flowers_models/catalog.html', context)
