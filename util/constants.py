
from arcade import Sprite
from keras import layers
from keras.layers import Dense, Input, concatenate
from keras.models import Model
import omegaml as om
from AdaptableAITesting.util.constants import *
import pickle

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
MAGE_IMAGE = '/app/pylib/user/AdaptableAITesting/images/mage.png'
KNIGHT_IMAGE = '/app/pylib/user/AdaptableAITesting/images/lilknight.png'


#@ray.remote
class Counter(object):
    def __init__(self, initval=0):
        pass
#        self.val = multiprocessing.RawValue('i', initval)
#        self.lock = multiprocessing.Lock()

#    @property
#    def value(self):
#        return self.val.value
 
#@ray.remote
class HitBox(Sprite):
    z = 500
    y = ARROW_IMAGE_HEIGHT

#@ray.remote
class Knife(Sprite):
    def update(self, rounds=None, process_id=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

#@ray.remote
class Arrow(Sprite):
    def update(self, rounds=None, process_id=None):
        self.center_x += self.change_x
        self.center_y += self.change_y

#@ray.remote
class Fireball(Sprite):
    def update(self, rounds=None, process_id=None):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
#@ray.remote
class ArrowSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box
        
#@ray.remote
class FireballSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box

#@ray.remote
class Layer:
    def __init__(self, weights):
        self.weights = weights

#@ray.remote
class Network:
    
    def __init__(self, layers): # layers comes from 
        self.layers = layers
            
    ## NH - corrected structure of output layers - instead of 5 separate layers, there are now
    # 2 layers, one for moves and one for attacks, with 2 and 3 output variables respectively
    
    def createNetwork(self, rounds, process_id):
        
        ## If network already exists, retrieve that model from omega and return it
#        print("CreateNetwork object passed in (self):",self)
        
        layer = layers.Dense(1, input_shape=(17,)) # NH - corrected shape of input tensor
#       print("layer var",layer)
        inputs = Input(shape=(17,))
#        print("inputs var",inputs)
#        print("Range for loop is",len(self.layers),"minus 1")
        for i in range(len(self.layers) + 2):
            if len(self.layers) - 2 == 0:
#                print("short network - only 2 layers")
                moves = layers.Dense(2, activation='tanh')(inputs)
                attacks = layers.Dense(3, activation='sigmoid')(inputs)
                outputs = concatenate([moves, attacks])
#               outputs = Dense(5, activation = 'softmax')(concat)
            elif i == 0:
#                print("i == 0, first layer")
                h = layers.Dense(len(self.layers[i].weights[0]), activation='elu')(inputs)
#                print("self.layers",len(self.layers[i].weights[0]))
            elif i < len(self.layers):
#                print("i <= tensors")
                h = layers.Dense(len(self.layers[i].weights[0]), activation='elu')(h)
#                print("self.layers",len(self.layers[i].weights[0]))
            else:
#                print("outputs")
                moves = layers.Dense(2, activation='tanh')(h)
                attacks = layers.Dense(3, activation='sigmoid')(h)
                outputs = concatenate([moves, attacks])
#               outputs = Dense(5, activation = 'softmax')(concat)
        
        model = Model(inputs=inputs,
                              outputs=outputs)
               
        ## Compile the model prior to saving
        model.compile('adadelta','mean_squared_error')
<<<<<<< HEAD

=======
        """     
#        model_id = 'gen%dp%d' % (rounds, process_id)
        
#        print("Attempting to pickle %s net" % model_id)
#        filename = str('/app/pylib/user/AdaptableAITesting/models/%s' % model_id) + ".pickle"        
#        with open(filename, 'wb') as handle:
#            pickle.dump(self, handle)
            
#        om.store.put(self, 'gen%dp%d' % (rounds, process_id))
        
        ## Save model via pickle
        #dump_object(str(model), model)
        
#        om.models.put(model, 'gen%dp%d' % (rounds, process_id))
#        model = om.runtime.require('gpu').model('gen%dp%d' % (rounds, process_id))
#        print("Model gen%dp%d stored in omega cloud" % (rounds, process_id))

        #counter = 0
        """        
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
        return model
                


