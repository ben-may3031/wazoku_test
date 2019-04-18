import random

from django.core.management.base import BaseCommand

from central.management.commands.utils.random_words import RANDOM_WORD_LIST
from central.models import Idea, Site


class Command(BaseCommand):

    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(domain="example.com")

        ideas = []

        for i in range(1000):
            name = 'Idea ' + str(i)
            description = " ".join(random.choices(RANDOM_WORD_LIST, k=20))

            ideas.append(
                Idea(
                    name=name,
                    description=description,
                    site=site
                )
            )

        Idea.objects.bulk_create(ideas)
