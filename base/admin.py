from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(topic)
admin.site.register(rooms)
admin.site.register(message)

# Register your models here.
