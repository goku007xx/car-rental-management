FROM python

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
# Dont copy .pyc files to the container

ENV PYTHONUNBUFFERED 1  
# Make python output come to the terminal for log checks.

COPY . .

RUN apt-get update && apt-get install -y postgresql postgresql-contrib libpq-dev sudo
RUN pip3 install -r reqs/requirements.txt

EXPOSE 8000

RUN reqs/db_dep.sh
# Runs during the build step

ENTRYPOINT reqs/server_run.sh
# Runs only when container is started