from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    employee_no = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.CharField(
        max_length=100
    )

    designation = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ("Admin", "Admin"),
            ("Engineer", "Engineer"),
            ("Viewer", "Viewer"),
        ],
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username