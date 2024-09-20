from django.shortcuts import render

from .models import Bouquet


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

    print(bouquet_serialized)
    return render(request, template_name="flowers_models/index.html", context={
        'bouquets': bouquet_serialized,
    })


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
    return render(request, 'flowers_models/catalog.html')
