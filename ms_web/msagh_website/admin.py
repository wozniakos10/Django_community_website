from django.contrib import admin
from .models import Spot, Meme, CommentSpot,CommentMeme


# Register your models here.

def approve_selected_post(modeladmin, request, queryset):
    for post in queryset:
        post.admin_aproved = True
        post.save()


class InputFilter(admin.SimpleListFilter):
    """ Input filter on the left site of admin page"""
    title = 'User:'
    parameter_name = 'user__username'
    template = 'msagh_website/admin_input_filter.html'

    def lookups(self, request, model_admin):
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice['query_params'] = query_params
        yield all_choice

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(user__username=value)


class MemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user', 'image', 'admin_aproved')
    readonly_fields = ('user', )
    list_filter = [
        "admin_aproved", InputFilter, "user"
    ]
    search_fields = ['title', 'user__username']  # search label on the center of page
    list_per_page = 20  # no. posts in one admin page
    actions = [approve_selected_post]


class CommentMemeAdmin(admin.ModelAdmin):
    list_display = ('user', 'meme', 'pub_date','meme')
    readonly_fields = ('meme', 'user')
    search_fields = ['content', 'user__username', 'meme']  # search label on the center of page
    list_per_page = 20  # no. posts in one admin page
    list_filter = [
        'user', InputFilter, 'meme',
    ]


class CommentSpotAdmin(admin.ModelAdmin):
    list_display = ('user', 'spot', 'pub_date', 'spot')
    readonly_fields = ('spot', 'user')
    search_fields = ['content', 'user__username', 'spot']  # search label on the center of page
    list_per_page = 20  # no. posts in one admin page
    list_filter = [
        'user', InputFilter, 'spot',
    ]


class CommentSpotInline(admin.TabularInline):
    model = CommentSpot
    fields = ('content','user', 'pub_date')
    readonly_fields = ('user','spot', 'pub_date')

class SpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user', 'content', 'admin_aproved')
    list_filter = [
        "admin_aproved", InputFilter, "user"
    ]
    readonly_fields = ('user',)
    inlines = [CommentSpotInline]
    search_fields = ['title', 'user__username']  # search label on the center of page
    list_per_page = 20  # no. posts in one admin page
    actions = [approve_selected_post]





admin.site.register(Spot, SpotAdmin)
admin.site.register(Meme, MemeAdmin)
admin.site.register(CommentSpot, CommentSpotAdmin)
admin.site.register(CommentMeme,CommentMemeAdmin)
