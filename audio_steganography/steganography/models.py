from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RSAKeyPair(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key = models.TextField()

    def __str__(self) -> str:
        return self.user.username