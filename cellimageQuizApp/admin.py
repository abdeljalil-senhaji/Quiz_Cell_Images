from django.contrib import admin
from .models import Image
from .forms import FormImage


# Register your models here.

#######################################################
##### Edit Image DB directly in admin interface #######
#######################################################
class PersonAdmin(admin.ModelAdmin):
    form = FormImage


admin.site.register(Image, PersonAdmin)
