from django.contrib import admin
from account.models import User, Course,Instructor,Enrollment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Custom UserAdmin
class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "tc", "is_admin","image"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc","image"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2","image"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["id"]
    filter_horizontal = []

# Register the User model with the custom UserModelAdmin
admin.site.register(User, UserModelAdmin)


class IsStaffFilter(admin.SimpleListFilter):
    title = 'Staff status'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_admin=True)
        if self.value() == 'No':
            return queryset.filter(is_admin=False)


# instructors model registration
class InstructorAdmin(BaseUserAdmin):
    list_display = ["id", "name", "email","image"]
    list_filter = (IsStaffFilter, 'is_active')

    fieldsets =[ ("Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "image"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2","image"],
            },
        ),
    ]
    search_fields = ["name"]
    ordering = ["id"]
    filter_horizontal = []

# Register the Courses model with the custom CoursesAdmin
admin.site.register(Instructor, InstructorAdmin)


# Custom CoursesAdmin
class CoursesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "instructor"]
    fieldsets = [
        ("Course Info", {"fields": ["title", "description", "instructor"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["title", "description", "instructor"],
            },
        ),
    ]
    search_fields = ["title"]
    ordering = ["id"]
    filter_horizontal = []

# Register the Courses model
admin.site.register(Course, CoursesAdmin)


# Custom Enrollment model
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["userEmail", "courseTitle"]
    fieldsets = [
        ("Enrollment Info", {"fields": ["userEmail", "courseTitle"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["userEmail", "courseTitle"],
            },
        ),
    ]
    search_fields = ["courseTitle"]
    ordering = ["id"]
    filter_horizontal = []

# Register the enrollment model
admin.site.register(Enrollment,EnrollmentAdmin)
