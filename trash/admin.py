from django.contrib import admin
from .models import *


class TrashItemAdmin(admin.ModelAdmin):
    list_display = ("name", "bin", "created_date")
    list_filter = ['created_date']
    search_fields = ['name']


class TrashBinAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "color", "avatar_name")

admin.site.register(TrashItem, TrashItemAdmin)
admin.site.register(TrashBin, TrashBinAdmin)
admin.site.register(TrashMaterial)
