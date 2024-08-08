from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .models import Course, Enrollment
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.serializers import (UserRegistrationSerializer,UserLoginSerializer,
                                  UserProfileSerializer,UserChangePasswordSerializer,
                                  SendPasswordResetEmailSerializer,UserPasswordResetSerializer,
                                  InstructorRegistrationSerializer,
                                  InstructorProfileSerializer,InstructorLoginSerializer,
                                  InstructorChangePasswordSerializer,
                                  SendInstructorPasswordResetEmailSerializer,
                                  InstructorPasswordResetSerializer,
                                  CourseSerializer,EnrollmentSerializer)
from django.contrib.auth import authenticate
from account.renderers import UserRenderer,InstructorRenderer,CoursesRenderer,EnrollmentRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            #token is created for new user
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"registration success"},
                            status=status.HTTP_201_CREATED)
        #errors are printed when raise_exception is missing
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                #token is created for logged in user
                token=get_tokens_for_user(user)
                return Response({"token":token,"msg":"Login success"},
                            status=status.HTTP_200_OK)
            else:
                return Response({'errors' : {'non_field_errors':['Email or Password is not valid']}}
                            ,status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,fomat=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
       
class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,fomat=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.data})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Changed Password"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,fomat=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset Link sent, please check your Email"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, uid, token, fomat=None):
        serializer=UserPasswordResetSerializer(data=request.data,
                                                context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
             return Response({"msg":"Password Reset successfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_instructors(instructor):
    refresh = RefreshToken.for_user(instructor)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class InstructorRegistrationView(APIView):
    renderer_classes=[InstructorRenderer]
    def post(self,request,format=None):
        serializer = InstructorRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instructor=serializer.save()
            #token is created for new instructor
            token=get_tokens_for_instructors(instructor)
            return Response({"token":token,"msg":"registration success"},
                            status=status.HTTP_201_CREATED)
        #errors are printed when raise_exception is missing
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class InstructorLoginView(APIView):
    def post(self, request, format=None):
        serializer = InstructorLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            instructor = authenticate(email=email, password=password)
            if instructor is not None:
                if instructor.is_active:
                    token = get_tokens_for_instructors(instructor)
                    return Response({"token": token, "msg": "Login success"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'errors': {'non_field_errors': ['Account is not active']}},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorProfileView(APIView):
    renderer_classes=[InstructorRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,fomat=None):
        serializer=InstructorProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
       
class InstructorChangePasswordView(APIView):
    renderer_classes=[InstructorRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,fomat=None):
        serializer=InstructorChangePasswordSerializer(data=request.data,context={"instructor":request.data})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Changed Password"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendInstructorPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,fomat=None):
        serializer=SendInstructorPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset Link sent, please check your Email"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InstructorPasswordResetView(APIView):
    renderer_classes=[InstructorRenderer]
    def post(self, request, uid, token, fomat=None):
        serializer=InstructorPasswordResetSerializer(data=request.data,
                                                context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
             return Response({"msg":"Password Reset successfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class RegisterCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

# Enroll in a Course
class EnrollCourseView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# List Courses for a User
class UserCoursesView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user_email = self.request.user.email
        enrollments = Enrollment.objects.filter(userEmail=user_email)
        return enrollments



