# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

#install dependency
RUN pip install -r /usr/src/app/requirements.txt

# copy project
COPY . /usr/src/app/