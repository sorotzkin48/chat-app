#!/bin/bash

# List all containers
echo "Containers:"
docker ps -a

# List all images
echo "Images:"
docker images

# List all volumes
echo "Volumes:"
docker volume ls

# List all networks
echo "Networks:"
docker network ls
