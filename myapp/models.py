from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class courseconcepts(models.Model):
    courseconcept=models.CharField(max_length=20)
    def __str__(self):
        return self.courseconcept



class courses(models.Model):
    coursename=models.CharField(max_length=50)
    courseimg=CloudinaryField('course')
    description=models.CharField(max_length=400)
    nametut=models.CharField(max_length=20)
    courseprice=models.IntegerField()
    corseconceptlist=models.ManyToManyField(courseconcepts)

    def __str__(self):
        return self.coursename
    

class CartItems(models.Model):
    userid=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    courseid=models.ForeignKey(courses,on_delete=models.CASCADE)


class EnrolledCourses(models.Model):
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    courseid = models.ForeignKey(courses, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('userid', 'courseid')  

    def __str__(self):
        return f"{self.userid.username} enrolled in {self.courseid.coursename}"