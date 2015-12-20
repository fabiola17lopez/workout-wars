from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer
from idios.views import ProfileDetailView

handler500 = "pinax.views.server_error"

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),

    #Override profile view before idios include
    url(r"^profiles/test$",
       'workout.views.profiles',
       name = "new_profiles_view"),
    url(r"^profile/(?P<username>[\w\._@-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),

    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),

    url(r"^workouts/", include("workout.urls")),
    url(r'scoreboard$', 'workout.views.scoreboard', name='scoreboard'),
    #url(r"^enter_workout$", "workout.views.index", name="workout_home")
  )


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
