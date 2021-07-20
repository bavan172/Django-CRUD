from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *

#admin.site.register(Customer)
#admin.site.register(Product)
#admin.site.register(Order)
#admin.site.register(Tag)
#admin.site.site_header = 'Admin'
#admin.site.site_title = 'Admin site'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
    
#    list_display = ['id', 'title', 'created_at']
#    list_display_links = ['id', 'title']
#    list_filter = ['title']
#    search_fields = ['title']
#    class Meta:
#        model = ModelName