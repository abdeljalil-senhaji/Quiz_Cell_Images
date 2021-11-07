from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Image(models.Model):
    image_name = models.CharField(max_length=255)
    description = models.TextField()
    microscopy = models.CharField(max_length=255)
    cell_type = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    doi = models.CharField(max_length=255)
    organism = models.CharField(max_length=255)

class Question(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    imageField = models.CharField(max_length=255)
    points = models.IntegerField()
    n_answer = models.IntegerField()
    n_image = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

class Answer(models.Model):
    question_id = models.IntegerField()
    answer = models.CharField(max_length=255)
    definition = models.TextField()

    def __str__(self):
        return f'{self.answer}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, unique=True, default=None)
    total_score = models.IntegerField(default=0)  # initialization
    component_score = models.IntegerField(default=0)
    microscopy_score = models.IntegerField(default=0)
    level = models.CharField(max_length=50, default="beginner")

    def getScore(self):
        return total_score

    def getComponentScore(self):
        return component_score

    def getMicroscopyScore(self):
        return microscopy_score


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
