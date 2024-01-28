from django.db import models
from django.contrib.auth.models import User
class Members(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    email = models.EmailField()
    year = models.IntegerField()
    mentee = models.CharField(max_length=100)    
    mentor = models.CharField(max_length=100)
    mentoremail=models.CharField(max_length=100)
    image=models.ImageField(upload_to='profile_image', blank=True)
    n_approved= models.IntegerField()  
    def _str__(self):
        return f"{self.first_name}"
    
class Leave(models.Model):
        user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
        start_date = models.DateField(null=True,blank=False)
        end_date = models.DateField(null=True,blank=False)
        reason = models.TextField(null=True,blank=True)
        status = models.CharField(max_length=12,default='pending')  
         
        def __str__(self):
                return f"{self.user}'s leave request from {self.start_date} to {self.end_date}"
