from django.contrib import admin
from .models import Person, EmailVerification
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = [
        # 'id',
        'username',
        'is_staff',
        'email'
    ]

admin.site.register(Person, PersonAdmin)

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = [
    'code' ,
    'user' ,
    'created',
    'expiration' ,
    ]

admin.site.register(EmailVerification, EmailVerificationAdmin)

