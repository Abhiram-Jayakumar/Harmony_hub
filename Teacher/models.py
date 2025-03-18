from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=100, unique=True)
    subjects = models.TextField()
    experience = models.IntegerField()  
    teacher_image = models.ImageField(upload_to='teacher_images/', blank=True, null=True)  
    teacher_bio = models.TextField(blank=True, null=True)  
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  
    password = models.CharField(max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)
    teacher_approved_status = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)    
    
def update_rating(self):
    feedbacks = self.feedbacks.all()  # Get all feedback related to this teacher
    total_ratings = feedbacks.count()
        
    if total_ratings > 0:
        avg_rating = sum(feedback.rating for feedback in feedbacks) / total_ratings
        self.average_rating = round(avg_rating, 2)
    else:
        self.average_rating = 0.0  # Reset if no feedback

    self.save() 




class MusicSection(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  
    section_name = models.CharField(max_length=255)  
    instrument = models.CharField(max_length=100) 
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2) 
    available_days = models.CharField(max_length=255) 
    available_time = models.TimeField() 
    location = models.CharField(max_length=255, blank=True, null=True) 
    section_image = models.ImageField(upload_to='section_images/', blank=True, null=True)  
    description = models.TextField(blank=True, null=True) 
    is_active = models.BooleanField(default=True)