from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import ListView

from workout.models import Workout

urlpatterns = patterns('workout.views',
    url(r'^$', 'index', name='index'),
    url(r'add/$', "add", name='workout_add'),
    url(r'indiv/$', "indiv", name='indiv'),
    url(r'test/$', "test", name='test'),
    url(r'stats/$', "stats_view", name='stats'),

    #Generic
    #url(r'add/$', WorkoutCreate.as_view(), name='workout_add'),
    url(r'^list/$',
        ListView.as_view(
            queryset=Workout.objects.order_by('-workout_date'),
            context_object_name='workouts',
            template_name='workout/workouts_home.html'),
        name='workout_list'),


    #reference
    url(r"^direct_test$", direct_to_template, {
        "template": "workout/workouts_home.html",
        }, name="workouts_home"),
    )
