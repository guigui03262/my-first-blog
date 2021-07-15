from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

	birth_date = models.DateField(null=True, verbose_name="Data de nascimento", help_text="Use o formato dia-mes-ano")

	def __str__(self):
		return self.username