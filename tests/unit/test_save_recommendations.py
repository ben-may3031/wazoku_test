from central.models import Idea, IdeaTfidfWeights, Recommendation, Site
from django.test import TestCase
from scripts import save_recommendations


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

        # Create TF-IDF weights objects for the ideas
        IdeaTfidfWeights(
            idea=self.ideaA,
            tfidfs='{"cat": 0.6, "dog": 0.8, "mouse": 0.0}'
        ).save()

        IdeaTfidfWeights(
            idea=self.ideaB,
            tfidfs='{"cat": 1.0, "dog": 0.0, "mouse": 0.0}'
        ).save()

        IdeaTfidfWeights(
            idea=self.ideaC,
            tfidfs='{"cat": 0.0, "dog": 0.6, "mouse": 0.8}'
        ).save()

    def test_save_recommendations(self):
        # run script
        save_recommendations.main()

        # Assert that (self.ideaA, self.ideaB) similarity is as expected
        expected_ideaA_ideaB_similarity = 0.6 * 1.0 + 0.8 * 0.0 + 0.0 * 0.0

        assert (
            Recommendation.objects
            .get(idea_1_id=self.ideaA.pk, idea_2_id=self.ideaB.pk)
            .similarity
        ) == expected_ideaA_ideaB_similarity

        # Assert that (self.ideaA, self.ideaC) similarity is as expected
        expected_ideaA_ideaC_similarity = 0.6 * 0.0 + 0.8 * 0.6 + 0.0 * 0.8

        assert (
            Recommendation.objects
            .get(idea_1_id=self.ideaA.pk, idea_2_id=self.ideaC.pk)
            .similarity
        ) == expected_ideaA_ideaC_similarity

        # Assert that (self.ideaB, self.ideaC) similarity is as expected
        expected_ideaB_ideaC_similarity = 1.0 * 0.0 + 0.0 * 0.6 + 0.0 * 0.8

        assert (
            Recommendation.objects
            .get(idea_1_id=self.ideaB.pk, idea_2_id=self.ideaC.pk)
            .similarity
        ) == expected_ideaB_ideaC_similarity
