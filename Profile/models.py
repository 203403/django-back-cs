from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ProfileTable(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        )
    url_img = models.ImageField(null = True, blank=True, default = '', upload_to="img_profile/")
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(blank=True, null=True, default=None)
    
    class Meta:
        managed = True
        db_table = 'TablaProfiles'

