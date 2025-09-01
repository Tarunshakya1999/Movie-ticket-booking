from django.db import models
from django.contrib.auth.models import User

# Create your models here.

'''Model for image carousel.'''
class ImageCarosel(models.Model):
    name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to="logo")
   
    def __str__(self):
        return self.name
    @staticmethod
    def getimage():
        return ImageCarosel.objects.all()
    
'''Model for Movies.'''

CATEGORY_CHOICES = [
    ('Hindi', 'Hindi Movie'),
    ('English', 'English Movie'),
    ('South', 'South Movie'),
    ('Animated', 'Animated Movie'),
    ('All', 'All Movies'),

 ]

class MoviesModel(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='logo')
    description = models.TextField()
    cast = models.TextField()
    trailer = models.URLField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    def __str__(self):
       return self.title

STATE_CHOICES = [

    ('Delhi', 'Delhi'),
    ('Mumbai', 'Mumbai'),
    ('MadhyePradesh', 'MadhyePradesh'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    

]
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)

    def __str__(self):
        return self.name
    


    
from django.db import models
from uuid import uuid4

class MovieTickets(models.Model):
    movie_name = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=10, unique=True)
    client_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    cinema_hall = models.CharField(max_length=50)
    date = models.DateField(default='')
    time = models.TimeField(default='')
    seats = models.PositiveIntegerField(default=1)
    payment_status = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)  # New field to track cancellations

    def __str__(self):
        return f"{self.movie_name}-{self.ticket_id}-{self.client_name}-{self.seats} seats"

    @staticmethod
    def getdetails():
        return MovieTickets.objects.all()



class Partner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='partners/')
    description = models.TextField()

    def __str__(self):
        return self.name
    
    @staticmethod
    def partners():
        return Partner.objects.all()
   