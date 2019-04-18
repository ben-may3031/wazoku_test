'''
BLURB!!!!
'''
import django # isort:skip # noqa
import os # isort:skip # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')  # isort:skip # noqa
django.setup()  # isort:skip # noqa

import math
from central import models
from central.management.commands.utils.random_words import RANDOM_WORD_LIST


def evaluate_idf_dict(vocabulary, idea_descriptions):
    number_of_ideas = len(idea_descriptions)

    idf_dict = {}

    for word in vocabulary:
        number_of_ideas_featuring_word = sum(
            1 for description in idea_descriptions
            if word in description
        )

        print(number_of_ideas_featuring_word)

        idf_dict[word] = (
            1 + math.log(
                (number_of_ideas + 1)
                / (number_of_ideas_featuring_word)
            )
        )

    return idf_dict


def save_feature_vectors(ideas, idf_dict):
    for idea in ideas:
        print("TEST")


def main():
    # Obtain the pks and descriptions for all the ideas we need to process
    ideas = list(models.Idea.objects.values('pk', 'description'))

    # Evaluate a list of idea descriptions
    idea_descriptions = [idea['description'] for idea in ideas]

    # Set the vocabulary to be the list of words from which idea description
    # words are sampled
    vocabulary = RANDOM_WORD_LIST

    idf_dict = evaluate_idf_dict(vocabulary, idea_descriptions)

    save_feature_vectors(ideas, idf_dict)


if __name__ == "__main__":
    main()
