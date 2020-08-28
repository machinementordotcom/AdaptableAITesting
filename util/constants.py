
import sys
import os
sys.stdout = open(os.devnull, 'w')
import arcade
import tensorflow as tf
import numpy as np
from tensorflow import keras
import multiprocessing
sys.stdout = sys.__stdout__

RANDOM_SEED = 1

SPRITE_SCALING = 0.5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Adaptive AI"
ARROW_IMAGE_HEIGHT = 7.9
MOVEMENT_SPEED = 3#7.5 
ARROW_SPEED = 12  #20
ANGLE_SPEED = 4
#variables for making walls for arcade viewing and a* algo
VERT_WALL_START=1
VERT_WALL_END=1
VERT_CENTER = 465 # X value
HOR_WALL_START=1
HOR_WALL_END=1
HOR_CENTER = 200 # y value
BOX = 3


PLAYER_HEALTH = 1000#80
SCALING_ADJUSTMENT = PLAYER_HEALTH/80

ARROW_HITS_UNTIL_DEATH = 5.2 * SCALING_ADJUSTMENT #5.5
ARROW_DAMAGE = PLAYER_HEALTH / ARROW_HITS_UNTIL_DEATH
FIREBALL_HITS_UNTIL_DEATH = 5.4 * SCALING_ADJUSTMENT
FIREBALL_DAMAGE = PLAYER_HEALTH / FIREBALL_HITS_UNTIL_DEATH
KNIFE_HITS_UNTIL_DEATH = 3.2 * SCALING_ADJUSTMENT
KNIFE_DAMAGE = PLAYER_HEALTH / KNIFE_HITS_UNTIL_DEATH


SHORT_SPEED_HANDICAP = .145#.955
MID_SPEED_HANDICAP = .09#1




MAGE_IMAGE = 'images/mage.png'
KNIGHT_IMAGE = 'images/lilknight.png'

# def decideWinner(num):
#     health = float(num)
#     if health < 
class Counter(object):
    def __init__(self, initval=0):
        self.val = multiprocessing.RawValue('i', initval)
        self.lock = multiprocessing.Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    @property
    def value(self):
        return self.val.value
class HitBox(arcade.Sprite):
    z = 500
    y = ARROW_IMAGE_HEIGHT
class Knife(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class ArrowSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box
class FireballSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box
        
class Layer:
    def __init__(self, weights):
        self.weights = weights
        
class Network:
    
    def __init__(self, layers): # layers comes from 
        self.layers = layers
    
    def createNetwork(self):
        tensors = []
        results = []
        layer = tf.keras.layers.Dense(1, input_shape=(17,1)) # 17 is input size
        inputs = keras.Input(shape=(17,))
        for i in range(len(self.layers) - 4):
            if len(self.layers)- 5 == 0:
                move_x = tf.keras.layers.Dense(1,activation='tanh')
                move_y = tf.keras.layers.Dense(1,activation='tanh')
                shoot1 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot2 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot3 = tf.keras.layers.Dense(1,activation='sigmoid')
                tensors.append(move_x)
                tensors.append(move_y)
                tensors.append(shoot1)
                tensors.append(shoot2)
                tensors.append(shoot3)
                results.append(move_x(inputs))
                results.append(move_y(inputs))
                results.append(shoot1(inputs))
                results.append(shoot2(inputs))
                results.append(shoot3(inputs))
            elif i == 0:
                h = tf.keras.layers.Dense(len(self.layers[i].weights[0]), activation='relu')
                results.append(h(inputs))
                tensors.append(h)
            elif i <= len(self.layers)- 4 - 2:
                h = tf.keras.layers.Dense(len(self.layers[i].weights[0]), activation='relu')
                results.append(h(results[i-1]))
                tensors.append(h)
            else:
                move_x = tf.keras.layers.Dense(1,activation='tanh')
                move_y = tf.keras.layers.Dense(1,activation='tanh')
                shoot1 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot2 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot3 = tf.keras.layers.Dense(1,activation='sigmoid')
                results.append(move_x(results[i-1]))
                results.append(move_y(results[i-1]))
                results.append(shoot1(results[i-1]))
                results.append(shoot2(results[i-1]))
                results.append(shoot3(results[i-1]))
                tensors.append(move_x)
                tensors.append(move_y)
                tensors.append(shoot1)
                tensors.append(shoot2)
                tensors.append(shoot3)
        counter = 0
        for i in range(len(tensors)):
            if i < len(self.layers) - 5:
                tensors[i].set_weights([np.asarray(self.layers[i].weights),np.zeros(len(self.layers[i].weights[0]))])
            else:
                tensors[i].set_weights([np.asarray(self.layers[i - counter].weights),np.zeros(len(self.layers[i - counter].weights[0]))])
                counter += 1 

        return tf.keras.Model(inputs=inputs, outputs=[results[len(results)-5],results[len(results)-4],results[len(results)-3],results[len(results)-2],results[len(results)-1]])
                



