from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Enrollment

def setup_roles():
    # Admin Group - all permissions
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Instructor Group - manage their own courses and enrollments
    instructor_group, _ = Group.objects.get_or_create(name='Instructor')

    course_ct = ContentType.objects.get_for_model(Course)
    enrollment_ct = ContentType.objects.get_for_model(Enrollment)

    instructor_permissions = Permission.objects.filter(
        content_type__in=[course_ct, enrollment_ct]
    )
    instructor_group.permissions.set(instructor_permissions)

    # Student Group - only basic view/add permissions
    student_group, _ = Group.objects.get_or_create(name='Student')

    student_permissions = Permission.objects.filter(
        codename__in=['view_course', 'view_enrollment', 'add_enrollment']
    )
    student_group.permissions.set(student_permissions)

    print("✅ Roles and permissions set up successfully.")
