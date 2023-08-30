check_valid() {
    # Validate tag name using regex
    regex_pattern="^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"

    if ! [[ $1 =~ $regex_pattern ]]; then
        return 1  # Return a non-zero value to indicate failure
    fi
    return 0  # Return 0 to indicate success
}

read -p "Enter version: " version
git log
read -p "Enter commit hash: " commit_hash

if check_valid "$version"; then
    git tag "$version" "$commit_hash"
    git push origin "$version"
    docker build -t "chat-app:$version" .
else
    echo "Invalid tag name format. Please use semantic versioning (e.g., v1.0.0)!"
    exit 1
fi