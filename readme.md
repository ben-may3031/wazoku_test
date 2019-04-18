# Wazoku data science backend developer test

## Description
This repo contains a method for measuring the similarity of description text associated with pairs of idea objects in a collection of idea objects. A command is included that can be used to populate a database with ideas having associated description text that consists of terms randomly sampled from a given vocabulary. Also included is a script named `save_tfidf_weights.py` which is run manually and saves a collection of term frequency-inverse document frequency (TF-IDF) weights for the descriptions associated with ideas. For each idea, a weight is stored for each term appearing in the vocabulary (see TF-IDF algorithm section below). TF-IDF weights are intended to reflect how important a term is to a document in a collection of documents. To simplfy this assessment, no pre-processing of text occurs prior to evaluating TF-IDF weights. Finally, a script called `save_recommendations.py` is included which is also run manually and saves a similarity for each pair of idea descriptions. These similarities are the cosine similarities of the TF-IDF vectors associated with the idea description (see Cosine similarity algorithm section below). We label the object saved as a recommendation, since it contains the ids for the two ideas and the similarity of the their text FINISH!!!!

## TF-IDF algorithm

The vocabulary used for this exercise is a fixed list of 100 terms. For each term, t, in the vocabulary, an inverse document frequency (IDF) is evaluated as follows:

- Set N to be the total number of ideas
- Set n to be the number of ideas that have a description containing term t at least once
- The IDF for term t is then given by 1 + log((N + 1) / (n + 1)), where log is the natural logarithm (base e). It is therefore the case that the IDF for term t decreases as n increases (so that "rare" terms have a relatively high IDF and "common" terms have a relatively low IDF). Let us denote the IDF for term t as IDF_t.

The TF-IDF weight for idea i and term t is then evaluated as follows:

- The term frequency (TF) for term t in idea i is the number of times t appears in the description for i. Let us denote the TF for term t in idea i as TF_(i, t).
- The TF-IDF weight for idea i and term t, denoted TF-IDF_(i, t) is then given by TF_(i, t) * IDF_t.
- NORMALISATION!!!!!

For each idea i, we store the collection of normalised TF-IDF_(i, t) weights for all t in the vocabulary.

## Cosine similarity algorithm

The cosine simlarity of two vectors is the cosine of the angle between the vectors. TF-IDF TO VECTOR BIT!!!! Since TF-IDF weights for an idea are already normalised, the cosine similarity of the TF-IDF weights associated with idea i and those associated with idea j is given by the sum of TF-IDF_(t, i) * TF-IDF_(t, j) over all terms t in the vocabulary. 

## Getting started

Copying the repository

Due to the public nature of forks we suggest you duplicate the repo rather then forking it. 
You will need to create your own repo e.g. `[your_github_username]/wazoku_test` and then clone 
this repo `ben-may3031/wazoku_test` and push the code into your new one. You can follow the steps for doing this here: https://help.github.com/articles/duplicating-a-repository/

Before proceeded be aware that this exercise assumes you are using a linux machine with [pip](https://pip.pypa.io/en/stable) and [virtualenv](https://virtualenv.pypa.io/en/stable/) installed. 

Create a new python 3.6 virtualenv in your checked out repo.

    cd /[path_to]/wazoku_test
    virtualenv -p python3.6 .


Then install the dependencies:

    bin/pip install -r requirements.txt


Set the default django settings file used by all following commands:

    export DJANGO_SETTINGS_MODULE=exercise.settings


The code in this repo uses an sqlite database as the persistence layer. You can initialize an sqlite database (this db will be stored in the file `./db.sqlite3`)

    bin/python manage.py migrate

There is a simple django `populate_db` command which can be used to prime the database with some idea data (the descriptions for the ideas are 20 terms randomly sampled from the set vocabulary using an uneven probability distribution with duplicates allowed)

    bin/python manage.py populate_db

The script to save tfidf weights can be run with the following:

    bin/python -m scripts.save_tfidf_weights
    
After the tfidf weights have been saved, the script to save recommendations can be run with the following:

    bin/python -m scripts.save_recommendations

There is also a unit test which can be used to validate the code:

    bin/python manage.py test tests/*


## Exercise 1

SCRIPT FOR REC. REQUESTS (+ TEST)

Please create a pull request for this work.

## Exercise 2

REFACTOR FEATURE VECTORS

Please create a pull request for this work.

## Exercise 3

HALF NUMBER OF REC OBJECTS

Please create a third pull request for this work.

## Exercise 4

MEMORY CONSIDERATIONS

Please create a third pull request for this work.
