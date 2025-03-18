

from django.urls import path

from Student import views


app_name="Student"

urlpatterns=[
    path('Index/',views.Index,name='Index'),
    path('register/', views.student_registration, name='student_registration'),
    path('student_home/', views.student_home, name='student_home'),
    path('login/',views.Login,name="login"),
    path('search/',views.search_teachers, name='search_teachers'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('book/<int:section_id>/', views.book_teacher, name='book_teacher'),
    path('my-bookings/', views.student_bookings, name='student_bookings'),
    path("make-payment/<int:booking_id>/", views.make_payment, name="make_payment"),
    path("payment/<int:booking_id>/", views.payment_processing, name="payment_processing"),
    path("chat/<int:teacher_id>/", views.chat, name="chat"),
    path("send-message/<int:teacher_id>/", views.send_message, name="send_message"),
    path("feedback/<int:teacher_id>/", views.submit_feedback, name="submit_feedback"),
    path("submit/", views.submit_complaint, name="submit_complaint"),
    path("profile/", views.student_profile, name="student_profile"),
    path("profile/update/", views.update_student_profile, name="update_student_profile"),
    path("profile/change-password/", views.update_student_password, name="update_student_password"),

]