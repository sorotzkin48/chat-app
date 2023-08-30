#!/bin/bash

# Stop and remove the chat-app container
docker ps
read -p "Enter container name " container_name
docker stop ${container_name}
docker rm ${container_name}

# Remove the chat-app image
docker images
read -p "Enter image_name:tag " image
docker rmi ${image}