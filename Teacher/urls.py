


from django.urls import path

from Teacher import views


app_name='Teacher'

urlpatterns=[
    path('Teacher_home/',views.Teacher_home,name="Teacher_home"),
    path('add-teacher/',views.add_teacher, name='add_teacher'),
    path('teacher/add-section/',views.add_music_section, name='add_music_section'),
    path('teacher/bookings/', views.teacher_bookings, name='teacher_bookings'),
    path('teacher/update-booking/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path("chat/<int:student_id>/", views.teacher_chat, name="teacher_chat"),
    path("send-message/<int:student_id>/", views.send_message_teacher, name="send_message"),
    path("profile/", views.teacher_profile, name="teacher_profile"),
    path("profile/update/", views.update_teacher_profile, name="update_teacher_profile"),
    path("profile/update-password/", views.update_teacher_password, name="update_teacher_password"),
    path("music-sections/", views.view_music_sections, name="view_music_sections"),
    path("music-sections/edit/<int:section_id>/", views.edit_music_section, name="edit_music_section"),

]

