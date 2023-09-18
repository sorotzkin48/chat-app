# create volume
docker volume create chat-app-data 

read -p "Enter version you want to run " version

# build  images
docker build -t chat_img:${version} -f Dockerfile . 

# run image
docker run -v chat-app-data:/code/$ROOMS_DIR -v chat-app-data:/code/users --name chat-app --memory=256m --cpus=1  -p 5000:5000 chat_img:${version}