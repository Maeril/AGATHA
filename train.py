# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    train.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: myener <myener@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/01 01:13:34 by myener            #+#    #+#              #
#    Updated: 2020/09/01 21:20:41 by myener           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# Import the necessary packages
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from vggnet.vggnet import VGGNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os

# Construct the argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", required=True,
	help="path to input dataset (i.e., directory of images)")
parser.add_argument("-m", "--model", required=True,
	help="path to output model")
parser.add_argument("-l", "--labelbin", required=True,
	help="path to output label binarizer")
parser.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output accuracy/loss plot")
args = vars(parser.parse_args())

# Initialize the number of epochs to train for, initial learning rate,
# batch size, and image dimensions
EPOCHS = 100
INIT_LR = 1e-3 # Basically just another way to write O.OO1 (aka 1 * 10^(-3))
BS = 32
IMAGE_DIMS = (96, 96, 3)
# Initialize the data and labels
data = []
labels = []
# Grab the image paths and randomly shuffle them
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# Loop over the input images
for imagePath in imagePaths:
	# Load the image, pre-process it, and store it in the data list
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
	image = img_to_array(image)
	data.append(image)
	# Extract the class label from the image path and update the
	# Labels list
	label = imagePath.split(os.path.sep)[-2]
	labels.append(label)

# Scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print("[INFO] data matrix: {:.2f}MB".format(
	data.nbytes / (1024 * 1000.0)))
# Binarize the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
# Partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(x_train, x_test, y_train, y_test) = train_test_split(data,
	labels, test_size=0.2, random_state=42)

# Construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# Initialize the model
print("[INFO] compiling model...")
model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
	depth=IMAGE_DIMS[2], classes=len(lb.classes_))
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])
# Train the network
print("[INFO] training network...")
Hist = model.fit(x=aug.flow(x_train, y_train, batch_size=BS),
	validation_data=(x_test, y_test),
	steps_per_epoch=len(x_train) // BS,
	epochs=EPOCHS, verbose=1)

# Save the model
print("[INFO] saving network...")
model.save(args["model"], save_format="tf")
# save the label binarizer to disk
print("[INFO] saving label binarizer...")
f = open(args["labelbin"], "wb") #wb stands for "write binary"
f.write(pickle.dumps(lb))
f.close()

# Create a plot capturing the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), Hist.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), Hist.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), Hist.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), Hist.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")
plt.savefig(args["plot"])
