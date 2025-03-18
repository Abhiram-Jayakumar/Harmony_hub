from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from Student.models import Complaint
from Teacher.models import Teacher

    

def Admin_home(request):
    return render(request,"Admin/Admin_home.html")
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def teacher_approval_requests(request):
    # Fetch teachers whose approval status is pending (0)
    pending_teachers = Teacher.objects.filter(teacher_approved_status=0)
    return render(request, "Admin/Admin_teacher_approval.html", {"teachers": pending_teachers})

def approve_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.teacher_approved_status = 1  # Approved
    teacher.save()
    return redirect('Admin:teacher_approval_requests')

def reject_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.teacher_approved_status = -1  # Rejected
    teacher.save()
    return redirect('Admin:teacher_approval_requests')

#//////////////////////////////////////////////////////////////////////////////////


def admin_view_complaints(request):
    complaints = Complaint.objects.all().order_by("-created_at")
    return render(request, "admin/complaints_list.html", {"complaints": complaints})

def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = "Resolved"
    complaint.save()
    messages.success(request, "Complaint marked as Resolved.")
    return redirect("Admin:admin_view_complaints")