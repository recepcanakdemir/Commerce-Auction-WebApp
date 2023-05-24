from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    #first_name = models.CharField(max_length=64)
    #second_name = models.CharField(max_length=64)
    #bids = models.ManyToManyField(Bid, blank=True,related_name="users")

   
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Listing(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= False, default=True)
    value= models.DecimalField(max_digits=19, decimal_places=2)
    publishing_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=550,null=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator",null=True)
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.name} price: {self.price}$ published at {self.publishing_date}"
    def get_absolute_url(self):
        return reverse('listing',kwargs={'listing_id':self.pk})

class Comment(models.Model):
    user = models.TextField(max_length=200) 
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comment",null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
class Bid(models.Model):
    user = models.TextField(max_length=200)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="price",null=True)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    class Meta:
        ordering = ['price']
    def __str__(self):
        return str(self.price)

   