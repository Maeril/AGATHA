# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: myener <myener@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/02 04:12:23 by myener            #+#    #+#              #
#    Updated: 2020/09/01 21:50:28 by myener           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Import the necessary packages
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

# Construct the argument parser and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", required=True,
	help="path to trained model")
parser.add_argument("-l", "--labelbin", required=True,
	help="path to label binarizer")
parser.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(parser.parse_args())

# Load the image
image = cv2.imread(args["image"])
output = image.copy()

# Pre-process the image for classification
image = cv2.resize(image, (96, 96))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# Load the trained convolutional neural network and the label
# binarizer
print("[INFO] loading network...")
model = load_model(args["model"])
lb = pickle.loads(open(args["labelbin"], "rb").read())
# Classify the input image
print("[INFO] classifying image...")
proba = model.predict(image)[0]
idx = np.argmax(proba)
label = lb.classes_[idx]

# Prediction is "correct" if image filename contains predicted label text
filename = args["image"][args["image"].rfind(os.path.sep) + 1:]
correct = "correct" if filename.rfind(label) != -1 else "incorrect"
# Build the label and draw the label on the image
label = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
output = imutils.resize(output, width=400)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	0.7, (0, 255, 0), 2)
# Display the output image
print("[INFO] {}".format(label))
cv2.imshow("Output", output)
cv2.waitKey(500)