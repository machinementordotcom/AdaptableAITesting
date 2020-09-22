
import random
import numpy as np
from util.constants import * 
import csv
import ast
import omegaml as om

def createNets(conCurrentGame): # creates new network with randomized layers and nodes

    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    nets = []
    # Create every network
    for i in range(conCurrentGame):
        layers = []
        totalLayers = random.randint(2, maxlayers)
        totalNodes = np.random.randint(inputsNum,maxNodes,size=(1,totalLayers)).tolist()[0]
        # Create every layer
        for j in range(totalLayers):
            if j == 0:
                nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = np.random.rand(inputsNum,totalNodes[j-1],totalNodes[j]).tolist()[0]
            layers.append(Layer(nodeWeights))
        nets.append(Network(layers))
    print("\ncreateNets has run with nets=\n",str(nets))
    return nets

def createNet(specificLayers = None,specificNodes = None): # creates new net with option to specify number of layers and nodes
    
    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    # Create every network
    layers = []
    if specificLayers == None: totalLayers = random.randint(2, maxlayers)
    else: totalLayers = specificLayers 
    if specificNodes == None: totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
    else: totalNodes = specificNodes
    # Create every layer
    for j in range(totalLayers):
        if j == 0:
            nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
        else:
            nodeWeights = np.random.rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
        layers.append(Layer(nodeWeights))
    return Network(layers)

def countBits(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n

def toggleKthBit(n, k): 
    return (n ^ (1 << (k-1))) 


def createChildNets(parents,number): # no longer used

    newNets = []
    inputsNum = 17
    maxNodes = 100
    for i in range(number):
        parent1 = parents[random.randint(0, len(parents)-1)]
        parent2 = parents[random.randint(0, len(parents)-1)]
        if np.random.random_sample() > .5:totalLayers = len(parent1.layers)
        else:totalLayers = len(parent2.layers)
        totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
        layers = []
        for j in range(totalLayers -1):
            if j == 0:
                nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = np.random.rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
            layers.append(Layer(nodeWeights))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        newNets.append(Network(layers))
    return newNets

def mutateNets(nets):
    for index, current in enumerate(nets): 
        # Calculate the length 
        currentLayers = len(current.layers)
        # This calculates using 16 bits number 
        # If current layers length 44 then it gives 3
        # I think basically counts for that integer number
        num = countBits(currentLayers)
        # Starting loop for num
        for i in range(1, num):
            # random.uniform(0,1) gives random number between 0 and 1
            if random.uniform(0, 1) < (1/num):
                # it returns a integer with will use for creating number of layes
                currentLayers = toggleKthBit(currentLayers,i)
        # New layers created for that number of currentLayers
        nets[index] = createNet(specificLayers = currentLayers)
    return nets

def writeNetworks(nets):
    for i in range(len(nets)):
        with open("GENN/weights" + str(i) + ".csv",'w') as myfile:
            wr = csv.writer(myfile, quoting = csv.QUOTE_ALL) 
            for j in range(len(nets[i].layers)):
                wr.writerow(nets[i].layers[j].weights)

def readNets(nets):
    with open("GENN/masterWeights/weights.csv") as csvfile:
        reader = csv.reader(csvfile)
        layers = []
        for row in reader:
            temp = []
            for j in row:
                temp.append(ast.literal_eval(j))
            layers.append(Layer(temp))
        return [Network(layers)] * nets  
    
def aGENN_train(model_id, rounds):
    
    ## Train the model and save to omega
    name = model_id
    result = om.runtime.require('gpu').model(model_id).fit('x_train',
                                                           'y_train',
                                                           epochs=10,
                                                           batch_size=256)
    try:                                                       
        result.get()
    except:
        print("Training not run due to exception")

def create_training_set(rounds):

    ## Create dataset for training
    ## Step 1: Filter stream on model ID
    
    last_round = rounds - 1
    mdf = om.datasets.get('GENN_io_stream')
    flt = mdf['model_id'] == 'gen%dp0' % (last_round) 
    stream = mdf[flt]

    x = stream[["center_x",
              "center_y",
              "opponent_center_x",
              "opponent_center_y",
              "player_health",
              "opponent_health",
              "total_time",
              "player_shield",
              "opponent_shield",
              "opponent_hitbox",
              "curtime",
              "proj_1_x",          
              "proj_1_y",             
              "proj_2_x",             
              "proj_2_y",             
              "proj_3_x",             
              "proj_3_y"
             ]]

    y = stream[["predict1",
              "predict2",
              "predict3",
              "predict4",
              "predict5"]]
    
    ## Step 3: Scale values inputs and outputs

    x['center_x'] = x['center_x'] / 1000
    x['center_y'] = x['center_y'] / 1000
    x['opponent_center_x'] = x['opponent_center_x'] / 1000
    x['opponent_center_y'] = x['opponent_center_y'] / 1000
    x['player_health'] = x['player_health'] / 10000
    x['opponent_health'] = x['opponent_health'] / 10000
    x['total_time'] = x['total_time'] / 1000
    x['opponent_hitbox'] = x['opponent_hitbox'] / 10
    x['curtime'] = x['curtime'] / 5000
    x['proj_1_x'] = x['proj_1_x'] / 1000
    x['proj_1_y'] = x['proj_1_y'] / 1000
    x['proj_2_x'] = x['proj_2_x'] / 1000
    x['proj_2_y'] = x['proj_2_y'] / 1000
    x['proj_3_x'] = x['proj_3_x'] / 1000
    x['proj_3_y'] = x['proj_3_y'] / 1000

    y['predict1'] = y['predict1'] / 1000
    y['predict2'] = y['predict2'] / 1000
    
    x = np.asarray(x).reshape(-1,17)
    y = np.asarray(y).reshape(-1,5)
    
    om.datasets.put(x, 'x_train', append=False)
    om.datasets.put(y, 'y_train', append=False)
