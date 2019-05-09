import django # isort:skip # noqa
import os # isort:skip # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')  # isort:skip # noqa
django.setup()  # isort:skip # noqa

import argparse

from central import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')
django.setup()

filename = 'users.csv'


def get_top_recommendations(idea_id, number_of_recommendations):
    recommendations_as_idea1 = list(
        models.Recommendation.objects
        .filter(idea_1_id=idea_id)
        .order_by('-similarity')
        .values_list(
            'idea_2__name',
            'similarity',
        )[:int(number_of_recommendations)]
    )

    recommendations_as_idea2 = list(
        models.Recommendation.objects
        .filter(idea_2_id=idea_id)
        .order_by('-similarity')
        .values_list(
            'idea_1__name',
            'similarity',
        )[:int(number_of_recommendations)]
    )

    all_recommendations = (
        recommendations_as_idea1
        + recommendations_as_idea2
    )

    all_recommendations = sorted(
        all_recommendations,
        key=lambda x: x[1],
        reverse=True,
    )[:int(number_of_recommendations)]

    return [recommendation[0] for recommendation in all_recommendations]


def print_recommendations(recommendations):
    for recommendation in recommendations:
        print(recommendation)


def main(idea_id, number_of_recommendations):
    recommendations = get_top_recommendations(
        idea_id,
        number_of_recommendations,
    )

    print_recommendations(recommendations)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A script to print recommendations for an idea'
    )
    parser.add_argument(
        '-i', '--idea_id',
        help='the id for the idea to get recommendations for',
        required=True,
    )
    parser.add_argument(
        '-n', '--number_of_recommendations',
        help='the number of recommendations to print',
        required=True,
    )

    return parser.parse_args()


if __name__ == "__main__":
    ns = parse_arguments()

    main(ns.idea_id, ns.number_of_recommendations)
