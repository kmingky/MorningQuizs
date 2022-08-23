from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = "categorys"

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    class Meta:
        db_table = "articles"

    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
