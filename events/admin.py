from django.contrib import admin
from .models import Event

# Register your models here.
class Events_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'date']
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')

admin.site.register(Event, Events_Admin)
