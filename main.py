
#import ray
from gc import collect
from sys import argv
from numpy import asarray
from os import path, remove
from operator import add, itemgetter
from ctypes import c_int
from pandas import read_csv, DataFrame
import omegaml as om
from time import time
from datetime import datetime
from multiprocessing import Pool
#from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from AdaptableAITesting.sim import Game
from AdaptableAITesting.util.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
#from util.inputFunctions import * 
from AdaptableAITesting.GENN.GENNFunctions import *
import pickle

<<<<<<< HEAD
# Log messages to omega log (will not print to console)
=======
# Log messages to omega log
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
print = om.logger.info

# Models saves path as a constant
PATH_TO_NETWORK = '/app/pylib/user/AdaptableAITesting/models/'

om = om.setup(username='devconnect', 
          apikey='2d4b51a02d0a9c91507cca882ee5e5f5188808fc')

def runOneGame(a):

    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11])
    x.setup()
    val = True
    while val == True:
        val = x.update()
    return val    

def main(args):
    
    graphics = 'no'
    graphOutput = 'no'
    train = 'yes'
    evolutions = True
    
    
    ## Remove existing io_stream, if applicable
    try:
        if path.exists("io_stream.csv"):
            remove("io_stream.csv")
            print("io_stream.csv found and removed")
        else:
            print("io_stream.csv not found")
  
        if path.exists("data_log.csv"):
            remove("data_log.csv")
            print("data_log.csv found and removed")
        else:
            print("data_log.csv not found")
    
    except:
        pass
        
    if train == 'yes':
        # Game/Network will be played in the same time per generation
<<<<<<< HEAD
        conCurrentGame = 100
        print('%s concurrent games will be played' % conCurrentGame)
        # Total Generation 
        generations = 1003
=======
        conCurrentGame = 10
        print('%s concurrent games will be played' % conCurrentGame)
        # Total Generation 
        generations = 25
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
        simulation_player_1 = 'genn'
        simulation_player_2 = 'fsm'
        player_2_type = 'range'
        graphics = 'no'
        player_1_type = 'genn'
        graphOutput = 'no'
        games_per_network = 9
        train = 'yes'
        evolutions = True
       
        # Generation number to start. (Set to 0 if don't want to resume)
        start_generation = 999
        
        # Select resume generations
        gen_resume = 'yes'
        
        
        # Generation number to start. (Set to 0 if don't want to resume)
        start_generation = 25
        
        # Select resume generations
        gen_resume = 'yes'
        
        ## Select optimal number of pools
<<<<<<< HEAD
        pools = 60  # 2x per core
=======
        pools = 10  # 2x per core
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
        
        if gen_resume == 'no':
            try:            
                om.datasets.drop('GENN_data_TITAN')
                print('\nGENN game dataset dropped\n')
            except:
                print("\nGENN game dataset not found or unable to drop\n")
                pass

            try:
                om.datasets.drop('GENN_model_log_TITAN')
                print('\nGENN model_log dropped\n')
            except:
                print("\nGENN model log not found or unable to drop\n")
                pass
            
            try:
                om.datasets.drop('GENN_io_stream_TITAN')
                print('\nio stream dataset dropped\n')
            except:
                print("\nio stream dataset not found or unable to drop\n")
                pass
     
        print("All variables are set")
        
    else:
        conCurrentGame = get_int_choice('How many games would you like played at the same time (Recommended amount based on computer cores '+str(multiprocessing.cpu_count())+"):",1,1000)
        generations = get_int_choice('Enter the amount of rounds to be played: ',1,500)
        games_per_network = get_int_choice('Enter the amount of games to play per network: ',1,5000)
#        trendTracking = get_str_choice("Would you like to track trends",'yes','no')
        graphOutput = get_str_choice("Would you like to create graphical outputs?",'yes','no')
        simulation_player_1 = get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc','genn','agenn')
        if simulation_player_1.lower() == "freeplay":
            player_1_type = "human"
            graphics = 'yes'
        elif simulation_player_1.lower() == "fsm":
            player_1_type = get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
        elif simulation_player_1.lower() == "dc":
            player_1_type = get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random','train')
        elif simulation_player_1.lower() == "genn":
            player_1_type = "genn"
        elif simulation_player_1.lower() == "agenn":
            player_1_type = "agenn"
        simulation_player_2 = get_str_choice("What type of simulation do you want for player 2?",'fsm','dc','freeplay','genn')
        if simulation_player_2 == "freeplay":
            player_2_type = "human"
            graphics = 'yes'
        if simulation_player_2 == "fsm":
            player_2_type = get_str_choice("What type of player is player 2?",'short','mid','range','pq')
        elif simulation_player_2.lower() == "dc":
            player_2_type = get_str_choice("What type of dynamic controller is player 2 ?",'master','average','random')
        elif simulation_player_2.lower() == "genn":
            player_2_type = "genn"
        if graphics == 'no':
            graphics = get_str_choice('Run Graphically?: ','yes','no')

    if graphics == 'yes':
        window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,generations,player_1_type,player_2_type)
        window.setup()
        try:
            arcade.run()
        except:
            pass
    elif graphics == 'no':
        start = time()
        player1Wins = 0
        player2Wins = 0
        shortWins = 0
        midWins = 0
        rangeWins = 0
        draws = 0
        leftOverHealth = 0
        evolutionHealth = []
        bestNets = []  # NH - bestNets added

        for rounds in range(start_generation, generations):
            
            collect()

            print("Total rounds %d out of %d" % (rounds, generations))
            
            if evolutions == True and train == 'yes':
                
                if player_1_type in ['genn','agenn']: # NH - added agenn to ensure evolution will take place with agenn as with genn
                    
                    if rounds != 0 :
                        # Gen Resume is yes
                        if gen_resume == 'yes':
                            # Read Networks from pickle with the starting rounds (player_1)
                            filename = PATH_TO_NETWORK + "player1_" + str(rounds) + ".pickle"
                            with open(filename, 'rb') as handle:
                                player_1_nets = pickle.load(handle)
                            
                            
                            # We will require Player 2 nets in order to continue
                            print("Creating opponent nets")
                            player_2_nets = createNets(conCurrentGame)  
                            
                            # For next generations, we don't need to do it again, we will continue with other
                            gen_resume = 'no'
                        else:
                        
                            ## If this is not the first round, then record and analyze the previous round
                            # and evolve the networks

                            # Export the data log to omega storage - can be run at any time
                            try:
                                data = read_csv("data_log.csv")
<<<<<<< HEAD
                                om.datasets.put(data, 'GENN_data_TITAN_3', append=True)
=======
                                om.datasets.put(data, 'GENN_data_HUGE', append=True, n_jobs=2)
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
                                remove("data_log.csv")
                                print(data.shape)
                            except FileNotFoundError:
                                print("data_log.csv not found")

                            # Save data stream
                            if player_1_type == 'agenn':
                                stream = read_csv("io_stream.csv")
<<<<<<< HEAD
                                om.datasets.put(stream, 'GENN_io_stream_TITAN', append=True, n_jobs=2)
=======
                                om.datasets.put(stream, 'GENN_io_stream_HUGE', append=True, n_jobs=2)
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
                                remove("io_stream.csv")
                                print(stream.shape)

                            print('evolutionHealth: %s' % str(evolutionHealth))
<<<<<<< HEAD

                            # NH - changed from .2 to .1 to take only top 10%
                            bestTen = sorted(range(len(evolutionHealth)),
                                                key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.1):]
                            #print("bestTen:",str(bestTen))                       

                            ## Retrieve the best 10% as a list of networks
                            if len(bestTen) < 2:
                                bestTenNets = itemgetter(bestTen[0])(player_1_nets)
                                bestNets = asarray([bestTenNets]).tolist()
                            else:
                                bestTenNets = list(itemgetter(*bestTen)(player_1_nets)) 
                                bestNets = bestTenNets
                            #print("These are the top 10% of Nets from previous round (top 10%):",str(bestTen))

=======

                            # NH - changed from .2 to .1 to take only top 10%
                            bestTen = sorted(range(len(evolutionHealth)),
                                                key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.1):]
                            #print("bestTen:",str(bestTen))                       

                            # NH - added bestThirty for use in mutate and xover
                            # No longer needed                        
                            """bestThirty = sorted(range(len(evolutionHealth)),
                                                key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.3):] 
                            print("bestThirty:",str(bestThirty))
                            """

                            ## Retrieve the best 10 and 30% as a list of networks
                            if len(bestTen) < 2:
                                bestTenNets = itemgetter(bestTen[0])(player_1_nets)
                                bestNets = asarray([bestTenNets]).tolist()
                            else:
                                bestTenNets = list(itemgetter(*bestTen)(player_1_nets)) 
                                bestNets = bestTenNets
                            #print("These are the top 10% of Nets from previous round (top 10%):",str(bestTen))

>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
                            ## Log best nets - recursively save each to omega using list
                            rank = (len(bestTen))
                            for net in bestTen:
                                model_log = dict(
                                    round = [rounds - 1],
                                    player = [net],
                                    rank = [rank],
                                    fitness = [evolutionHealth[net]],
                                    timestamp = [datetime.now()]
                                )
                                dataFrame = DataFrame(model_log)
<<<<<<< HEAD
                                om.datasets.put(dataFrame, 'GENN_model_log_TITAN', append=True)
                                rank -= 1

=======
                                om.datasets.put(dataFrame, 'GENN_model_log_HUGE', append=True)
                                rank -= 1

                            # NH - changed 'newNets' to 'bestThirtyNets'
                            ## no longer needed
                            """bestThirtyNets = list(itemgetter(*bestThirty)(player_1_nets)) 
                            print("These are the top 30% of Nets from previous round (top 10%):",str(bestThirty))
                            """

>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
                            ## Create training set from top players of previous round
                            if player_1_type == 'agenn':
                                create_training_set(rounds, bestTen)
                                print("Training set created from round %d top players" % (rounds - 1))

                            if rounds % 11 == 0: # Every 11th generation the top players from previous 10 generations are tested
                                start_gen = rounds - 10
                                player_1_nets = []
                                count_top = int(conCurrentGame * 0.1)

                                for gen in range(start_gen, rounds):
                                    filename = PATH_TO_NETWORK + "player1_" + str(gen) + ".pickle"
                                    with open(filename, 'rb') as handle:
                                        temp_nets = pickle.load(handle)
                                        temp_nets = temp_nets[:count_top]
<<<<<<< HEAD

                                        for temp_net in temp_nets:
                                            player_1_nets.append(temp_net)

                                # Got the list, now send it to where it will initialize and play the games
                                print("These are the players teed up for 11th gen test round: %s" % player_1_nets)

                            else:  ## Perform evolution
                                #print(bestNets[0])
                                #print(bestNets[0].layers)
                                #print(bestNets[0].layers[0].weights)
    #                            try: ## If nets are listed in network form, this will work
                                xoverNets = crossoverNets(bestNets+bestNets+bestNets) # top 10% is used to create 30% of nets 
                                """except:  ## After an 11th gen, nets will be listed in omega format, must convert
                                    last_round = rounds - 1
                                    bestNets = []
                                    for i in bestTen:
                                        net = om.models.get('gen%dp%d' % (last_round, i))
                                        bestNets.append(net)
                                    xoverNets = crossoverNets(bestNets+bestNets+bestNets)
                                    """
                                #print("These are xoverNets (30%):",str(xoverNets))

                                # Bit Flip mutation
                                mutatedNets = mutateNets(bestNets+bestNets+bestNets) 
                                #print("And these are the nets mutated from best nets (30%):",str(mutatedNets))

=======

                                        for temp_net in temp_nets:
                                            player_1_nets.append(temp_net)


                                """
                                player_1_nets = []
                                count = int(conCurrentGame * 0.1)
                                start_gen = rounds - 10

                                for gen in range(start_gen,rounds):
                                    for model in range(count):
                                        filename = '/app/pylib/user/AdaptableAITesting/models/gen%dp%d.pickle' % (gen, model)
                                        with open(filename, 'rb') as handle:
                                            net = pickle.load(handle)
                                            player_1_nets.append(net)
                                """   
                                # Got the list, now send it to where it will initialize and play the games
                                print("These are the players teed up for 11th gen test round: %s" % player_1_nets)

                            else:  ## Perform evolution
                                #print(bestNets[0])
                                #print(bestNets[0].layers)
                                #print(bestNets[0].layers[0].weights)
    #                            try: ## If nets are listed in network form, this will work
                                xoverNets = crossoverNets(bestNets+bestNets+bestNets) # top 10% is used to create 30% of nets 
                                """except:  ## After an 11th gen, nets will be listed in omega format, must convert
                                    last_round = rounds - 1
                                    bestNets = []
                                    for i in bestTen:
                                        net = om.models.get('gen%dp%d' % (last_round, i))
                                        bestNets.append(net)
                                    xoverNets = crossoverNets(bestNets+bestNets+bestNets)
                                    """
                                #print("These are xoverNets (30%):",str(xoverNets))

                                # Bit Flip mutation
                                mutatedNets = mutateNets(bestNets+bestNets+bestNets) 
                                #print("And these are the nets mutated from best nets (30%):",str(mutatedNets))

>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
                                # The balance of nets will be created randomly
                                randomNets = createNets(int(conCurrentGame)-len(bestTen)-len(xoverNets)-len(mutatedNets)) 
                                #print("These are the new random nets (30%):",str(randomNets))

                                # NH - pasting the network lists together
                                player_1_nets = bestNets + randomNets + xoverNets + mutatedNets  
                                #print("These are player_1_nets for next round:",player_1_nets)

                            evolutionHealth = []
                            #print("evolutionHealth is reset to",evolutionHealth)
                        
                    else:
                        
                        ## If this is the first round, then create all the nets from scratch
                        
                        print("Creating player 1 nets")
                        player_1_nets = createNets(conCurrentGame)
                        print("Creating opponent nets")
                        player_2_nets = createNets(conCurrentGame)        
                        
                if player_2_type == 'genn':
                    if rounds != 0:
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createNets(conCurrentGame - len(newNets)) # NH - replaced createChildNets with createNets
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets)
            
<<<<<<< HEAD
                      
=======
           
#            print("Creating",pools,"process or thread pools")
#            ex = ProcessPoolExecutor(max_workers=pools)  
            
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
            ex = Pool(pools,
                      maxtasksperchild=1
                     ) 
            
            #r = [runOneGame.remote(i) for i in [ x + [i - 1]  \
            result = ex.map(runOneGame,[ x + [i - 1]  \
                                       for i,x in enumerate([x for x in \
                                                             [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,
                                                             games_per_network,player_1_type,player_2_type,
                                                             conCurrentGame,rounds,player_1_nets,
                                                             player_2_nets,bestNets]]*conCurrentGame],1)])

            ex.close()
            ex.join()
            
            print("Round result set: %s" % result)

            evolutionHealth = [float(i) for i in result]
                  
            player1Wins += sum(int(i) > 0 for i in [int(i) for i in result]) 
            player2Wins += sum(int(i) < 0 for i in [int(i) for i in result])

            draws += sum(int(i) == 0 for i in [int(i) for i in result])  
            leftOverHealth += sum([float(i) for i in result])
            
            # Create File Path for Player1 and Player2
            filename_player1 = PATH_TO_NETWORK + "player1_" + str(rounds) + ".pickle"
            filename_player2 = PATH_TO_NETWORK + "player2_" + str(rounds) + ".pickle"
            
            # Dump Player1 nets
            with open(filename_player1, 'wb') as handle:
                pickle.dump(player_1_nets, handle)
<<<<<<< HEAD

=======
            """
            # Dump Player2 nets
            with open(filename_player2, 'wb') as handle:
                pickle.dump(player_2_nets, handle)
            

            """
>>>>>>> 1f42928bb4a28bfb5e631263666dc5c6964cdf73
        
        #print("player 1 (" + player_1_type + "):",player1Wins)
        #print("player 2 (" + player_2_type + "):",player2Wins)

        #print("Draws: ",draws)
        #print("Average Health Difference: ",round(abs(leftOverHealth) / (conCurrentGame * generations),4))
        #print("Total Time: ",round(time() - start,4))

if __name__ == "__main__":
    main(argv)

