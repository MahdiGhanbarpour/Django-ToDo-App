from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import User
from ...models import Task


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            self.fake.user_name(), self.fake.email(), "Test12345"
        )

        for _ in range(5):
            Task.objects.create(
                author=user,
                title=self.fake.paragraph(nb_sentences=1),
                is_done=random.choice([True, False]),
            )
