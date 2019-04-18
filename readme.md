# Wazoku data science backend developer test

## Description
(REWORD!!!!) This repo represents a stripped down version of our core ideas platform product 'Idea Spotlight'. A command is included that can be used to populate a database with ideas having associated description text that consists of words randomly sampled from a given vocabulary. Also included is a script named `save_feature_vectors.py` which is run manually and saves a feature vector of term frequency-inverse document frequency (TF-IDF) weights for each idea. For each of these feature vectors, a weight is stored for each term appearing in the vocabulary (see TF-IDF algorithm section below). Finally, a script called `save_recommendations.py` is included which is also run manually and saves a similarity for each pair of ideas. These similarities are the cosine similarities of the TF-IDF vectors associated with the ideas (see Cosine similarity algorithm section below).

## TF-IDF algorithm

## Cosine similarity algorithm

## Getting started

Copying the repository

Due to the public nature of forks we suggest you duplicate the repo rather then forking it. 
You will need to create your own repo e.g. `[your_github_username]/wazoku_test` and then clone 
this repo `chrispbailey/wazoku_test` and push the code into your new one. You can follow the steps for doing this here: https://help.github.com/articles/duplicating-a-repository/

Before proceeded be aware that this exercise assumes you are using a linux machine with [pip](https://pip.pypa.io/en/stable) and [virtualenv](https://virtualenv.pypa.io/en/stable/) installed. 

Create a new virtualenv in your checked out repo.

    cd /[path_to]/wazoku_test
    virtualenv .


Then install the dependencies:

    bin/pip install -r requirements.txt


Set the default django settings file used by all following commands:

    export DJANGO_SETTINGS_MODULE=exercise.settings


The code in this repo uses an sqlite database as the persistence layer. You can initialize an sqlite database (this db will be stored in the file `./db.sqlite3`)

    bin/python manage.py migrate

There is a simple django `populate_db` command which can be used to prime the database with some example data

    bin/python manage.py populate_db

The user export script can be run with the following:

    bin/python -m scripts.user_activity_export \
      -c example.com \
      -e recipient@email.com

There is also a unit test which can be used to validate the code:

    bin/python manage.py test tests/*



## Exercise 1

Our clients wish to receive a list of inactive users as well as active ones. Given the limitation
of the csv format, we propose generating an Excel document instead of a csv file. Use the
[openpyxl](https://openpyxl.readthedocs.org/) library to modify the code to produce an xlsx document
containing two sheets, the first mirrors the csv with a list of active users and their activity, the
second sheet contains a list of email addresses for those users with no activity on the site.
Feel free to refactor the code any way you see fit.

Please create a pull request for this work.

## Exercise 2

Although the tests are all passing, after a recent refactoring this code appears to have stopped working as
our customers are all reporting they are not receiving the emails when we run the script
(although occasionally the wrong manager does receive an email).
Please identify and fix the problem and issue a second pull request for your fix.

Bonus marks will be awarded for the addition of tests against your fix

## Exercise 3

The current script is not particularly efficient against large customers. Can you improve on
the current code and reduce it's complexity from `O(N)` to `O(1)`. You might want to consider using [assertNumQueries]( https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries) to help you confirm this.

Please create a third pull request for this work.
