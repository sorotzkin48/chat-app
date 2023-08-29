docker volume create chat-app-data 
docker build -t chat_img:1 .
docker run -v chat-app-data:/code -p 5000:5000 chat_img:1