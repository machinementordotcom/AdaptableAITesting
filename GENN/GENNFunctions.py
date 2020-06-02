import random 
import numpy as np
from util import neural_net
from util import constants
import csv
import ast

def createNets(conCurrentGame, adaptive = False):
    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    nets = []
    # Create every network
    for i in range(conCurrentGame):
        layers = []
        totalLayers = random.randint(2, maxlayers)
        totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
        # Create every layer
        for j in range(totalLayers):
            if j == 0:
                nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = np.random.rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
            layers.append(constants.Layer(nodeWeights))
        layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        if adaptive == True: #JTW modified to optionally allow creating adaptive network which adjusts its own weights
            nets.append(neural_net.AdaptiveNetwork(layers))
        else:
            nets.append(neural_net.Network(layers))
    return nets

def createNet(specificLayers = None,specificNodes = None, adaptive = False):
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
        layers.append(constants.Layer(nodeWeights))
    layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
    layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
    layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
    layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
    layers.append(constants.Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
    if adaptive == True:  #JTW modified to optionally allow creating adaptive network which adjusts its own weights
        return neural_net.neural_net.AdaptiveNetwork(layers)
    else:
        return neural_net.Network(layers)

def createChildNets(parents,number, adaptive = False):
    return createNets(number)
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
        if adaptive:
            newNets.append(AdaptiveNetwork(layers))
        else:
            newNets.append(Network(layers))
    return newNets

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

def mutateNets(nets, adaptive =False):
    newNetsIndex = np.random.randint(0,len(nets),int(len(nets)*.1))
    for i in newNetsIndex:
        current = nets[i]
        currentLayers = len(current.layers)
        num = countBits(currentLayers)
        for i in range(num):
            if random.uniform(0, 1) < (1/num):
                currentLayers = toggleKthBit(currentLayers,i)
        nets[i] = createNet(specificLayers = currentLayers, adaptive=adaptive)
    return nets

def writeNetworks(nets,adaptive = False):
    if adaptive:
        filename = "Genn/weights"
    else:
        filename = "Genn/adaptiveWeights"
    for i in range(len(nets)):
        with open(filename + str(i) + ".csv",'w') as myfile:
            wr = csv.writer(myfile, quoting = csv.QUOTE_ALL) 
            for j in range(len(nets[i].layers)):
                wr.writerow(nets[i].layers[j].weights)

def readNets(nets, adaptive = False):
    if adaptive:
        filename = "Genn/masterWeightsAdaptive/weights.csv"
    else:
        filename = "Genn/masterWeights/weights.csv"
        
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        layers = []
        for row in reader:
            temp = []
            for j in row:
                temp.append(ast.literal_eval(j))
            layers.append(constants.Layer(temp))
        if adaptive:
            return[neural_net.AdaptiveNetwork(layers)] * nets
        else:
            return [neural_net.Network(layers)] * nets


