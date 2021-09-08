FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pipenv \
  && pip3 install --upgrade pip


WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --ignore-pipfile

EXPOSE 8000
ADD . /app

# CMD ["gunicorn", "blog.wsgi:application", "-b :8000"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
