from django.db import models
# import django.utils.timezone as timezone
# import datetime
# Create your models here.

class upload(models.Model):
	user_name = models.CharField(max_length=20)
	user_nickname = models.CharField(max_length=20, default="")
	user_sex = models.CharField(max_length=20)
	user_city = models.CharField(max_length=20)
	user_filename = models.CharField(max_length=5000)
	user_hobby = models.CharField(max_length=200)
	user_password = models.CharField(max_length=128, default="")
	user_role = models.CharField(max_length=20, default="")
	
	
	def __str__(self):
		return self.user_name

#upload.objects.exlude(user_name='admin')