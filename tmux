rename-session instagram-chat

send " ./manage.py runserver" C-m
rename-window "django-server"

new-window
send " cd db ; docker-compose up" C-m
rename-window "db-docker"

new-window
send " vim ." C-m
rename-window "vim"

