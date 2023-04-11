import os
import cv2
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from keras.models import load_model
from tensorflow.keras.models import Model, load_model
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
upload_folder = os.path.join('static', 'images')

def prepareImage(path):
    IMG_SIZE = 80
    img_array = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.imread(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def predictionWithCNN(path):
    model = load_model(
        ('./cnn2.h5'),
        custom_objects={'KerasLayer':hub.KerasLayer}
        )
    path = "."+path
    x = load_img(path, target_size=(224, 224))
    y = img_to_array(x)
    y = np.expand_dims(y, axis=0)
    time_ini = datetime.now()
    array = model.predict(y)
    time_fin = datetime.now()
    time_tot = (time_fin-time_ini).seconds
    position = np.argmax(array)
    return array, position, time_tot

def imageSegmentation(path):
    path = "."+path
    img_name = os.path.basename(os.path.normpath(path))
    print("img_name", img_name)
    # Imagen segmentada
    img = cv2.imread(path)
    img = cv2.resize(img, (224,224))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    segmented_image = os.path.join(upload_folder, 'seg_'+ img_name)
    # cv2.imwrite(os.path.join(upload_folder, segmented_image), thresh)
    img_seg = Image.fromarray(thresh)
    img_seg.save(segmented_image)
    # Deteccion de bordes
    edges = cv2.Canny(img, 100, 200)
    edges_image = os.path.join(upload_folder, 'edge_'+ img_name)
    img_edg = Image.fromarray(edges)
    img_edg.save(edges_image)
    # cv2.imwrite(os.path.join(upload_folder, edges_image), edges)
    
    # Deteccion de caracteristicas
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    img_with_keypoints = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)
    features_image = os.path.join(upload_folder, 'feat_' + img_name)
    img_feat = Image.fromarray(img_with_keypoints)
    img_feat.save(features_image)
    # cv2.imwrite(os.path.join(upload_folder, features_image), img_with_keypoints)
    return segmented_image, edges_image, features_image
