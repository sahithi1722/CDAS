from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="1001",
            defaults={
                "email": "sahithi1722@gmail.com",
                "is_staff": True,
                "is_superuser": True
            }
        )

        if created:
            user.set_password("admin1001")
            user.save()
            self.stdout.write("Demo user created")
        else:
            self.stdout.write("Demo user already exists")