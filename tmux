rename-session instagram-chat
send " ./manage.py runserver" C-m
new-window
send " $BROWSER http://localhost:8080/" C-m
new-window
send " cd db ; docker-compose up" C-m
new-window
send " vim ." C-m

