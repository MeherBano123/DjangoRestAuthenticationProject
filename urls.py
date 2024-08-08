from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from account.views import (UserRegistrationView,UserLoginView,
                           UserProfileView,UserChangePasswordView,
                           SendPasswordResetEmailView,UserPasswordResetView,InstructorRegistrationView,
                           InstructorLoginView,InstructorProfileView,InstructorChangePasswordView,
                           InstructorPasswordResetView,SendInstructorPasswordResetEmailView,
                           EnrollCourseView,RegisterCourseView,UserCoursesView)

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(),name="register"),
    path('user/login/',UserLoginView.as_view(),name='login'),
    path('user/profile/',UserProfileView.as_view(),name='profile'),
    path('user/changepassword/',UserChangePasswordView.as_view(),name='change-password '),
    path('user/send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('user/password-reset/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),

    path('instructor/register/', InstructorRegistrationView.as_view(),name="instructor-register"),
    path('instructor/login/',InstructorLoginView.as_view(),name='instructor-login'),
    path('instructor/Profile/',InstructorProfileView.as_view(),name='instructor-profile'),
    path('instructor/changepassword/',InstructorChangePasswordView.as_view(),name='instructor-change-password '),
    path('instructor/send-reset-password-email/',SendInstructorPasswordResetEmailView.as_view(),name='send-instructor-reset-password-email'),
    path('instructor/password-reset/<uid>/<token>/',InstructorPasswordResetView.as_view(),name='instructor-reset-password'),
    
    path('registerCourses/',RegisterCourseView.as_view(),name='register-course'),
    path('enrollCourses/',EnrollCourseView.as_view(),name='enroll-course'),
    path('user-courses/',UserCoursesView.as_view(),name='user-courses'),
    
    
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
