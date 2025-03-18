from django.db import models

from Teacher.models import MusicSection, Teacher

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255) 
    address = models.TextField(blank=True, null=True)
    skill_level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner')
    date_registered = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    music_section = models.ForeignKey(MusicSection, on_delete=models.CASCADE)
    booking_date = models.DateField()  
    time_slot = models.TimeField() 
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled")
    ], default="Pending")
    payment_status = models.CharField(
        max_length=20, 
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")], 
        default="Pending"
    )





class ChatMessage(models.Model):
    sender_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_messages", null=True, blank=True)  
    sender_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_sent_messages", null=True, blank=True)
    receiver_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)  
    receiver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_received_messages", null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.get_sender()} to {self.get_receiver()}: {self.text[:20]}"

    def get_sender(self):
        return self.sender_student or self.sender_teacher

    def get_receiver(self):
        return self.receiver_student or self.receiver_teacher


class TeacherFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="feedbacks")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'teacher')  # Ensure a student rates a teacher only once

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self.teacher, 'update_rating'):  # ✅ Ensure method exists before calling
            self.teacher.update_rating()



class Complaint(models.Model):
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Who is complaining
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    complaint_text = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)