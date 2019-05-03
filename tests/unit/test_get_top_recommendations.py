from central.models import Idea, Recommendation, Site
from django.test import TestCase
from scripts.print_recommendations import get_top_recommendations


class SaveRecommendationsTests(TestCase):

    def setUp(self):
        self.site, _ = Site.objects.get_or_create(domain="example.com")

        # Create some ideas
        self.ideaA = Idea(
            name='Idea A',
            site=self.site,
        )
        self.ideaA.save()

        self.ideaB = Idea(
            name='Idea B',
            site=self.site,
        )
        self.ideaB.save()

        self.ideaC = Idea(
            name='Idea C',
            site=self.site,
        )
        self.ideaC.save()

        self.ideaD = Idea(
            name='Idea D',
            site=self.site,
        )
        self.ideaD.save()

        # Create TF-IDF weights objects for the ideas
        Recommendation(
            idea_1_id=self.ideaA.pk,
            idea_2_id=self.ideaB.pk,
            similarity=0.1,
        ).save()

        Recommendation(
            idea_1_id=self.ideaA.pk,
            idea_2_id=self.ideaC.pk,
            similarity=0.2,
        ).save()

        Recommendation(
            idea_1_id=self.ideaA.pk,
            idea_2_id=self.ideaD.pk,
            similarity=0.3,
        ).save()

    def test_save_recommendations(self):
        # run function
        recommendations = get_top_recommendations(self.ideaA.pk, 2)

        # Assert that recommendations are as expected
        assert recommendations == ['Idea D', 'Idea C']
