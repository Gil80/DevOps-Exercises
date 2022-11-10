# build nginx 
FROM nginx

# Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

# build the Flask app
# Pick a low configuration python base image
FROM python:alpine
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# create and activate virtual environment
# using final folder name to avoid path issues with packages
#RUN python3 -m venv /home/whist/venve
#ENV VIRTUAL_ENV=/home/whist/venve
#ENV PATH="/home/whist/venve/bin:$PATH"
#RUN source /home/whist/venve/bin/activate
#
## create user without password
#RUN adduser whist -D
#
#WORKDIR /home/whist/app

# Create a folder app in container and work inside it
#WORKDIR /app

COPY /app/requirements.txt .

# Install bash
RUN apk add --no-cache bash

# Install all the requirements
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy all the flask project files into the WORKDIR
COPY . .

# Expose the port 5000 of the docker container
EXPOSE 5000

# Execute flask application inside the container
CMD python3 /app.py
