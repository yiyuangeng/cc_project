from django.contrib import admin
from calendarapp.models import Event, EventMember

admin.site.register(EventMember)
admin.site.register(Event)