from django.contrib import admin
from .models import Event, Bouquet, Order, Client


admin.site.register(Event)
admin.site.register(Bouquet)
admin.site.register(Order)
admin.site.register(Client)
