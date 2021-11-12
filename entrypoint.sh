#!/bin/sh

# Migrate database
echo "Creating database..."
python manage.py migrate

# Ceate superuser
echo "Creating super user..."
python manage.py createsuperuser --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting the server..."
if [ $DEPLOY = "0" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    uwsgi --socket :29000 --module moodle_csv_prof.wsgi --master --enable-threads --uid=505 --gid=505
fi