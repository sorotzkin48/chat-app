#!/bin/bash

check_valid() {
    regex_pattern="^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"
    if ! [[ $1 =~ $regex_pattern ]]; then
        return 1
    fi
    return 0
}

read -p "Enter version: " version
git log
read -p "Enter commit hash: " commit_hash

if check_valid "$version"; then
    # Check if the Docker image with the same tag already exists
    if docker image inspect "chat-app:$version" &> /dev/null; then
        read -p "Image chat-app:$version already exists. Do you want to rebuild it? (y/n): " rebuild
        if [[ "$rebuild" == "y" ]]; then
            # Delete the existing image
            docker rmi "chat-app:$version"
        else
            echo "Using existing image chat-app:$version."
        fi
    fi

    # Build the Docker image
    docker build -t "chat-app:$version" .

    # Push the image to Artifact Registry (assuming you have impersonation set up)
    read -p "Do you want to push the image to Artifact Registry? (y/n): " push_to_registry
    if [[ "$push_to_registry" == "y" ]]; then
        # Use service account impersonation
        gcloud auth activate-service-account --key-file=/path/to/artifact-admin-sa-key.json --impersonate-service-account=artifact-admin-sa@your-project-id.iam.gserviceaccount.com

        # Tag the image for Artifact Registry
        docker tag "chat-app:$version" "gcr.io/your-project-id/chat-app:$version"

        # Push the image to Artifact Registry
        docker push "gcr.io/your-project-id/chat-app:$version"

        echo "Image chat-app:$version pushed to Artifact Registry."
    else
        echo "Image not pushed to Artifact Registry."
    fi

    # Create a Git tag
    git tag "$version" "$commit_hash"
    read -p "Do you want to push the tag to GitHub? (y/n): " push_tag
    if [[ "$push_tag" == "y" ]]; then
        git push origin "$version"
    else
        echo "Tag not pushed to GitHub."
    fi
else
    echo "Invalid tag name format. Please use semantic versioning (e.g., v1.0.0)!"
    exit 1
fi
