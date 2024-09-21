from django.urls import path

from flower_models.views import index, card, consultation, order, order_step, quiz, result, catalog

app_name = 'flower_models'

urlpatterns = [
    path('', index, name='index'),
    path('card/<int:bouquet_id>', card, name='card'),
    path('consultation', consultation, name='consultation'),
    path('order', order, name='order'),
    path('order_step', order_step, name='order_step'),
    path('quiz', quiz, name='quiz'),
    path('result', result, name='result'),
    path('catalog', catalog, name='catalog')
]
