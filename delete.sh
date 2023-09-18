#added
# Stop and remove the running container
docker stop chat-app
docker rm chat-app
# Delete the image
docker rmi chat_img:${version}


# # delete all images
# docker rmi -f $(docker images -aq)

# # delete all containers
# docker rm -f $(docker ps -a -q)

#delete volume
docker volume rm chat-app-data
