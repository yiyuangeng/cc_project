from django.contrib import admin
from calendarapp.models import Event, EventMember

# class EventMemberAdmin(admin.ModelAdmin):
    # model = EventMember
    # list_display = ['event', 'user']
    # list_display = ['event']
    # pass

# admin.site.register(Event)
# admin.site.register(EventMember, EventMemberAdmin)
admin.site.register(EventMember)
admin.site.register(Event)