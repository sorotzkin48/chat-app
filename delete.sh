# delete all images
docker rmi -f $(docker images -aq)

# delete all containers
docker rm -f $(docker ps -a -q)

#delete volume
docker volume rm chat-app-data
