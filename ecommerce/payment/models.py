from django.db import models

from django.contrib.auth.models import User

from store.models import Product


class ShippingAddress(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    address1 = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)

    city = models.CharField(max_length=255)


    # Optional

    state = models.CharField(max_length=255, null=True, blank=True)

    zipcode = models.CharField(max_length=255, null=True, blank=True)


    # FK

    # Authenticated / not authenticated users (bear in mind)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)



    class Meta:

        verbose_name_plural = 'Shipping Address'



    def __str__(self):

        return 'Shipping Address - ' + str(self.id)



class Order(models.Model):
    PAYMENT_CHOICES = [
            ('paypal', 'PayPal'),
            ('mobile_money', 'Mobile Money'),
        ]
        
    MOBILE_PROVIDERS = [
            ('mtn', 'MTN'),
            ('airtel', 'Airtel'),
            ('vodafone', 'Vodafone'),
            ('tigo', 'Tigo'),
            ('other', 'Other'),
        ]
    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


     # Payment-specific fields
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='paypal')
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    mobile_provider = models.CharField(max_length=20, choices=MOBILE_PROVIDERS, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order #{self.id} - {self.full_name}'
    
class OrderItem(models.Model):
    # FK -> 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)    
    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):

        return 'Order Item - #' + str(self.id)



        