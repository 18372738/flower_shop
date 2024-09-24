from django.contrib import admin
from .models import Event, Bouquet, Order, Client, Consultation

admin.site.register(Event)

admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Consultation)

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
