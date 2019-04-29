'''
Saves an IdeaTfidfWeights object to the database for each idea. Each object
stores the normalised term frequency-inverse document (TF-IDF) weights for all
words in the vocabulary in a JSON represented as a string, and is related to
its idea through a OneToOneField.
'''
import django # isort:skip # noqa
import os # isort:skip # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise.settings')  # isort:skip # noqa
django.setup()  # isort:skip # noqa

import json
import math
from central import models
from central.management.commands.utils.random_words import RANDOM_WORD_LIST


def evaluate_idf_dict(vocabulary, idea_descriptions):
    '''
    Loop over all words in the vocabulary. For each word count the number of
    idea descriptions that contain the word and then calculate the inverse
    document frequency (IDF) for that word

    Arguments:
    - list of word strings representing the vocabulary used to generate the
    idea descriptions
    - a list of idea description strings (for all ideas)

    Returns:
    - a dict with words from the vocabulary as keys and IDFs as values
    '''
    number_of_ideas = len(idea_descriptions)

    idf_dict = {}

    for word in vocabulary:
        number_of_ideas_featuring_word = sum(
            1 for description in idea_descriptions
            if word in description
        )

        idf_dict[word] = (
            1 + math.log(
                (number_of_ideas + 1)
                / (number_of_ideas_featuring_word + 1)
            )
        )

    return idf_dict


def save_tfidf_weights(ideas, idf_dict):
    '''
    For each idea, evaluate the normalised term frequency-inverse document
    frequency (TF-IDF) weight for all terms in the vocabulary and stores the
    result in the database. Note that old results are deleted first.

    Arguments:
    - list of dicts storing idea ids and corresponding descriptions
    - a dict with words from the vocabulary as keys and IDFs as values

    Returns nothing
    '''
    models.IdeaTfidfWeights.objects.all().delete()

    idea_tfidf_weights_objects = []

    for idea in ideas:
        idea_tfidf_dict = {}
        sum_of_squares = 0

        for word, idf in idf_dict.items():
            tf = idea['description'].count(word)
            tfidf = tf * idf
            idea_tfidf_dict[word] = tfidf
            sum_of_squares += tfidf * tfidf

        idea_tfidf_magnitude = math.sqrt(sum_of_squares)

        # If idea_tfidf_magnitude > 0, normalise idea_tfidf_dict by dividing
        # each value by magnitude of the vector formed from all the TF-IDF
        # weights for the idea and then append the normalised result to
        # idea_tfidf_weights_objects (to be saved later). If
        # idea_tfidf_magnitude = 0, then no object is saved for the idea
        # (since its similarity to any other idea will always be 0 anyway)
        if idea_tfidf_magnitude > 0:
            idea_tfidf_dict_normalised = dict(
                (key, value / idea_tfidf_magnitude)
                for key, value in idea_tfidf_dict.items()
            )

            idea_tfidf_weights_objects.append(
                models.IdeaTfidfWeights(
                    idea_id=idea['pk'],
                    tfidfs=json.dumps(idea_tfidf_dict_normalised),
                )
            )

    models.IdeaTfidfWeights.objects.bulk_create(idea_tfidf_weights_objects)


def main():
    # Obtain the pks and descriptions for all the ideas we need to process
    ideas = list(models.Idea.objects.values('pk', 'description'))

    # Evaluate a list of idea descriptions
    idea_descriptions = [idea['description'] for idea in ideas]

    # Set the vocabulary to be the list of words from which idea description
    # words are sampled
    vocabulary = RANDOM_WORD_LIST

    # Evaluate a dict with words from the vocabulary as keys and inverse
    # document frequencies (IDFs) as values
    idf_dict = evaluate_idf_dict(vocabulary, idea_descriptions)

    # For each idea, evaluate the normalised term frequency-inverse document
    # frequency (TF-IDF) weight for all terms in the vocabulary and stores the
    # result in the database
    save_tfidf_weights(ideas, idf_dict)


if __name__ == "__main__":
    main()
