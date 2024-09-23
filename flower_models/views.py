from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserForm
from .models import Bouquet, Consultation
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
    return render(request, 'flowers_models/index.html', context)


# TODO
def card(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)

    return render(
        request,
        'flowers_models/card.html',
        {
            'bouquet': bouquet
        })


# TODO
def consultation(request):
    if request.method == "POST":
        name = request.POST.get('fname')
        phone = request.POST.get('tel')
        Consultation.objects.create(name=name, phone=phone)
        messages.success(request, 'Запись на консультацию отправлена. Наш менеджер свяжется с вами в ближайшее время.')
        return redirect('index')

    return render(request, 'consultation.html')


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
