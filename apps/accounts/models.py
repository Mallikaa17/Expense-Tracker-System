# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    source = models.CharField(max_length=100)
    date = models.DateField()

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.FloatField()
    month = models.DateField()

class RecurringExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    frequency = models.CharField(max_length=50)  # monthly, weekly
    category = models.CharField(max_length=100)
    start_date = models.DateField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10)



