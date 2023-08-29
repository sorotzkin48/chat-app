# create volume
docker volume create chat-app-data 

# build  images
docker build -t chat_img:1 -f Dockerfile . 

# run image
docker run -d -v chat-app-data:/code --memory=256m --cpus=1  -p 5000:5000 chat_img:1


 