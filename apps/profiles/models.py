from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase

from workout.models import Team

class Profile(ProfileBase):
  """
  PROFILE
  -------
  Fields available for profile and bio fields.

  """

  #Name that shows up on your profile
  name = models.CharField(_("name"),
    max_length=50, null=True, blank=True)

  #About / Description / Bio
  about = models.TextField(_("about"),
    null=True, blank=True)

  #Graduating Year
  FRESHMAN = 'FR'; SOPHOMORE = 'SO';
  JUNIOR = 'JR'; SENIOR = 'SR'; GRADUATE = 'GR'
  COACH = 'CO'

  GRADUATING_CLASS_CHOICES = (
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
    (GRADUATE, 'Graduate Student'),
    (COACH, 'Coach')
    )

  graduating_class = models.CharField(max_length=2,
    choices=GRADUATING_CLASS_CHOICES,
    default=SOPHOMORE)

  #Queens or Tarts?
  TART = 'TR'; PIE = 'PI'; NO_DESSERT = 'NO'
  DESSERT_CHOICES = (
    (NO_DESSERT, 'None'),
    (TART, 'Tart'),
    (PIE, 'Pie')
    )
  dessert = models.CharField(max_length=2,
    choices=DESSERT_CHOICES,
    default=NO_DESSERT)

  #Teams that the user is part of.
  teams = models.ManyToManyField(Team, blank=True)

  #URL (href) to a photo to use in Bio
  photo_link = models.URLField(_("photo_link"), null=True,
    blank=True, verify_exists=False)

  #location (DISABLED)
  #location  = models.CharField(_("location"), max_length=40, null=True, blank=True)

  # ----- Methods -------
  def is_upperclass(self):
    """Checks if upperclassman"""
    return self.graduating_class in (self.JUNIOR, self.SENIOR, self.GRADUATE)

  def class_str(self):
    """Returns string rep for graduating class"""
    CLASS_STR_DICT = {
        'FR': 'Freshman',
        'SO': 'Sophomore',
        'JR': 'Junior',
        'SR': 'Senior',
        'GR': 'Graduate Student',
        'CO': 'Coach',
        }
    return CLASS_STR_DICT[self.graduating_class]

  def dessert_str(self):
    """Returns string rep for graduating class"""
    DESSERT_STR_DICT = {
        'PI': 'Pie',
        'TR': 'Tart',
        }
    return DESSERT_STR_DICT[self.dessert]
