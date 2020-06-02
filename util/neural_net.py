import sys
import os
sys.stdout = open(os.devnull, 'w')

import tensorflow as tf
import numpy as np
from tensorflow import keras

from .constants import DEBUG,\
    NORMALIZE_WEIGHTS, \
    GENE_LENGTH

sys.stdout = sys.__stdout__


class Network:
    """
    This class creates basic Artificial Neural network
    """
    def __init__(self, layers):
        self.layers = layers


    def createNetwork(self, adaptive = False):
        if adaptive:
            net = AdaptiveNetwork(self.layers)
            return net.createNetwork()
        else:
            tensors = []
            results = []
            layer = tf.keras.layers.Dense(1, input_shape=(17,1))
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
                    
    
    
class AdaptiveNetwork:
    """
    This class creates Artificial Neural Network along with adding layer of
    Recurrent Neural Netowrk
    """
    def __init__(self, layers):
        #layers is a list of Layer objects, each of which has a list of weights
        self.layers = layers

    def createNetwork(self, adaptive = True):
        # Set CPU as available physical device
        my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
        tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')
        
        tensors = []
        results = []
        inputs = keras.Input(shape=(17,),batch_size =1,name = 'inputs')
        hidden_activations = []
        for i in range(len(self.layers) - 4):
            if len(self.layers)== 5:
                move_x = tf.keras.layers.Dense(1,activation='tanh')
                move_y = tf.keras.layers.Dense(1,activation='tanh')
                shoot1 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot2 = tf.keras.layers.Dense(1,activation='sigmoid')
                shoot3 = tf.keras.layers.Dense(1,activation='sigmoid')
                #The adaptive layer is a recurrent LSTM layer which recieves normalized 
                #inputs from the last dense hidden layer.  The weights for the hidden layer
                #are based on the hidden weights for the first 3 layers        
                adaptive_layer = tf.keras.layers.GRU(6, time_major = True, stateful = True,activity_regularizer=tf.keras.regularizers.l2(0.01))
                adaptive_inputs = tf.expand_dims(inputs,0)   
                adaptive_outputs = adaptive_layer(adaptive_inputs)
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
                if DEBUG: hidden_activations.append(h.output)
            elif i <= len(self.layers)- 4 - 2:
                h = tf.keras.layers.Dense(len(self.layers[i].weights[0]), activation='relu')
                normed_inputs = tf.keras.layers.LayerNormalization()(results[i-1])
                results.append(h(normed_inputs))
                tensors.append(h)
                if DEBUG: hidden_activations.append(h.output)
            else:
                move_x = tf.keras.layers.Dense(1,activation='tanh', name = 'move_x')
                move_y = tf.keras.layers.Dense(1,activation='tanh',name = 'move_y' )
                shoot1 = tf.keras.layers.Dense(1,activation='sigmoid',name = 'shoot1')
                shoot2 = tf.keras.layers.Dense(1,activation='sigmoid',name = 'shoot2')
                shoot3 = tf.keras.layers.Dense(1,activation='sigmoid',name = 'shoot3')
                 #The adaptive layer is a recurrent LSTM layer which recieves normalized 
                #inputs from the last dense hidden layer.  The weights for the hidden layer
                #are based on the hidden weights for the first 3 layers     
                normed_inputs = tf.keras.layers.LayerNormalization()(results[i-1])
                adaptive_layer = tf.keras.layers.GRU(6, 
                                                     time_major = True, 
                                                     stateful = True,
                                                     activity_regularizer=tf.keras.regularizers.l2(0.01),
                                                     name = 'adaptive_targets')
                adaptive_inputs = tf.expand_dims(normed_inputs,0)   
                adaptive_outputs = adaptive_layer(adaptive_inputs)
                results.append(move_x(normed_inputs))
                results.append(move_y(normed_inputs))
                results.append(shoot1(normed_inputs))
                results.append(shoot2(normed_inputs))
                results.append(shoot3(normed_inputs))
                tensors.append(move_x)
                tensors.append(move_y)
                tensors.append(shoot1)
                tensors.append(shoot2)
                tensors.append(shoot3)
                
        counter = 0
        for i in range(len(tensors)):
            if i < len(self.layers) - 5:
                weights = np.asarray(self.layers[i].weights)
                
                if NORMALIZE_WEIGHTS:
                    fan_out = weights.shape[1]
                    last_width = weights.shape[0]
                    if i == 0: 
                        fan_in = 17
                    else: 
                        fan_in = last_width
                    target_std = np.sqrt(2/(fan_in + fan_out)) #rescale to gloirot
                    weights = weights/np.std(weights)*target_std
                
                tensors[i].set_weights([weights,np.zeros(len(self.layers[i].weights[0]))])
                
            else:
                tensors[i].set_weights([np.asarray(self.layers[i - counter].weights),np.zeros(len(self.layers[i - counter].weights[0]))])
                counter += 1 
                
       
        
        #current weights are read to get the proper shape
        input_weights,hidden_weights, bias = adaptive_layer.get_weights()

        weight_list = []
        counter = 0
        for weights in [input_weights, hidden_weights, bias]:          
            #Input weights are based on the first layer weights
            #Hidden unit weights are based on the second layer weights
            #Bias is based on the 3rd layer weights
            first_layer_weights = np.asarray(self.layers[counter].weights)[0] 
            if counter == 0:
                learn_rate = first_layer_weights[0]/10 
            counter+=1
            weights_1d = np.ravel(first_layer_weights)
            times_to_repeat = np.ceil(weights.size / weights_1d.size).astype(int)  
            
            #Each weight used for the adaptive layer is based on alternating addition and 
            #subtraction of the weights used for the first three layers
            weights_1d = np.tile(weights_1d, times_to_repeat)[:weights.size]
            new_weights = np.copy(weights_1d)
            for i in range(1,GENE_LENGTH):
                if i%2 ==0:
                    new_weights += np.roll(weights_1d,i)
                else:
                    new_weights -= np.roll(weights_1d,i)
            assert not np.isnan(np.sum(new_weights))        
            new_weights -= np.mean(new_weights)
            new_weights /= np.std(new_weights)
            weight_list.append(np.reshape(new_weights,weights.shape))
        import pickle 
        
        if DEBUG:
            with open('weights_dump.p','wb') as f:
                  pickle.dump([weight_list,new_weights, weights_1d,first_layer_weights],f)
        adaptive_layer.set_weights(np.asarray(weight_list))
        
        output=[results[len(results)-5],
                        results[len(results)-4],
                        results[len(results)-3],
                        results[len(results)-2],
                        results[len(results)-1],
                        adaptive_outputs]
        if DEBUG:
            output.append(hidden_activations)
            pass
            
        
        model = tf.keras.Model(inputs=inputs, outputs=output)
        sgd = tf.keras.optimizers.SGD(
                learning_rate=learn_rate, clipnorm = 1 )
        
        #Compile model so that it can be trained
        model.compile(sgd,loss = 'logcosh')
        return model
