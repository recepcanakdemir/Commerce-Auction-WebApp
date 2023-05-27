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

class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="watchlist_user",null=True)

class Listing(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= False, default=True)
    starting_price= models.DecimalField(max_digits=19, decimal_places=2)
    publishing_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=550,null=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator",null=True)
    image = models.URLField(null=True, blank=True)
    is_closed = models.BooleanField(null=True,default=False)
    is_in_watchlist = models.BooleanField(null=True,default=False)
    watchlist = models.ManyToManyField(User,blank=True, related_name="watchlist")
    def __str__(self):
        return f"{self.name} price: {self.starting_price}$ published at {self.publishing_date}"
    def get_absolute_url(self):
        return reverse('listing',kwargs={'listing_id':self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_creator",null=True) 
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comment",null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="customer", null=True)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="bid",null =True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    class Meta:
        ordering = ['price']
    def __str__(self):
        return str(self.price)

#class Bid(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user",null=True)
    #listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="price",null=True)
    #price = models.DecimalField(max_digits=19, decimal_places=10)
    #class Meta:
        #ordering = ['price']
    #def __str__(self):
        #return str(self.price)

   