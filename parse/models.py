from django.db import models


class Page(models.Model):
    link = models.CharField(max_length=400)
    title = models.TextField()
    raw_text = models.TextField()
    category = models.CharField(max_length=100)
    dictionary = models.TextField()
    parsed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Data(models.Model):
    category = models.CharField(max_length=100)
    dictionary = models.TextField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.category
