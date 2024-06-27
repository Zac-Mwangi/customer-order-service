import os

from customer_app.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create an admin superuser - does not throw Exception if user exists"

    def handle(self, *args, **options):
        user = User.objects.filter(username="admin")

        if not user.exists():
            User.objects.create_superuser(
                first_name="super",
                last_name="admin",
                username="admin",
                email="admin@mail.com",
                password="admin123",
            )
