# create volume
docker volume create chat-app-data 

# build  images
docker build -t chat_img:1 .

# run image
docker run -v chat-app-data:/code -p 5000:5000 chat_img:1
