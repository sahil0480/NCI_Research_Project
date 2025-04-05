from django.contrib import admin
from .models import MenuItem,Order

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')
    list_filter = ('category',)

admin.site.register(MenuItem, MenuItemAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at')
    search_fields = ('user__username',)