from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('course_description/', views.course_description, name='course_description'),
    path('lesson_detail/', views.lesson_detail, name='lesson_detail'),
    path('chatbot/mock-reply/', views.chatbot_mock_reply, name='chatbot_mock_reply'),
    path('pretest/', views.pretest, name='pretest'),
    path('posttest/', views.posttest, name='posttest'),
    path('results/', views.results, name='results'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/students/', views.teacher_students, name='teacher_students'),
    path('teacher/lessons/', views.teacher_lessons, name='teacher_lessons'),
    path('teacher/grades/', views.teacher_grades, name='teacher_grades'),
    path('login/', views.login_page, name='login'),
    path('exercise/', views.exercise, name='exercise'),
]