'''
BLURB!!!!
'''
import django # isort:skip # noqa
import os # isort:skip # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')  # isort:skip # noqa
django.setup()  # isort:skip # noqa

import json
from central import models


def get_similarity(
    idea_feature_vector_1,
    idea_feature_vector_2,
):
    similarity = 0

    for word, tfidf in idea_feature_vector_1.items():
        similarity += tfidf * idea_feature_vector_2.get(word, 0)

    return similarity


def main():
    models.Recommendation.objects.all().delete()

    idea_feature_vector_dict = dict(
        models.IdeaFeatureVector.objects
        .values_list('idea_id', 'tfidfs')
    )

    recommendation_objects = []

    for (
        outer_idea_id,
        outer_idea_feature_vector_string,
    ) in idea_feature_vector_dict.items():
        for (
            inner_idea_id,
            inner_idea_feature_vector_string,
        ) in idea_feature_vector_dict.items():
            if outer_idea_id == inner_idea_id:
                continue

            similarity = get_similarity(
                json.loads(outer_idea_feature_vector_string),
                json.loads(inner_idea_feature_vector_string),
            )

            recommendation_objects.append(
                models.Recommendation(
                    similarity=similarity,
                    idea_1_id=outer_idea_id,
                    idea_2_id=inner_idea_id,
                )
            )

    models.Recommendation.objects.bulk_create(recommendation_objects)


if __name__ == "__main__":
    main()
