from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import random


def img_predict(path):
    model_stock = load_model('./module/model_rps.h5')

    img = image.load_img(path, target_size=(200,200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model_stock.predict(images, batch_size=10)

    return classes

def convert_classes(classes):
    if np.all(classes <= [[1, 0, 0]]):
      return "Paper"
    elif np.all(classes <= [[0, 1, 0]]):
      return "Rock"
    else :
      return "Scissors"

def generate_janken():
    janken = ["Paper", "Rock", "Scissors"]
    return random.choice(janken)

def battle(user, comp):
    if user == comp:
        return 0
    elif user == "Rock":
        if comp == "Paper":
            return "Lose"
        else:
            return "Win"
    elif user == "Paper":
        if comp == "Scissors":
            return "Lose"
        else:
            return "Win"
    elif user == "Scissors":
        if comp == "Rock":
            return "Lose"
        else:
            return "Win"

def janken_game(classes):
    user = convert_classes(classes)
    comp = generate_janken()
    game_result = battle(user, comp)

    return user, comp, game_result