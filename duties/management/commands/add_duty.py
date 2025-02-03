from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
import random
from datetime import datetime

from accounts.models import Profile
from duties.models import Duty

User = get_user_model()


class Command(BaseCommand):
    # add faker to the object initiator
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # make a user with fake email
        user = User.objects.create_user(email=self.fake.email(), password="ax/1234567")
        # get the user profile
        profile = Profile.objects.get(user=user)
        # complete the profile with fake first name and last name
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.save()

        for _ in range(5):
            # create 5 duty (task) with fake data
            Duty.objects.create(
                author=profile,
                # fake title with two words
                title=" ".join(self.fake.words(2)),
                # fake description with one paragraph and 5 sentences
                description=self.fake.paragraph(nb_sentences=5),
                # random done status (don= done (completed) and not= not done (uncompleted))
                done_status=random.choice(["don", "not"]),
                # fake deadline date between today and one day in two years ahead!
                deadline_date=self.fake.date_between(
                    start_date=datetime.today(), end_date="+2y"
                ),
            )
