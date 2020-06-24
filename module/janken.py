from keras.preprocessing import image
from keras.models import load_model
import numpy as np

def img_predict(path):
    model_stock = load_model('./src/static/model/model_rps.h5')
    
    img = image.load_img(path, target_size=(200,200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model_stock.predict(images, batch_size=10)

    return classes