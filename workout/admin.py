from django.contrib import admin

from workout.models import Workout, Activity, Team

class ActivityAdmin(admin.ModelAdmin):

  #fields to show in Admin change list
  list_display = ('description', 'intensity_multiplier')


  #Filter options on right filter bar
  list_filter = ['intensity_multiplier']

admin.site.register(Workout)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Team)
