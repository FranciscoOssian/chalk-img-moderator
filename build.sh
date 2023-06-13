#!/bin/bash

cd model
wget https://s3.amazonaws.com/ir_public/ai/nsfw_models/nsfw.299x299.h5
cd ..

pip install -r requirements.txt