from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','fullName','verified','photo','department','roll','createdAt','updatedAt']