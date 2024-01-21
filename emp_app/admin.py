from django.contrib import admin
from . models import employee,Role,department

# Register your models here.
admin.site.register(employee)
admin.site.register(Role)
admin.site.register(department)