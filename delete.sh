# delete all images
docker rmi -f $(docker images -aq)

# delete all containers
docker rm -f $(docker ps -a -q)
<<<<<<< HEAD
docker volume rm chat-app-data
=======

#delete volume
docker volume rm chat-app-data
>>>>>>> b83ee59cf6374b19ceecddd428313a5757e84e57
