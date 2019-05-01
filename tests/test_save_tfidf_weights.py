import json

from django.test import TestCase

from central.models import Idea, Site
from scripts import save_tfidf_weights


class SaveTfidfWeightsTests(TestCase):

    def setUp(self):
        self.site, _ = Site.objects.get_or_create(domain="example.com")

        # Create some ideas
        self.idea1 = Idea(
            name='Idea 1',
            description='jovian assisi',
            site=self.site
        )
        self.idea1.save()

        self.idea2 = Idea(
            name='Idea 2',
            description='cotton jovian cotton',
            site=self.site
        )
        self.idea2.save()

    def test_save_tfidf_weights(self):
        # run script
        save_tfidf_weights.main()

        # TODO!!!
        self.idea1.refresh_from_db()

        print(json.loads(self.idea1.idea_feature_vector))

        assert 0 == 1
