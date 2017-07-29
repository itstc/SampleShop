from django.contrib import admin
from .models import Category, Product
from django.contrib import admin

# Actions
def clear_image(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    for obj in queryset:
        obj.image = None
        obj.save()

clear_image.short_description = 'Clear Image'

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']

    prepopulated_fields = {'slug':('name',)}

    actions = [clear_image]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.site_header = 'Sample Shop'
