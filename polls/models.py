from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Balance(models.Model):
	""" Balance range: -MAX_INTEGER < balance < MAX_INTEGER"""
	balance = models.IntegerField(default=0)
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

	def __str__(self):
		return str(self.balance)

class Category(models.Model):
	text = models.CharField(max_length=20)
	def __str__(self):
		return self.text

class Log(models.Model):
	history_name = models.CharField(max_length=50, default="Default Log Name")
	date = models.DateTimeField(default=datetime.now, blank=True)
	category = models.CharField(max_length=20, default="Others")
	income_or_outcome = models.CharField(max_length=8, default="Income")
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
	amount = models.IntegerField(default=1)
	def __str__(self):
		return self.history_name
