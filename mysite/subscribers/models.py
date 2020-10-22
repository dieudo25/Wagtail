from django.db import models

class Subscriber(models.Model):
    """A subscriber model"""

    email = models.EmailField(blank=False, null=False, help_text='Email address', max_length=100)
    full_name = models.CharField(max_length=100, blank=False, null=False, help_text="First and last name")

    def __str__(self):
        """Str representation of object"""
        return self.full_name
    