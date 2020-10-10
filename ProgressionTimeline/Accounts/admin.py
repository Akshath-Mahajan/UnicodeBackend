from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class Admin(UserAdmin):
    model = User
    list_display = ('email','username', 'full_name','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username', 'full_name')
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, Admin)