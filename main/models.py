from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Directory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    directory_name = models.CharField(max_length=50)
    parent_directory = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    image_path = models.ImageField(null=True, default=None ,upload_to='images/')
    is_directory = models.BooleanField(default=1, null=False)