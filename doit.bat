color 18
title OldEgg WebServer
py manage.py makemigrations
py manage.py migrate
start /max http://localhost:8000/
start /max http://localhost:8000/admin
py manage.py runserver 8000