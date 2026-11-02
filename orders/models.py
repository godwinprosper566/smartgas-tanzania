from django.db import models

class Order(models.Model):
    CUSTOMER_TYPES = [
        ('Household', 'Household'),
        ('Vehicle', 'Vehicle (CNG)'),
        ('Business', 'Business'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='Household')
    size_kg = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending')
    payment_status = models.CharField(max_length=20, default='Unpaid')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.size_kg}kg"