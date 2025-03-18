from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from Student.models import Booking, ChatMessage, Student
from Teacher.models import MusicSection, Teacher
from django.db.models import Q
# Create your views here.

def Teacher_home(request):
    return render(request,'Teacher/Teacher_Home.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////


def add_teacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        id_number = request.POST.get('id_number')
        subjects = request.POST.get('subjects')
        experience = request.POST.get('experience')
        teacher_bio = request.POST.get('teacher_bio')
        address = request.POST.get('address')
        location = request.POST.get('location')
        password = request.POST.get('password')
        teacher_image = request.FILES.get('teacher_image')

       
        teacher = Teacher(
            name=name,
            email=email,
            phone_number=phone_number,
            id_number=id_number,
            subjects=subjects,
            experience=experience,
            teacher_bio=teacher_bio,
            address=address,
            location=location,
            password=password,
            teacher_image=teacher_image
        )
        teacher.save()
        return redirect('Student:Index')

    return render(request, "Teacher/Teacher_Register.html")
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def add_music_section(request):
    if 'Tid' not in request.session:  
        return redirect('Student:login')  
    if request.method == "POST":
        teacher_id = request.session['Tid']
        teacher = Teacher.objects.get(id=teacher_id)

        section_name = request.POST.get('section_name')
        instrument = request.POST.get('instrument')
        rate_per_hour = request.POST.get('rate_per_hour')
        available_days = request.POST.get('available_days')
        available_time = request.POST.get('available_time')
        location = request.POST.get('location')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') 
       
        section_image = request.FILES.get('section_image')

       
        is_active = True if is_active == "on" else False

        
        MusicSection.objects.create(
            teacher=teacher,
            section_name=section_name,
            instrument=instrument,
            rate_per_hour=rate_per_hour,
            available_days=available_days,
            available_time=available_time,
            location=location,
            description=description,
            
            section_image=section_image,
            is_active=is_active
        )

        return redirect('Teacher:Teacher_home') 
    return render(request, "Teacher/Add_music_section.html") 

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def teacher_bookings(request):
    if "Tid" not in request.session: 
        return redirect("Student:Index") 
    teacher_id = request.session["Tid"] 
    bookings = Booking.objects.filter(teacher_id=teacher_id).order_by("-booking_date")  

    return render(request, "Teacher/Teacher_bookings.html", {"bookings": bookings})



def update_booking_status(request, booking_id, status):
    if "Tid" not in request.session:  
        return redirect("Student:Index")

    booking = get_object_or_404(Booking, id=booking_id, teacher_id=request.session["Tid"]) 

    if status in ["Confirmed", "Cancelled"]:
        booking.status = status
        booking.save()
        messages.success(request, f"Booking has been {status.lower()} successfully.")
    else:
        messages.error(request, "Invalid status update.")

    return redirect("Teacher:teacher_bookings")


#///////////////////////////////////////////////////////////////////////////////////

def teacher_chat(request, student_id):
    teacher_id = request.session.get("Tid")  # Ensure the teacher is logged in

    if not teacher_id:
        messages.error(request, "You must be logged in as a teacher to view messages.")
        return redirect("Teacher:Index")

    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = get_object_or_404(Student, id=student_id)

    # Get chat messages between the teacher and student
    messages_list = ChatMessage.objects.filter(
        Q(sender_student=student, receiver_teacher=teacher) |
        Q(sender_teacher=teacher, receiver_student=student)
    ).order_by("timestamp")

    return render(request, "Teacher/teacher_chat.html", {
        "student": student,
        "teacher": teacher,
        "messages": messages_list
    })
    
def send_message_teacher(request, student_id):
    teacher_id = request.session.get("Tid")  # Ensure teacher is logged in
    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(sender_teacher=teacher, receiver_student=student, text=message_text)

    return redirect("Teacher:teacher_chat", student_id=student.id)


#///////////////////////////////////////////////////////////////////////////////////////

def teacher_profile(request):
    """View for displaying the teacher profile"""
    if "Tid" not in request.session:
        messages.error(request, "You must be logged in to view your profile.")
        return redirect("Teacher:Index")

    teacher_id = request.session["Tid"]
    teacher = get_object_or_404(Teacher, id=teacher_id)

    return render(request, "Teacher/teacher_profile.html", {"teacher": teacher})


def update_teacher_profile(request):
    """View for updating teacher profile"""
    if "Tid" not in request.session:
        messages.error(request, "You must be logged in to update your profile.")
        return redirect("Teacher:Index")

    teacher_id = request.session["Tid"]
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == "POST":
        teacher.name = request.POST.get("name")
        teacher.email = request.POST.get("email")
        teacher.phone_number = request.POST.get("phone_number")
        teacher.experience = request.POST.get("experience")
        teacher.address = request.POST.get("address")
        teacher.location = request.POST.get("location")
        teacher.teacher_bio = request.POST.get("teacher_bio")
        
        if "teacher_image" in request.FILES:
            teacher.teacher_image = request.FILES["teacher_image"]
        
        teacher.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("Teacher:teacher_profile")

    return render(request, "Teacher/update_profile.html", {"teacher": teacher})


def update_teacher_password(request):
    """View for updating teacher password (without hashing)"""
    if "Tid" not in request.session:
        messages.error(request, "You must be logged in to update your password.")
        return redirect("Teacher:Index")

    teacher_id = request.session["Tid"]
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("Teacher:update_teacher_password")

        teacher.password = new_password  # Not hashing password as per your request
        teacher.save()
        messages.success(request, "Password updated successfully!")
        return redirect("Teacher:teacher_profile")

    return render(request, "Teacher/update_password.html")


#///////////////////////////////////////////////////////////////////////////////////////

def view_music_sections(request):
    if "Tid" not in request.session:  
        messages.error(request, "You must be logged in to view your music sections.")
        return redirect("Teacher:login")  

    teacher_id = request.session["Tid"]  
    teacher = get_object_or_404(Teacher, id=teacher_id)
    sections = MusicSection.objects.filter(teacher=teacher)

    return render(request, "Teacher/view_music_sections.html", {"sections": sections})


def edit_music_section(request, section_id):
    if "Tid" not in request.session:  
        messages.error(request, "You must be logged in to edit your music section.")
        return redirect("Teacher:login")  

    teacher_id = request.session["Tid"]  
    section = get_object_or_404(MusicSection, id=section_id, teacher_id=teacher_id)

    if request.method == "POST":
        section.section_name = request.POST.get("section_name")
        section.instrument = request.POST.get("instrument")
        section.rate_per_hour = request.POST.get("rate_per_hour")
        section.available_days = request.POST.get("available_days")
        section.available_time = request.POST.get("available_time")
        section.location = request.POST.get("location")
        section.description = request.POST.get("description")
        section.is_active = request.POST.get("is_active") == "on"

        if "section_image" in request.FILES:
            section.section_image = request.FILES["section_image"]

        section.save()
        messages.success(request, "Music section updated successfully!")
        return redirect("Teacher:view_music_sections")

    return render(request, "Teacher/edit_music_section.html", {"section": section})