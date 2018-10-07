from django.db import models
 
class Urls(models.Model):
    short_id = models.SlugField(max_length=8,primary_key=True)
    httpurl = models.URLField(max_length=200)