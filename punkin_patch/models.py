from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Character(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = user_directory_path, blank=True)

    def __str__(self):
        return self.name

class PatchTemplate(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return self.name