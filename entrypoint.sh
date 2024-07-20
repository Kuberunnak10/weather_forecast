#!/bin/bash

python3 manage.py migrate

python3 manage.py collectstatic --no-input

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

gunicorn core.wsgi:application -b 0.0.0.0:8000