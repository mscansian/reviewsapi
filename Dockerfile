FROM python:3.6-alpine
ENV PYTHONUNBUFFERED=1

ADD requirements.txt /
RUN pip install -r /requirements.txt

RUN adduser -Ds /bin/sh django
USER django

WORKDIR /var/www
ADD webservice /var/www

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
