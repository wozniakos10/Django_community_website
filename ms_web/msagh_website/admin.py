from django.contrib import admin
from .models import Spot,Meme
# Register your models here.

def approve_selected_post(modeladmin, request, queryset):
    for post in queryset:
        post.admin_aproved = True
        post.save()




class MemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user','image','admin_aproved')
    actions = [approve_selected_post]


class SpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user','content','admin_aproved')
    list_filter = [
        "admin_aproved"
        ]
    actions = [approve_selected_post]


admin.site.register(Spot,SpotAdmin)
admin.site.register(Meme,MemeAdmin)


