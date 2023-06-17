#!/bin/bash

# Get the absolute directory of the script
script_dir=$(dirname "$(realpath "$0")")

# Navigate to the project root from the script's directory
project_root="$script_dir/.."

# Download a file to the models directory
wget -P "$project_root/models" https://s3.amazonaws.com/ir_public/ai/nsfw_models/nsfw.299x299.h5

# Install the dependencies listed in requirements.txt
pip install -r "$project_root/requirements.txt"
