from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

class CallLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transcript = models.TextField(blank=True, null=True)
    bot_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
