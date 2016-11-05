from django.contrib import admin
from .models import *


class TrashItemAdmin(admin.ModelAdmin):
    list_display = ("name", "material", "bin", "created_date")
    list_filter = ['created_date']
    search_fields = ['name']


admin.site.register(TrashItem, TrashItemAdmin)
admin.site.register(TrashBin)
admin.site.register(TrashMaterial)
