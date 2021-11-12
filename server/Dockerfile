FROM nginx:1.21.3-alpine

COPY default.conf /etc/nginx/conf.d/default.conf
COPY uwsgi_params /etc/nginx/uwsgi_params

# Create static folder
RUN mkdir /static
RUN chmod 755 /static