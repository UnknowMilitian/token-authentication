from django.db import models


class Item(models.Model):
    title = models.CharField("Item title", max_length=250)
    description = models.TextField("Item description", null=True, blank=True)

    def __str__(self):
        return self.title
