from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Deucer)
admin.site.register(Establishment)
admin.site.register(Review)
admin.site.register(Restroom)
admin.site.register(Gender)
admin.site.register(Rating)
admin.site.register(Feature)
