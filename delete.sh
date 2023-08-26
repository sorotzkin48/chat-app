docker rmi -f $(docker images -aq)
docker rm -f $(docker ps -a -q)
docker volume rm chat-app-data