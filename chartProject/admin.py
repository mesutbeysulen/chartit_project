from django.contrib import admin

# Register your models here.
from chartProject.models import SalesReport, SalesHistory

admin.site.register(SalesReport)
admin.site.register(SalesHistory)
