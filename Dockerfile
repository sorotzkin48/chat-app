# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# retrieve the rooms/ dir as an environment variable
ENV ROOMS_DIR='rooms/'

# change the enviroment to be development
ENV FLASK_ENV development

# install dependencies
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./chatApp.py" ]
