from datetime import datetime, time

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserForm
from .models import Bouquet, Order, Client
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
    return render(request, 'flowers_models/consultation.html')


# TODO
def order(request):
    context = {}
    if request.method == "POST":
         context['bouquet_title'] = request.POST['bouquet_title']
         context['bouquet_price'] = request.POST['bouquet_price']
         print(type(request.POST))
         print(context)
         return render(request, 'flowers_models/order.html', context=context)

    print(context)
    return render(request, 'flowers_models/order.html', context=context)


# TODO
def order_step(request):
    context = {}
    status = "подтверждение"

    if request.method == "POST":
        bouquet_title = request.POST['bouquet_title']
        name = request.POST['name']
        phone = request.POST['phone']
        bouquet = Bouquet.objects.get(title=bouquet_title)
        order_time = request.POST['orderTime']
        # today = datetime.date.today()
        if order_time:
            delivery_date = datetime.now()

        try:
            # Пытаемся найти клиента по имени и телефону
            client1 = Client.objects.get(full_name=name, phone=phone)
        except Client.DoesNotExist:
            # Если клиент не найден, создаем нового
            client1 = Client.objects.create(full_name=name, phone=phone)

        # Дальнейшие действия с client1 (например, создание заказа)
        order = Order.objects.create(
            client=client1,
            delivery_date=delivery_date,
            status=status,
            address=request.POST['address'],
            bouquet=bouquet
        )

        return render(request, 'flowers_models/order-step.html') #context=context)

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
