import random

from django.core.management.base import BaseCommand

from central.management.commands.utils.random_words import RANDOM_WORD_LIST
from central.models import Idea, Site


class Command(BaseCommand):

    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(domain="example.com")

        for i in range(1000):
            name = 'Idea ' + str(i)
            description = " ".join(random.sample(RANDOM_WORD_LIST, 20))

            idea = Idea(
                name=name,
                description=description,
                site=site
            )
            idea.save()
