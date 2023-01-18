import tensorflow as tf
import keras
from keras.models import model_from_json
import numpy as np
import matplotlib.image as mpimg
import cv2

IMG_HEIGHT = 48
IMG_WIDTH = 48

class Model(object):
    EMOTE_LIST = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral']

    def __init__(self, model_json, model_weights):
        with open(model_json, "r") as json_file:
            loaded_model = json_file.read()
            self.loaded_model = model_from_json(loaded_model)

        self.loaded_model.load_weights(model_weights)

    def load_img_from_path(self, image_path):
        image=mpimg.imread(image_path)
        image= cv2.imread(image_path, cv2.COLOR_BGR2RGB)
        image= cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH), interpolation = cv2.INTER_AREA)
        images_arr = []
        images_arr.append(np.array(image))
        img = np.asarray(images_arr)
        img= img.astype('float32')
        img /= 255
        return img

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return Model.EMOTE_LIST[np.argmax(self.preds)]
            


