# create volume
docker volume create chat-app-data 

#changed
gcloud compute ssh [INSTANCE_NAME] --zone [INSTANCE_ZONE]
gcloud auth configure-docker
docker pull chat_img:${version}
#docker run chat_img:${version}


# read -p "Enter version you want to run " version

# # build  images
# docker build -t chat_img:${version} -f Dockerfile . 

# # run image
 docker run -v chat-app-data:/code/$ROOMS_DIR -v chat-app-data:/code/users --name chat-app --memory=256m --cpus=1  -p 5000:5000 chat_img:${version}