from django.db import models

class TimeStampedModel(models.Model):
    """
    Abstract base model to handle created_at and updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True