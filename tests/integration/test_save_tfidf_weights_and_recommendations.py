from central.models import Idea, Recommendation, Site
from django.test import TestCase
from scripts import save_recommendations, save_tfidf_weights


class SaveTfidfWeightsAndRecommendationsTests(TestCase):

    def setUp(self):
        self.site, _ = Site.objects.get_or_create(domain="example.com")

        # Create some ideas
        self.ideaA = Idea(
            name='Idea A',
            description='jovian assisi',
            site=self.site
        )
        self.ideaA.save()

        self.ideaB = Idea(
            name='Idea B',
            description='cotton jovian cotton',
            site=self.site
        )
        self.ideaB.save()

    def test_save_tfidf_weights_and_recommendations(self):
        # run scripts
        save_tfidf_weights.main()
        save_recommendations.main()

        # Assert (self.ideaA, self.ideaB) similarity is as expected
        assert (
            Recommendation.objects
            .get(idea_1_id=self.ideaA.pk, idea_2_id=self.ideaB.pk)
            .similarity
        ) == 0.19431434016858146

        # Assert (self.idea2, self.idea1) similarity is as expected
        assert (
            Recommendation.objects
            .get(idea_1_id=self.ideaB.pk, idea_2_id=self.ideaA.pk)
            .similarity
        ) == 0.19431434016858146
