from django.db import models

class User(models.Model):

    ROLE_CHOICES = [
        ("sys_admin", "System Admin"),
        ("dept_admin", "Department Admin"),
        ("dept_user", "Department User"),
        ("ppm_admin", "PPM Admin"),
        ("ppm_user", "PPM User"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    emp_no = models.CharField(max_length=20, unique=True)
    emp_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)

    password = models.CharField(max_length=100)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="dept_user"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    def __str__(self):
        return self.emp_name


class AuditLog(models.Model):

    user = models.CharField(max_length=100)

    action = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"


class LoginHistory(models.Model):

    emp_no = models.CharField(max_length=20)

    emp_name = models.CharField(max_length=100)

    login_time = models.DateTimeField(auto_now_add=True)

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.emp_name