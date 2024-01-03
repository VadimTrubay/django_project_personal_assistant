from django.contrib import admin

from .models import CustomUser
# Register your models here.




@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):


    list_display = ('id', 'email', 'role', 'is_active', 'is_superuser')
    list_filter = ('role', 'is_active')
    ordering = ('id',)
    search_fields = ('id', 'email', 'role')
    actions = ('mute', 'unmute', 'set_role_admin')

    def mute(self, request, queryset):
        queryset.update(is_active=False)

    mute.short_description = 'mute user'

    def unmute(self, request, queryset):
        queryset.update(is_active=True)

    unmute.short_description = 'Снять игнорирование по артикулу'


    def set_role_admin(self, request, queryset):
        queryset.update(role='admin')

    set_role_admin.short_description = 'Set admin'





# additional setup for all project
admin.site.site_header = "Personal-Assistent"
admin.site.site_title = "Assistent System"
admin.site.index_title = 'Assistent Dashboard'

