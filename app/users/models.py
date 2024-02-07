import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now

class Person(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified_email = models.BooleanField(default=False)
    
class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    
    def send_verification_mail(self):        
        link = reverse('users:email_verification', kwargs={'email':self.user.email, 'code':self.code} )
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        print(verification_link)
        subject = "Подтверждение Регистрации"
        message = f"для подтверждения перейдите по ссылке: {verification_link}"
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[self.user.email]
        print(settings)
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
    def is_expired(self):
        return True if now() >= self.expiration else False