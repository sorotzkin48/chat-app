docker build -t chat_image:1 .
docker run -v user_data:/code -p 5000:5000 chat_image:1
