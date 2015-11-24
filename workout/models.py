from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Workout(models.Model):
  """
  WORKOUT
  ------
  Models an individual workout completed by the athlete
  
  """
  #When was the workout?
  workout_date = models.DateField('workout date',
        default = datetime.today())

  #Who did the workout?
  user = models.ForeignKey(User)

  #How long was the workout?
  duration = models.DecimalField(
    max_digits = 5, 
    decimal_places = 2,
    default = 1)

  #What was the workout activity? 
  activity = models.ForeignKey('Activity')

  #With a classmate of a different year?
  with_other_class = models.BooleanField(default=False)

  @property
  def score(self):
    """calculated score"""
    #score = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, editable = False)
    d = self.duration
    m = self.activity.intensity_multiplier

    s = d * m

    #Bonus point for working out with a classmate
    #  from another team
    if self.with_other_class:
      s += 1

    return s

  def __unicode__(self):
    return '{0} | {1:%b-%d} | Score={2}'.format(
        self.user, 
        self.workout_date,
        self.score,
      )

  def get_absolute_url(self):
    """Reverse absolute url to enable generic views"""
    return reverse('workout_detail', kwargs={'pk' : self.pk})

class Activity(models.Model):
  description = models.CharField(max_length=60)
  intensity_multiplier = models.DecimalField(
    max_digits = 5, 
    decimal_places = 2,
    default = 1.0)

  def __unicode__(self): 
    return '{}'.format(self.description)

class Team(models.Model):
  name = models.CharField(max_length=30)

  def __unicode__(self): 
    return '{}'.format(self.name)
