from django.contrib import admin
from .models import Spot
# Register your models here.

class SpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user','content')


admin.site.register(Spot,SpotAdmin)

