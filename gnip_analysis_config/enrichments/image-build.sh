#!/usr/bin/env bash

# "strict mode"
set -e

echo "$(date +%Y-%m-%d\ %H:%M:%S) -- started running $0"
echo "$(date +%Y-%m-%d\ %H:%M:%S) -- checking for python environment"

# TODO: add check for conda env too, generalize the path var below
# check if  ${CONDA_DEFAULT_ENV} serves this role wrt conda (via Aaron)
if [[ -z ${VIRTUAL_ENV} ]]; then
    echo
    echo "Please build a Python3 virtualenv prior to running this script."
    echo 
    exit 0
fi

echo "$(date +%Y-%m-%d\ %H:%M:%S) -- installing python libraries (takes a bit the first time)"
${VIRTUAL_ENV}/bin/pip install -U pip > /dev/null
${VIRTUAL_ENV}/bin/pip install -r image-reqs.txt > /dev/null

echo "$(date +%Y-%m-%d\ %H:%M:%S) -- running minimal example to download weights and codes to ~"
${VIRTUAL_ENV}/bin/python - << EOM
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image as k_image
import numpy as np
from PIL import Image
from io import BytesIO
import requests
# instantiate model (will download weights) 
model = VGG16(weights='imagenet')
# make a prediction (will download labels) 
response = requests.get('https://pbs.twimg.com/profile_images/620254280490979328/M88ZsuCT_400x400.jpg')
img = Image.open(BytesIO(response.content)).convert('RGB').resize((224,224))
proc_img = preprocess_input(np.expand_dims(k_image.img_to_array(img), axis=0))
output = decode_predictions(model.predict(proc_img), top=5)[0]
EOM

echo 
echo "$(date +%Y-%m-%d\ %H:%M:%S) -- successful. finished running $0"

