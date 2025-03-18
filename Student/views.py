
from Admin.models import Admintable
from Student.models import Booking, ChatMessage, Complaint, Student, TeacherFeedback
from Teacher.models import MusicSection, Teacher
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from datetime import date
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def Index(request):
    return render(request,'Student/Index.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def student_registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password') 
        address = request.POST.get('address')
        skill_level = request.POST.get('skill_level')

        
        if Student.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if Student.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'error': 'Phone number already exists'}, status=400)

       
        student = Student(
            name=name,
            email=email,
            phone_number=phone_number,
            password=password,
            address=address,
            skill_level=skill_level
        )
        student.save()
        return redirect("Student:login")
    return render(request, "Student/Student_register.html") 




def student_home(request):
    return render(request,"Student/student_home.html")
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def Login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Tlogin=Teacher.objects.filter(email=email,password=password,teacher_approved_status=True).count()
        Slogin=Student.objects.filter(email=email,password=password).count()
        Alogin=Admintable.objects.filter(email=email,password=password).count()


        if Tlogin > 0:
            Tadmin=Teacher.objects.get(email=email,password=password,teacher_approved_status=1)
            request.session['Tid']=Tadmin.id
            return redirect('Teacher:Teacher_home')
        elif Slogin > 0:
            Sadmin=Student.objects.get(email=email,password=password)
            request.session['Sid']=Sadmin.id
            return redirect('Student:student_home')
        elif Alogin > 0:
            Aadmin=Admintable.objects.get(email=email,password=password)
            request.session['aid']=Aadmin.id
            return redirect('Admin:Admin_home')
         
        else:
            error="Invalid Credentials!!"
            return render(request,"Student/Login.html",{'ERR':error})
    else:
        return render(request, "Student/Login.html")
    
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
def search_teachers(request):
    query = MusicSection.objects.filter(is_active=True)  

    location = request.GET.get('location', '').strip()
    instrument = request.GET.get('instrument', '').strip()

    if location:
        query = query.filter(location__icontains=location)
    if instrument:
        query = query.filter(instrument__icontains=instrument)

    print("Search Query Results:", query)  

    return render(request, 'Student/Search_teachers.html', {'sections': query, 'location': location, 'instrument': instrument})

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def section_detail(request, section_id):
    section = get_object_or_404(MusicSection, id=section_id)
    feedbacks = TeacherFeedback.objects.filter(teacher=section.teacher)  # Get teacher feedback

    return render(request, 'Student/section_detail.html', {
        'section': section,
        'feedbacks': feedbacks
    })
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def book_teacher(request, section_id):
    if "Sid" not in request.session:  
        messages.error(request, "You must be logged in to book a lesson.")
        return redirect("Student:Index")  

    section = get_object_or_404(MusicSection, id=section_id)
    student = get_object_or_404(Student, id=request.session["Sid"])  

    if request.method == "POST":
        booking_date = request.POST.get("booking_date")
        time_slot = request.POST.get("time_slot")

        if Booking.objects.filter(student=student, teacher=section.teacher, booking_date=booking_date, time_slot=time_slot).exists():
            messages.error(request, "You have already booked a lesson at this time.")
            return redirect("section_detail", section_id=section.id)

        Booking.objects.create(
            student=student,
            teacher=section.teacher,
            music_section=section,
            booking_date=booking_date,
            time_slot=time_slot,
            status="Pending"
        )

        return redirect("Student:student_bookings")

    return render(request, "Student/Booking_form.html", {"section": section})

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def student_bookings(request):
    if "Sid" not in request.session:  
        messages.error(request, "You must be logged in to view your bookings.")
        return redirect("Student:Index")  

    student_id = request.session["Sid"]  
    bookings = Booking.objects.filter(student_id=student_id).order_by("-booking_date")  

    if not bookings:
        messages.info(request, "You have no bookings yet.")

    return render(request, "Student/Student_bookings.html", {"bookings": bookings})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student_id=request.session.get("Sid"))
    
    if booking.status != "Confirmed":
        messages.error(request, "Payment is only allowed for confirmed bookings.")
        return redirect("Student:student_bookings")
    
    return render(request, "Student/payment.html", {"booking": booking})



def payment_processing(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student_id=request.session.get("Sid"))

    if booking.status != "Confirmed":
        messages.error(request, "Payment is only allowed for confirmed bookings.")
        return redirect("Student:student_bookings")

    if request.method == "POST":
        # Simulate payment processing
        booking.payment_status = "Completed"
        booking.save()
        messages.success(request, "Payment successful! You can now chat with your teacher.")

    return redirect("Student:student_bookings")


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def chat(request, teacher_id):
    """ Load chat between student and teacher """
    student_id = request.session.get("Sid")

    if not student_id:
        messages.error(request, "You must be logged in to start a chat.")
        return redirect("Student:Index")

    student = get_object_or_404(Student, id=student_id)
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # ✅ Correct query: Filter messages for both sender/receiver cases
    messages_list = ChatMessage.objects.filter(
        Q(sender_student=student, receiver_teacher=teacher) |
        Q(sender_teacher=teacher, receiver_student=student)
    ).order_by("timestamp")

    return render(request, "Student/chat.html", {
        "student": student,
        "teacher": teacher,
        "messages": messages_list
    })



def send_message(request, teacher_id):
    student_id = request.session.get("Sid")
    
    if not student_id:
        messages.error(request, "You must be logged in to send messages.")
        return redirect("Student:Index")

    student = get_object_or_404(Student, id=student_id)
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                sender_student=student,
                receiver_teacher=teacher,
                text=message_text
            )

    return redirect("Student:chat", teacher_id=teacher.id)

#//////////////////////////////////////////////////////////////////////////////////

def submit_feedback(request, teacher_id):
    if "Sid" not in request.session:
        messages.error(request, "You must be logged in to give feedback.")
        return redirect("Student:Index")  

    student_id = request.session["Sid"]

    # Get student instance
    student = get_object_or_404(Student, id=student_id)

    # Get teacher instance
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating:
            messages.error(request, "Please provide a rating.")
            return redirect("Student:submit_feedback", teacher_id=teacher_id)

        feedback, created = TeacherFeedback.objects.get_or_create(
            student=student,
            teacher=teacher,
            defaults={"rating": int(rating), "comment": comment},
        )

        if not created:
            messages.error(request, "You have already submitted feedback for this teacher.")
        else:
            messages.success(request, "Feedback submitted successfully!")

        return redirect("Student:student_bookings")

    return render(request, "Student/feedback_form.html", {"teacher": teacher})

#//////////////////////////////////////////////////////////////////////////////////

def submit_complaint(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        complaint_text = request.POST.get("complaint")

        student = None
        teacher = None

        Complaint.objects.create(
            user_type=user_type,
            student=student,
            teacher=teacher,
            name=name,
            email=email,
            phone=phone,
            complaint_text=complaint_text,
        )
        messages.success(request, "Complaint submitted successfully!")
        return redirect("Student:Index")

    return render(request, "Student/submit_complaint.html")

#//////////////////////////////////////////////////////////////////////////////////

def student_profile(request):
    """View for displaying the student profile"""
    if "Sid" not in request.session:
        messages.error(request, "You must be logged in to view your profile.")
        return redirect("Student:Index")

    student_id = request.session["Sid"]
    student = get_object_or_404(Student, id=student_id)

    return render(request, "Student/student_profile.html", {"student": student})


def update_student_profile(request):
    """View for updating student profile"""
    if "Sid" not in request.session:
        messages.error(request, "You must be logged in to update your profile.")
        return redirect("Student:Index")

    student_id = request.session["Sid"]
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.phone_number = request.POST.get("phone_number")
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("Student:student_profile")

    return render(request, "Student/update_profile.html", {"student": student})


def update_student_password(request):
    """View for updating student password (without hashing)"""
    if "Sid" not in request.session:
        messages.error(request, "You must be logged in to update your password.")
        return redirect("Student:Index")

    student_id = request.session["Sid"]
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("Student:update_student_password")

        student.password = new_password  # Not hashing password as per your request
        student.save()
        messages.success(request, "Password updated successfully!")
        return redirect("Student:student_profile")

    return render(request, "Student/update_password.html")