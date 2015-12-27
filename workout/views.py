from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.core.urlresolvers import reverse_lazy

from collections import defaultdict
from decimal import Decimal
from django.utils import simplejson

from workout.models import Workout, Activity, Team, User
from apps.profiles.models import Profile

import operator


@login_required
def index(request):
    """
    Index View
    -----------
    Shows a list of recent workouts by all Users
    Perhaps a list of current user's recent workouts
    Good place for a scoreboard.
    """
    try:
        recent_workouts = Workout.objects.all().order_by('workout_date')
    except ObjectDoesNotExist:
        recent_workouts = []

    return render_to_response(
        'workout/workouts_home.html',
        {'workouts': recent_workouts},
        context_instance=RequestContext(request)
    )


def indiv(request):
    pdict = defaultdict(int)
    for ww in Workout.objects.all():
        pdict[ww.user.username] += float(ww.score)

    pdict = dict(pdict)

    rankedlist = sorted(
        pdict.iteritems(),
        key=operator.itemgetter(1),
        reverse=True)

    userinfo = []
    for user, score in rankedlist:
        pp = Profile.objects.filter(user__username__iexact=user)[0]
        userinfo.append((user, score, pp.class_str(), pp.dessert_str()))

    return render_to_response(
        'workout/workouts_indiv.html',
        {'ranked_players': userinfo},
        context_instance=RequestContext(request)
    )


def playerlist(request):
    """
    List of players participating, ranked by points
    """
    pdict = defaultdict(int)
    for ww in Workout.objects.all():
        pdict[ww.user.username] += float(ww.score)

    rankedlist = sorted(
        pdict.iteritems(),
        key=operator.itemgetter(1),
        reverse=True)

    return render_to_response(
        'workout/workouts_indiv.html',
        {'ranked_players': rankedlist},
        context_instance=RequestContext(request)
        )


def profiles(request):
    pass


def scoreboard(request):
    """
    Scoreboard View
    ---------------
    Shows the scoreboards.
    1. Total for each class
    2. Total for each team
    """

    # Commenting out b/c not using pie/tart distinction in 2015
    # class_list_PI, class_dict_PI = _gclass_query(dessert = 'PI')
    # class_list_TR, class_dict_TR = _gclass_query(dessert = 'TR')
    # ... instead:
    class_list, class_dict = _gclass_query()

    # For Teams
    all_teams = [t.name for t in Team.objects.all()]
    team_scores = []

    for team in all_teams:
        q = Workout.objects.filter(
            user__profile__teams__name=team
            )
    # Get total workout score for each Team.
    iscore = 0
    for iworkout in q:
        iscore += iworkout.score

    team_scores.append([team, iscore])

    return render_to_response(
        'workout/scoreboard.html',
        {
            'team_scores': team_scores,
            # 'class_dict_PI': dict(class_dict_PI),
            # 'class_list_PI': simplejson.dumps(class_list_PI),
            # 'class_dict_TR': dict(class_dict_TR),
            # 'class_list_TR': simplejson.dumps(class_list_TR),
            'class_dict_BOTH': dict(class_dict),
            'class_list_BOTH': simplejson.dumps(class_list),
        },
        context_instance=RequestContext(request)
    )


def _gclass_query(dessert=None):
    """
    Calculates workout scores by class
    with option to subdivid by dessert (pies vs tarts)
    """
    CLASS_YEARS = ['FR', 'SO', 'JR', 'SR', 'GR', 'CO']
    class_dict = defaultdict(Decimal)

    class_list = []
    class_list.append(['Class', 'Points'])

    for gclass in CLASS_YEARS:
        # Get number of players in class
        if dessert is not None:
            n_players = len(
                User.objects.filter(
                    profile__dessert__iexact=dessert).filter(
                    profile__graduating_class__iexact=gclass)
                )
        else:  # i.e., if dessert is None
            n_players = len(
                User.objects.filter(
                    profile__graduating_class__iexact=gclass)
                )

    iscore = 0

    # Get all workouts for each Year
    if dessert is not None:
        q = Workout.objects.filter(
            user__profile__dessert__iexact=dessert).filter(
            user__profile__graduating_class__iexact=gclass
        )
    else:  # i.e., if dessert is None
        q = Workout.objects.filter(
            user__profile__graduating_class__iexact=gclass
        )

    # get total workout score for each Year
    for iworkout in q:
        iscore += iworkout.score

    # Normalize scores by n_players in the class
    # with: iscore / n_players
    if n_players > 0:
        normed = float(iscore / n_players)
    elif n_players == 0:
        normed = 0
    class_list.append([gclass, normed])
    # Tuple with both total and normalized scores
    class_dict[gclass] = (normed, iscore)

    return class_list, class_dict


@login_required
def add(request):
    """
    Add View
    ------------
    Fill out a CreateForm for a workout
    Simple form entry here, maybe a default view?
    Need dropdown for workout options
    """
    context_data = {}

    if request.method == 'POST':
        '''
        Form has been submitted. Run checks and cleans and save
        '''
        # Get all data here
        workout = Workout()

        workout.duration = request.POST['duration']
        if 'with_other_class' in request.POST:
            if request.POST['with_other_class'] == 'on':
                workout.with_other_class = True

        # Manage Dates
        try:
            workout.workout_date = request.POST['workout_date']
        except:
            year = request.POST['workout_date_year']
            month = request.POST['workout_date_month']
            day = request.POST['workout_date_day']
            workout.workout_date = '{}-{}-{}'.format(year, month, day)

        workout.activity_id = request.POST['activity']

        # Populate user data
        user = request.user
        workout.user_id = user.pk

        # Create bound form
        # form = WorkoutFormCreate(data = workout_data )

        try:
            # VALID DATA
            workout.save()
            context_data['message'] = "Data submitted."

            return render_to_response(
                'workout/workouts_submit.html',
                context_data, context_instance=RequestContext(request),
                )
        except:
            # INVALID DATA
            context_data['message'] = \
                "Invalid Data Submitted. Please try again."

    '''
    ELSE if request.method != POST)
    Form has not yet been submitted. Create new form.
    '''

    # Create unbound form
    context_data['form'] = WorkoutFormCreate(user=request.user)
    # form = WorkoutFormCreate(user = request.user )

    return render_to_response(
        'workout/workout_form.html',
        context_data,
        context_instance=RequestContext(request),
        )


"""
Form Stuff
"""

from django.forms import ModelForm, ModelChoiceField
from django.forms.fields import DecimalField, BooleanField, DateField
# from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime, date
from django.forms.extras.widgets import SelectDateWidget


class WorkoutFormCreate(ModelForm):
    duration = DecimalField(
        min_value=0, max_value=40, max_digits=5,
        label="Duration (15 min blocks)",
        help_text="e.g., for a 30 minute workout, enter '2'."
        )

    with_other_class = BooleanField(
        label="With different class?",
        help_text="BONUS POINTS! Select this if you worked out with" +
        "a teammates from a different graduating class, like a" +
        "Sophomore with a Junior."
        )

    workout_date = DateField(
        initial=datetime.today,
        widget=SelectDateWidget(years=(2014, 2015)),
        label="Workout Date",
        help_text="When did you do the workout?"
        )

    activity = ModelChoiceField(
        queryset=Activity.objects.order_by('description'))

    class Meta:
        model = Workout
        fields = [   # Appears in the form in this order:
            'workout_date',
            'activity',
            'with_other_class',
            'duration', ]
        exclude = ['user', ]

    def __init__(self, user=None, *args, **kwargs):
        super(WorkoutFormCreate, self).__init__(*args, **kwargs)
        self._user = user


"""
Stats stuff
"""


def stats_view(request):
    """
    Display some very basic statistics
    """
    stats = {}

    stats['n_workouts'] = Workout.objects.all().count()
    stats['n_queens'] = Workout.objects.values('user').distinct().count()
    stats['n_days'] = (date.today() - date(2015, 12, 21)).days


    return render_to_response(
        'workout/workouts_stats.html',
        {'stats' : stats},
        context_instance=RequestContext(request)
    )
