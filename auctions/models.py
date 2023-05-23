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

class Bid(models.Model):
    bid = models.FloatField()
    class Meta:
        ordering = ['bid']
    def __str__(self):
        return str(self.bid)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="comment_user",null=True)
    title = models.CharField(max_length=60)
    text= models.TextField(max_length=200)
    
    def __str__(self):
        return f"{self.title} {self.text}"
    

class Listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.ManyToManyField(Bid,blank=True,related_name="Bids")
    publishing_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=550,null=True)
    category = models.CharField(max_length=35)#models.ForeignKey(Category,on_delete=models.SET_DEFAULT,related_name="category")
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator",null=True)
    comment = models.ManyToManyField(Comment,blank=True, related_name="comments")
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.name} price: {self.price}$ published at {self.publishing_date}"
    def get_absolute_url(self):
        return reverse('listing',kwargs={'listing_id':self.pk})

class Category(models.Model):
    name = models.CharField(max_length=50)
    listings = models.ManyToManyField(Listing,blank=True,related_name="Listings")
    def __str__(self):
        return self.name

