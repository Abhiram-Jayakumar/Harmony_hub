

from django.urls import path
from Admin import views


app_name='Admin'

urlpatterns=[
   
    path('Admin_home/',views.Admin_home,name="Admin_home"),
    path('admin/teacher-approvals/', views.teacher_approval_requests, name='teacher_approval_requests'),
    path('admin/approve-teacher/<int:teacher_id>/',views.approve_teacher, name='approve_teacher'),
    path('admin/reject-teacher/<int:teacher_id>/',views.reject_teacher, name='reject_teacher'),
    path("admin/complaints/",views. admin_view_complaints, name="admin_view_complaints"),
    path("admin/complaints/update/<int:complaint_id>/", views.update_complaint_status, name="update_complaint_status"),


]