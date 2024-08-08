from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, image=None, password=None,password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
            image=image,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, image=None, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            tc=tc,
            image=image,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class InstructorManager(BaseUserManager):
    def create_instructor(self, email, name, image=None, password=None,password2=None):
        if not email:
            raise ValueError("Instructors must have an email address")

        instructor = self.model(
            email=self.normalize_email(email),
            name=name,
            image=image,
        )
        instructor.set_password(password)
        instructor.save(using=self._db)
        return instructor


    def create_superinstructor(self, email, name, image=None, password=None):
        instructor = self.create_instructor(
            email=email,
            name=name,
            password=password,
            image=image
        )
        instructor.is_admin = True
        instructor.save(using=self._db)
        return instructor

class Instructor(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    objects = InstructorManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Course(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    courseTitle = models.ForeignKey(Course, on_delete=models.CASCADE,to_field='title')
    enrolled_on = models.DateTimeField(auto_now_add=True)

