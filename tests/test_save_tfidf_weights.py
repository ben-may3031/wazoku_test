import json
import math

from central.models import Idea, Site
from django.test import TestCase
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

    def get_expectations(self):
        number_of_ideas = 2

        number_of_jovian_ideas = 2
        number_of_assisi_ideas = 1
        number_of_cotton_ideas = 1

        expected_jovian_idf = 1 + math.log(
            (number_of_ideas + 1) / (number_of_jovian_ideas + 1)
        )

        expected_assisi_idf = 1 + math.log(
            (number_of_ideas + 1) / (number_of_assisi_ideas + 1)
        )

        expected_cotton_idf = 1 + math.log(
            (number_of_ideas + 1) / (number_of_cotton_ideas + 1)
        )

        idea1_jovian_tf = 1
        idea1_assisi_tf = 1

        expected_idea1_jovian_tfidf = idea1_jovian_tf * expected_jovian_idf
        expected_idea1_assisi_tfidf = idea1_assisi_tf * expected_assisi_idf

        expected_idea1_tfidf_magnitude = math.sqrt(
            expected_idea1_jovian_tfidf ** 2 + expected_idea1_assisi_tfidf ** 2
        )

        expected_idea1_jovian_tfidf_normalised = (
            expected_idea1_jovian_tfidf / expected_idea1_tfidf_magnitude
        )

        expected_idea1_assisi_tfidf_normalised = (
            expected_idea1_assisi_tfidf / expected_idea1_tfidf_magnitude
        )

        idea2_jovian_tf = 1
        idea2_cotton_tf = 2

        expected_idea2_jovian_tfidf = idea2_jovian_tf * expected_jovian_idf
        expected_idea2_cotton_tfidf = idea2_cotton_tf * expected_cotton_idf

        expected_idea2_tfidf_magnitude = math.sqrt(
            expected_idea2_jovian_tfidf ** 2 + expected_idea2_cotton_tfidf ** 2
        )

        expected_idea2_jovian_tfidf_normalised = (
            expected_idea2_jovian_tfidf / expected_idea2_tfidf_magnitude
        )

        expected_idea2_cotton_tfidf_normalised = (
            expected_idea2_cotton_tfidf / expected_idea2_tfidf_magnitude
        )

        return (
            expected_idea1_jovian_tfidf_normalised,
            expected_idea1_assisi_tfidf_normalised,
            expected_idea2_jovian_tfidf_normalised,
            expected_idea2_cotton_tfidf_normalised,
        )

    def test_save_tfidf_weights(self):
        # run script
        save_tfidf_weights.main()

        (
            expected_idea1_jovian_tfidf_normalised,
            expected_idea1_assisi_tfidf_normalised,
            expected_idea2_jovian_tfidf_normalised,
            expected_idea2_cotton_tfidf_normalised,
        ) = self.get_expectations()

        idea1_tfidfs = json.loads(self.idea1.idea_feature_vector.tfidfs)

        assert idea1_tfidfs['jovian'] == expected_idea1_jovian_tfidf_normalised
        assert idea1_tfidfs['assisi'] == expected_idea1_assisi_tfidf_normalised

        idea2_tfidfs = json.loads(self.idea2.idea_feature_vector.tfidfs)

        assert idea2_tfidfs['jovian'] == expected_idea2_jovian_tfidf_normalised
        assert idea2_tfidfs['cotton'] == expected_idea2_cotton_tfidf_normalised

        assert 0 == 1
