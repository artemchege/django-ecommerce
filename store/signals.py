from django.db.models.signals import post_save
from django.contrib.auth.models import User
from store import models


def create_customer_to_user(sender, instance, created, **kwargs):
    name = instance.username
    email = instance.email
    if created:
        models.Customer.objects.create(user=instance, name=name, email=email)


post_save.connect(create_customer_to_user, sender=User)

















