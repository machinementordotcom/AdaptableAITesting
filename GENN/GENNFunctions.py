
from random import randint, uniform
from numpy.random import rand, randint
from numpy import asarray
from AdaptableAITesting.util.constants import Layer, Network 
import omegaml as om


def createNets(conCurrentGame): # creates new network with randomized layers and nodes

    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    nets = []
    # Create every network
    for i in range(conCurrentGame):
        layers = []
        totalLayers = randint(2, maxlayers)
        totalNodes = randint(inputsNum,maxNodes,size=(1,totalLayers)).tolist()[0]
        # Create every layer
        for j in range(totalLayers):
            if j == 0:
                nodeWeights = rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = rand(inputsNum,totalNodes[j-1],totalNodes[j]).tolist()[0]
            layers.append(Layer(nodeWeights))
        nets.append(Network(layers))
#    print("\ncreateNets has run with nets=\n",str(nets))
    return nets

def createNet(specificLayers = None,specificNodes = None): # creates new net with option to specify number of layers and nodes
    
    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    # Create every network
    layers = []
    if specificLayers == None: totalLayers = randint(2, maxlayers)
    else: totalLayers = specificLayers 
    if specificNodes == None: totalNodes = randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
    else: totalNodes = specificNodes
    # Create every layer
    for j in range(totalLayers):
        if j == 0:
            nodeWeights = rand(1,inputsNum,totalNodes[0]).tolist()[0]
        else:
            nodeWeights = rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
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

def swap(i, j):
    return j, i

def crossoverNets(nets):
    """
    parameters:
        nets:
            Takes list of nets. Pass the 30% of the nets to it
    description:
        Do Uniform Crossover weights between the nets
    returns:
        nets with Crossover
    """
    for net in nets:
        # Total Loop, length(nets)x length(layers, per net)
        for layer in net.layers:
            # Total Loop, length(nets) x length(layers, per net)
            # x length(2D weights, per layer)
            for _ in layer.weights:
                # Set Initial Indexes(Select weight for exchange, first swap value)
                # Take a random index from nets
                try:
                    initial_net_index = randint(0,len(nets)-1)
                except ValueError:
                    initial_net_index = 0
                try:
                # Take a random index from layers on that net
                    initial_layer_index = randint(0, len(nets[initial_net_index].layers)-1)
                except ValueError:
                    initial_layer_index = 0
                try:
                    # Take a random index for Weights 2D from the layer (list)
                    initial_weight2D_index = randint(0, len(nets[initial_net_index]\
                                                                   .layers[initial_layer_index]\
                                                                   .weights)-1)
                except ValueError:
                    initial_weight2D_index = 0
                try:
                    # Take a random index for Weights 1D from the Weights 1D (float)
                    initial_weight1D_index = randint(0, len(nets[initial_net_index]\
                                                                  .layers[initial_layer_index]\
                                                                  .weights[initial_weight2D_index])-1)
                except ValueError:
                    initial_weight1D_index=0
                # Set Final Indexes(Replace weight for exchange, second swap value)
                try:
                    # Take a random index from nets
                    final_net_index = randint(0,len(nets)-1)
                except ValueError:
                    final_net_index = 0
                try:
                    # Take a random index from layers on that net
                    final_layer_index = randint(0, len(nets[final_net_index].layers)-1)
                except ValueError:
                    final_layer_index = 0
                try:
                    # Take a random index for Weights 2D from the layer (list)
                    final_weight2D_index = randint(0, len(nets[final_net_index]\
                                                                 .layers[final_layer_index].weights)-1)
                except ValueError:
                    final_weight2D_index = 0
                try:
                    # Take a random index for Weights 1D from the Weights 1D (float)
                    final_weight1D_index = randint(0, len(nets[final_net_index]\
                                                                .layers[final_layer_index]\
                                                                .weights[final_weight2D_index])-1)
                except ValueError:
                    final_weight1D_index = 0
                # Now swap values
                # Simply it's like this a,b = b,a but done using swap function
                nets[initial_net_index] \
                .layers[initial_layer_index] \
                .weights[initial_weight2D_index][initial_weight1D_index] \
                , nets[final_net_index ] \
                .layers[final_layer_index] \
                .weights[final_weight2D_index][final_weight1D_index] = swap(
                        nets[initial_net_index].layers[initial_layer_index]\
                        .weights[initial_weight2D_index][initial_weight1D_index],
                        nets[final_net_index ].layers[final_layer_index]\
                        .weights[final_weight2D_index][final_weight1D_index]
                        )
    return nets


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
            # uniform(0,1) gives random number between 0 and 1
            if uniform(0, 1) < (1/num):
                # it returns a integer with will use for creating number of layes
                currentLayers = toggleKthBit(currentLayers,i)
        # New layers created for that number of currentLayers
        nets[index] = createNet(specificLayers = currentLayers)
    return nets

"""def writeNetworks(nets):
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
        """

def aGENN_train(model_id, rounds):
    
    ## Train the model and save to omega
    from omegaml import runtime
    name = model_id
    bs = 32
    e = 2
    spe = 32
    shuf = True
    vs = 0.2
    
    print("Preparing to train model", name)

    try: # Try training on GPU for best performance                                               
        result = runtime.require('gpu').model(name).fit('x_train',
                                                       'y_train',
                                                        batch_size=bs, 
                                                        epochs=e,
                                                        #validation_split=vs,
                                                        steps_per_epoch=spe,
                                                        shuffle=shuf)
        result.get()
        model = om.models.get(name)
        print("Training on GPU successful for",model_id)
    except:  # Train on local CPU if GPU is busy
        
        model = om.models.get(name)
        model.fit('x_train',
                   'y_train',
                    batch_size=bs, 
                    epochs=e,
                    #validation_split=vs,
                    steps_per_epoch=spe,
                    shuffle=shuf)
            
        print("Training run locally for",model_id)
    
    return model
        
        
def create_training_set(rounds, bestTen):
    
    ## Create dataset for training
    ## Step 1: Take the top 3 (or less) models from best 10%
    from numpy import asarray
    last_round = (rounds - 1)
    bestModels = []
    print(len(bestTen))
    mdf = om.datasets.getl('GENN_io_stream')

    if len(bestTen) >= 2:
        for i in asarray(bestTen):
            model = str("gen%dp%s" % (last_round, i))
            bestModels.append(model)
        print(bestModels)
        flt = (mdf['model_id'] == bestModels[0]) | (mdf['model_id'] == bestModels[1])

    else:
        model_name = str("gen%dp%s" % (last_round, bestTen[0]))
        bestModels.append(model_name)
        print(bestModels)
        flt = (mdf['model_id'] == bestModels[0])
        
    ## Get the dataset and filter it on the top model names
    stream = mdf[flt].value

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
              "proj_3_y"]]

    y = stream[["predict1",
              "predict2",
              "predict3",
              "predict4",
              "predict5"]]
    
    ## Step 3: Scale values inputs and outputs
    
    x['center_x'] = x.loc[:, 'center_x'] / 1000
    x['center_y'] = x.loc[:, 'center_y'] / 1000
    x['opponent_center_x'] = x.loc[:, 'opponent_center_x'] / 1000
    x['opponent_center_y'] = x.loc[:, 'opponent_center_y'] / 1000
    x['player_health'] = x.loc[:, 'player_health'] / 10000
    x['opponent_health'] = x.loc[:, 'opponent_health'] / 10000
    x['total_time'] = x.loc[:, 'total_time'] / 1000
    x['opponent_hitbox'] = x.loc[:, 'opponent_hitbox'] / 10
    x['curtime'] = x.loc[:, 'curtime'] / 5000
    x['proj_1_x'] = x.loc[:, 'proj_1_x'] / 1000
    x['proj_1_y'] = x.loc[:, 'proj_1_y'] / 1000
    x['proj_2_x'] = x.loc[:, 'proj_2_x'] / 1000
    x['proj_2_y'] = x.loc[:, 'proj_2_y'] / 1000
    x['proj_3_x'] = x.loc[:, 'proj_3_x'] / 1000
    x['proj_3_y'] = x.loc[:, 'proj_3_y'] / 1000

    y['predict1'] = y.loc[:, 'predict1'] / 1000
    y['predict2'] = y.loc[:, 'predict2'] / 1000
    
    x = asarray(x).reshape(-1,17)
    y = asarray(y).reshape(-1,5)
    
    om.datasets.put(x, 'x_train', append=False)
    om.datasets.put(y, 'y_train', append=False)
    
"""def generateSupArray(conCurrentGame, max_moves): # creates new array with aGENN training values
    
    # Declare arrays of possible variables for training
    fitnessLevel = [-1000,1000] # range of fitness level used as trigger for in-game training
    frequency = [0.01, 0.25] # range of how how often fitness is checked in-game, function of max_moves
    epochs = [1,10] # range of possible epochs allowed in a single training
    batchSize = [4, 8, 16, 32, 64, 128, 256] # sample sizes 
    stepsPerEpoch = [] # function of number of epochs and set size
    setSize = [0.1, 0.25, 0.5, 0.75, 1] # portion of training set used
    shuffle = [True, False]
    supArray = [] # resulting array
    
    # Create supervisor array with randomized values
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
        supArray.append(Network(layers))
    print("\nsupervisor array has been created",str(nets))
    return supArray
    """
