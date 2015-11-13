 rm dev.db 
 python manage.py syncdb
 python manage.py loaddata fixtures/users.json 
 python manage.py loaddata fixtures/workout.json 
 python manage.py loaddata fixtures/class_teams.json 
