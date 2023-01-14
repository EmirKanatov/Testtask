from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(null=True, blank=True, upload_to='images/avatar')
    bio = models.TextField(null=True, blank=True)
    nickname = models.CharField(max_length=128, blank=False, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.userprofile.save()

    objects = Manager()
