import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from Student.models import Booking, Complaint, Student, TeacherFeedback
from Teacher import models
from Teacher.models import Teacher


def Admin_home(request):
    context = {
        'context_list': [{
            'teacher_count': Teacher.objects.count(),
            'student_count': Student.objects.count(),
            'booking_count': Booking.objects.count(),
            'pending_teachers': Teacher.objects.filter(teacher_approved_status=0).count(),
        }],
        'complaints': Complaint.objects.all(),  # Merged complaints into the same dictionary
        'feedbacks': TeacherFeedback.objects.all(),
    }
    return render(request, 'Admin/Admin_home.html', context)


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def teacher_approval_requests(request):
    pending_teachers = Teacher.objects.filter(teacher_approved_status=0)
    return render(request, "Admin/Admin_teacher_approval.html", {"teachers": pending_teachers})

#//////////////////////////////////////////////////////////////////////////////////

def approve_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.teacher_approved_status = 1  
    teacher.save()
    return redirect('Admin:teacher_approval_requests')

#//////////////////////////////////////////////////////////////////////////////////

def reject_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.teacher_approved_status = -1 
    teacher.save()
    return redirect('Admin:teacher_approval_requests')

#//////////////////////////////////////////////////////////////////////////////////


def admin_view_complaints(request):
    complaints = Complaint.objects.all().order_by("-created_at")
    return render(request, "admin/complaints_list.html", {"complaints": complaints})

#//////////////////////////////////////////////////////////////////////////////////

def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = "Resolved"
    complaint.save()
    messages.success(request, "Complaint marked as Resolved.")
    return redirect("Admin:admin_view_complaints")

#//////////////////////////////////////////////////////////////////////////////////

def view_students(request):
    students = Student.objects.all() 
    return render(request, 'Admin/view_students.html', {'students': students})

#//////////////////////////////////////////////////////////////////////////////////

def view_teachers(request):
    teachers = Teacher.objects.all() 
    return render(request, 'Admin/view_teachers.html', {'teachers': teachers})

#///////////////////////////////////////////////////////////////////////////////////////

def booking_statistics(request):
    teacher_bookings = list(
        Booking.objects.values('teacher__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    teacher_bookings_json = json.dumps(teacher_bookings)
    total_bookings = Booking.objects.count()
    context = {
        'teacher_bookings_json': teacher_bookings_json, 
        'total_bookings': total_bookings,
    }
    return render(request, 'Admin/booking_statistics.html', context)