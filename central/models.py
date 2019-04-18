from django.contrib.sites.models import Site
from django.db import models


class TimestampModel(models.Model):
    """
    An abstract model that provides self-updating 'created' and 'modified'
    fields
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'central'


class Idea(TimestampModel):
    """
    This object represent an idea on the spotlight website.
    """
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'central'


class IdeaFeatureVector(models.Model):
    idea = models.OneToOneField(
        Idea,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='idea_feature_vector',
    )
    tfidfs = models.TextField(blank=True)

    class Meta:
        app_label = 'central'


class Recommendation(models.Model):
    similarity = models.FloatField(default=0)
    idea_1 = models.ForeignKey(
        Idea,
        models.CASCADE,
        related_name='recommendations_as_idea_1',
    )
    idea_2 = models.ForeignKey(
        Idea,
        models.CASCADE,
        related_name='recommendations_as_idea_2',
    )

    class Meta:
        app_label = 'central'
