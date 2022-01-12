from django.contrib import admin

from .models import Location, Weathertype, Event, Userprofile, Usersearchhistory

# Register your models here.
admin.site.register(Location)
admin.site.register(Weathertype)
admin.site.register(Event)
admin.site.register(Userprofile)
admin.site.register(Usersearchhistory)