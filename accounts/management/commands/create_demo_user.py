from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        user, created = User.objects.get_or_create(
            emp_no="9999",
            defaults={
                "emp_name": "Demo User",
                "department": "IT",
                "role": "Admin",
                "status": "Active",
            }
        )

        if created:
            user.set_password("demo123")
            user.save()
            self.stdout.write("Demo user created successfully")
        else:
            self.stdout.write("Demo user already exists")