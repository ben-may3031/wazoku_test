"""
Saves an Recommendation object to the database for each pair of ideas.
Each object stores the cosine similarity between the (normalised) TF-IDF
weights associated with the ideas, and is related to each idea through a
ForeignKey field.
"""
import django # isort:skip # noqa
import os # isort:skip # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')  # isort:skip # noqa
django.setup()  # isort:skip # noqa

import json

from central import models


def get_similarity(
    idea_1_tfidfs,
    idea_2_tfidfs,
):
    """
    Evaluates the cosine similarity between two sets of the TF-IDF weights

    Arguments:
    - dict with words from the vocabulary as keys and TF-IDF weights as values
    - another dict with words from the vocabulary as keys and TF-IDF weights as
    values

    Returns:
    - a float representing cosine similarity
    """
    similarity = 0.0

    for word, tfidf in idea_1_tfidfs.items():
        similarity += tfidf * idea_2_tfidfs.get(word, 0)

    return similarity


def main():
    # Delete all existing Recommendation objects
    models.Recommendation.objects.all().delete()

    # Evaluate a dict with idea ids as keys and associated
    # TF-IDF dicts as values.
    idea_tfidf_dict = dict(
        models.IdeaTfidfWeights.objects
        .values_list('idea_id', 'tfidfs')
    )

    recommendation_objects = []

    # Loop over all pairs of ideas, evaluating the cosine similarity
    # between the TF-IDF weights for each of the two ideas.
    for (
        outer_idea_id,
        outer_idea_tfidf_string,
    ) in idea_tfidf_dict.items():
        for (
            inner_idea_id,
            inner_idea_tfidf_string,
        ) in idea_tfidf_dict.items():
            if outer_idea_id == inner_idea_id:
                continue

            similarity = get_similarity(
                json.loads(outer_idea_tfidf_string),
                json.loads(inner_idea_tfidf_string),
            )

            recommendation_objects.append(
                models.Recommendation(
                    similarity=similarity,
                    idea_1_id=outer_idea_id,
                    idea_2_id=inner_idea_id,
                )
            )

    # Save the new Recommendation objects to the database
    models.Recommendation.objects.bulk_create(recommendation_objects)


if __name__ == "__main__":
    main()
