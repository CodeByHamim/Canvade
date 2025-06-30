from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .admin import assign_role

@receiver(post_save, sender=CustomUser)
def set_user_group(sender, instance, created, **kwargs):
    if created:
        assign_role(instance)
