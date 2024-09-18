from django.shortcuts import render


# TODO
def index(request):
    return render(request, 'flowers_models/index.html')


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
