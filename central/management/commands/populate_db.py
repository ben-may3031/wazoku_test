import random

from django.core.management.base import BaseCommand

from central.management.commands.utils.random_words import (
    RANDOM_WORD_LIST,
    RANDOM_WORD_LIST_WEIGHTS,
)
from central.models import Idea, Site


class Command(BaseCommand):

    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(domain="example.com")

        # delete existing ideas
        Idea.objects.all().delete()

        ideas = []

        for i in range(1000):
            name = 'Idea ' + str(i)

            # build a description consisting of 20 words sampled from
            # RANDOM_WORD_LIST using RANDOM_WORD_LIST_WEIGHTS for the
            # probability weighting
            description = " ".join(
                random.choices(
                    population=RANDOM_WORD_LIST,
                    weights=RANDOM_WORD_LIST_WEIGHTS,
                    k=20,
                )
            )

            ideas.append(
                Idea(
                    name=name,
                    description=description,
                    site=site
                )
            )

        Idea.objects.bulk_create(ideas)
