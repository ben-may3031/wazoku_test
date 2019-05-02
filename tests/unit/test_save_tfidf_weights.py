import json
import math

from central.models import Idea, Site
from django.test import TestCase
from scripts import save_tfidf_weights


class SaveTfidfWeightsTests(TestCase):

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

    def get_expectations(self):
        # Evaluate expected IDF for each term that features
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

        # Evaluate expected normalised TF-IDFs for self.ideaA
        ideaA_jovian_tf = 1
        ideaA_assisi_tf = 1

        expected_ideaA_jovian_tfidf = ideaA_jovian_tf * expected_jovian_idf
        expected_ideaA_assisi_tfidf = ideaA_assisi_tf * expected_assisi_idf

        expected_ideaA_tfidf_magnitude = math.sqrt(
            expected_ideaA_jovian_tfidf ** 2 + expected_ideaA_assisi_tfidf ** 2
        )

        expected_ideaA_jovian_tfidf_normalised = (
            expected_ideaA_jovian_tfidf / expected_ideaA_tfidf_magnitude
        )

        expected_ideaA_assisi_tfidf_normalised = (
            expected_ideaA_assisi_tfidf / expected_ideaA_tfidf_magnitude
        )

        # Evaluate expected normalised TF-IDFs for self.ideaB
        ideaB_jovian_tf = 1
        ideaB_cotton_tf = 2

        expected_ideaB_jovian_tfidf = ideaB_jovian_tf * expected_jovian_idf
        expected_ideaB_cotton_tfidf = ideaB_cotton_tf * expected_cotton_idf

        expected_ideaB_tfidf_magnitude = math.sqrt(
            expected_ideaB_jovian_tfidf ** 2 + expected_ideaB_cotton_tfidf ** 2
        )

        expected_ideaB_jovian_tfidf_normalised = (
            expected_ideaB_jovian_tfidf / expected_ideaB_tfidf_magnitude
        )

        expected_ideaB_cotton_tfidf_normalised = (
            expected_ideaB_cotton_tfidf / expected_ideaB_tfidf_magnitude
        )

        return (
            expected_ideaA_jovian_tfidf_normalised,
            expected_ideaA_assisi_tfidf_normalised,
            expected_ideaB_jovian_tfidf_normalised,
            expected_ideaB_cotton_tfidf_normalised,
        )

    def test_save_tfidf_weights(self):
        # run script
        save_tfidf_weights.main()

        # Get expected normalised TF-IDFs
        (
            expected_ideaA_jovian_tfidf_normalised,
            expected_ideaA_assisi_tfidf_normalised,
            expected_ideaB_jovian_tfidf_normalised,
            expected_ideaB_cotton_tfidf_normalised,
        ) = self.get_expectations()

        # Get self.ideaA normalised TF-IDFs from the database
        ideaA_tfidfs = json.loads(self.ideaA.idea_tfidf_weights.tfidfs)

        # Assert that self.ideaA TF-IDFs are as expected
        assert ideaA_tfidfs['jovian'] == expected_ideaA_jovian_tfidf_normalised
        assert ideaA_tfidfs['assisi'] == expected_ideaA_assisi_tfidf_normalised
        assert sum(value for value in ideaA_tfidfs.values()) == (
            expected_ideaA_jovian_tfidf_normalised
            + expected_ideaA_assisi_tfidf_normalised
        )

        # Get self.ideaB normalised TF-IDFs from the database
        ideaB_tfidfs = json.loads(self.ideaB.idea_tfidf_weights.tfidfs)

        # Assert that self.ideaB TF-IDFs are as expected
        assert ideaB_tfidfs['jovian'] == expected_ideaB_jovian_tfidf_normalised
        assert ideaB_tfidfs['cotton'] == expected_ideaB_cotton_tfidf_normalised
        assert sum(value for value in ideaB_tfidfs.values()) == (
            expected_ideaB_jovian_tfidf_normalised
            + expected_ideaB_cotton_tfidf_normalised
        )
