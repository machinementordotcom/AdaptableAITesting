
import sys
import os
import arcade
import tensorflow as tf
import numpy as np
from tensorflow import keras
import multiprocessing
from keras.layers import Dense, Input, concatenate
from keras.models import Model
import omegaml as om

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
    def update(self, rounds=None, process_id=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Arrow(arcade.Sprite):
    def update(self, rounds=None, process_id=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Fireball(arcade.Sprite):
    def update(self, rounds=None, process_id=None):
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
        
    ## NH - corrected structure of output layers - instead of 5 separate layers, there are now
    # 2 layers, one for moves and one for attacks, with 2 and 3 output variables respectively
    
    def createNetwork(self, rounds, process_id):
        
        ## If network already exists, retrieve that model from omega and return it
#        print("CreateNetwork object passed in (self):",self)
        
        layer = tf.keras.layers.Dense(1, input_shape=(17,)) # NH - corrected shape of input tensor
#       print("layer var",layer)
        inputs = keras.Input(shape=(17,))
#        print("inputs var",inputs)
#        print("Range for loop is",len(self.layers),"minus 1")
        for i in range(len(self.layers) + 2):
            if len(self.layers) - 2 == 0:
#                print("short network - only 2 layers")
                moves = tf.keras.layers.Dense(2, activation='linear')(inputs)
                attacks = tf.keras.layers.Dense(3, activation='sigmoid')(inputs)
                outputs = concatenate([moves, attacks])
#               outputs = Dense(5, activation = 'softmax')(concat)
            elif i == 0:
#                print("i == 0, first layer")
                h = tf.keras.layers.Dense(len(self.layers[i].weights[0]), activation='relu')(inputs)
#                print("self.layers",len(self.layers[i].weights[0]))
            elif i < len(self.layers):
#                print("i <= tensors")
                h = tf.keras.layers.Dense(len(self.layers[i].weights[0]), activation='relu')(h)
#                print("self.layers",len(self.layers[i].weights[0]))
            else:
#                print("outputs")
                moves = tf.keras.layers.Dense(2, activation='tanh')(h)
                attacks = tf.keras.layers.Dense(3, activation='sigmoid')(h)
                outputs = concatenate([moves, attacks])
#               outputs = Dense(5, activation = 'softmax')(concat)
        
        model = tf.keras.Model(inputs=inputs,
                              outputs=outputs)
               
        ## Save the model (either H5 or omega) for later access
        model.compile('adam','mean_squared_error')
        om.models.put(model, 'gen%dp%d' % (rounds, process_id))
#        model = om.runtime.require('gpu').model('gen%dp%d' % (rounds, process_id))
        print("Model gen%dp%d stored in omega cloud" % (rounds, process_id))

        counter = 0
        
        return model
                


