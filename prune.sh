#!/bin/bash

# Prune containers
docker container prune -f

# Prune images (including dangling images)
docker image prune -f --all

# Prune volumes
docker volume prune -f

# Prune networks
docker network prune -f