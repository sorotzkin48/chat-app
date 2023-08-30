# Use an official Python runtime as a parent image
FROM python:3.8-slim AS reduce_docker_image
 
# Set the working directory to /code in the build stage
WORKDIR /code

# Set an environment variable for the directory where room files will be stored
ENV ROOMS_DIR='rooms/'

# Set the Flask environment to development
ENV FLASK_ENV development

# Copy the debug script and requirements file to the build stage
COPY debug.sh requirements.txt .

RUN apt-get update && apt-get install -y curl

# Install Python dependencies from requirements file
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt 

# Copy the rest of the application code to the build stage
COPY . .

# Stage 2: Final Image
# Use the reduced Docker image as the base image
FROM reduce_docker_image

# Copy the content from the build stage to the final image
COPY --from=reduce_docker_image /code /code

# Set the working directory for the final image (optional)
# WORKDIR /code

HEALTHCHECK --interval=10s --timeout=3s CMD curl --fail http://localhost:5000/health || exit 1

# Command to run when the container starts
CMD [ "python", "./chatApp.py" ]