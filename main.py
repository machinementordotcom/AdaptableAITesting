
import sys
import os
#sys.stdout = open(os.devnull, 'w') # this cancels all output and prevents writing to the console
from MyGame import *
import arcade
from sim import *
from util.constants import * 
from util.inputFunctions import * 
from GENN.GENNFunctions import * 
import time
import multiprocessing
# import concurrent.futures
from operator import add 
from ctypes import c_int
from operator import itemgetter 
import pandas as pd
import json
import re 
import matplotlib.ticker as ticker

#sys.stdout = sys.__stdout__

def runOneGame(a):

    max_moves = 5000
    print("runOneGame commencing")
    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13])
    print("setting up players")
    x.setup()
    val = True
    print("Game Play Started...")
    while val == True:
#        print("Playing...")
        val = x.update(max_moves)
    return val    
    print('runOneGame OVER') 

"""
    while True:
        if type(val) is list:
            if val[0] == True:
                val = x.update(move, val[1])
#                move += 1
#                if move % 250  == 0:  ## updates are coordinated with sim.py health updates
                    #print("Move", str(move))
#                    None
        else:
            print("Game over")
            return val

def createGraphs(playerNum):
    with open('player' + str(playerNum) + 'Trends.txt') as f:
        z = str(f.readline()).replace("}","").split("{")
    p = []
    for elm in z[1:]:
        use = elm.split(",")
        temp = [ re.sub("\D", "", x) for x  in use ] 
        p.append(temp)
    x = pd.DataFrame(p,columns = ['arrow','fire','knife','towardsOpponent','awayOpponent','movementChanges','biggestTrend'])
    fig, ax = plt.subplots()

    plt.plot(range(len(x)),x['arrow'].astype(float))    
    plt.plot(range(len(x)),x['fire'].astype(float))    
    plt.plot(range(len(x)),x['knife'].astype(float)) 
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))   


    plt.ylabel("Shot Frequency")
    plt.xlabel("Time segment")
    plt.title("Shooting trends per segment for player " + str(playerNum))
    # plt.yticks(range(len(x)))
    plt.legend(['Arrow', 'Fire', 'Knife'], loc='upper left')

    plt.savefig("player" + str(playerNum) + "ShootingTrends")
"""

def main(args):
    """ Main method """
    """
    #Remove the Log File first otherwise it for avoiding merge log data for every run
    if os.path.exists('player_1_log.csv'):
        os.remove('player_1_log.csv')
    else:
        pass

    if os.path.exists('player_2_log.csv'):
        os.remove('player_2_log.csv')
    else:
        pass
        """
    graphics = 'no'
    graphOutput = 'no'
    train = 'yes'
    trendTracking = 'no'
    evolutions = True

    if train == 'yes':
        # Game/Network will be played in the same time per generation
        conCurrentGame = 20  # Must be at least 20 for topTen to function (min 2 nets)
        # Total Generation 
        generations = 111
        simulation_player_1 = 'genn'
        simulation_player_2 = 'fsm'
        player_2_type = 'range'
        graphics = 'no'
        player_1_type = 'genn'
        trendTracking = 'no'
        graphOutput = 'no'
        games_per_network = 9
        train = 'yes'
        
        ## Select optimal number of pools
        pools = os.cpu_count() * 4
        
        print("All variables are set")
    else:
        conCurrentGame = get_int_choice('How many games would you like played at the same time (Recommended amount based on computer cores '+str(multiprocessing.cpu_count())+"):",1,1000)
        generations = get_int_choice('Enter the amount of rounds to be played: ',1,500)
        games_per_network = get_int_choice('Enter the amount of games to play per network: ',1,5000)
        trendTracking = get_str_choice("Would you like to track trends",'yes','no')
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

    if (player_1_type == 'genn' or player_1_type == 'agenn') and train == 'yes':
        evolutions = True
        print("Creating nets",player_1_type,train)
        player_1_nets = createNets(conCurrentGame)
    elif (player_1_type == 'genn' or player_1_type == 'agenn') and train == 'no':
        print("Creating nets",player_1_type,train)
        player_1_nets = readNets(conCurrentGame)
    else: player_1_nets = None
        
    if (player_2_type == 'genn' or player_2_type == 'agenn') and train == 'yes':
        evolutions = True
        print("Creating nets",player_1_type,train)
        player_2_nets = createNets(conCurrentGame)
    elif (player_2_type == 'genn' or player_2_type == 'agenn') and train == 'no':
        print("Creating nets",player_1_type,train)
        player_2_nets = readNets(conCurrentGame)
    else: player_2_nets = None
        
    if graphics == 'yes':
        window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,generations,player_1_type,player_2_type)
        window.setup()
        try:
            arcade.run()
        except:
            pass
    elif graphics == 'no':
        start = time.time()
        player1Wins = 0
        player2Wins = 0
        shortWins = 0
        midWins = 0
        rangeWins = 0
        draws = 0
        leftOverHealth = 0
        evolutionHealth = []

        for rounds in range(generations):

            print("Total rounds %d out of %d" % (rounds, generations))
            print("Player1 Nets length:", str(len(player_1_nets)))
            print("at beginning of round:\n",player_1_nets)
#            time.sleep(30)
            
            if evolutions == True and train == 'yes':
                
                if player_1_type in ['genn','agenn']: # NH - added agenn to ensure evolution will take place with agenn as with genn
                    
                    if rounds != 0: # NH - mutation should happen at the beginning of every generation after 1
                        
                        print("evolutionHealth:",str(evolutionHealth))
                        
                        # NH - changed from .2 to .1 to take only top 10%
                        bestTen = sorted(range(len(evolutionHealth)),
                                            key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.1):]
                        print("bestTen:",str(bestTen))                       
                    
                        # NH - added bestThirty for use in mutate and xover
                        bestThirty = sorted(range(len(evolutionHealth)),
                                            key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.3):] 
                        print("bestThirty:",str(bestThirty))
                        
                        evolutionHealth = []
                        print("evolutionHealth is reset to",evolutionHealth)
                        #time.sleep(10)
                        
                        ## Retrieve the best 10 and 30% as a list of networks
                        bestTenNets = list(itemgetter(*bestTen)(player_1_nets)) 
                        print("These are the top 10% of Nets from previous round (top 10%):",str(bestTen))
                        
                        # NH - changed 'newNets' to 'bestThirtyNets'
                        bestThirtyNets = list(itemgetter(*bestThirty)(player_1_nets)) 
                        print("These are the top 30% of Nets from previous round (top 10%):",str(bestThirty))
                        
                        ## NH - this will be replaced with crossover code when defined
                        xoverNets = createNets(int(conCurrentGame * 0.3)) 
                        print("These are xoverNets (30%):",str(player_1_nets))
                        
                        # passing in an additional variable
                        mutatedNets = mutateNets(bestThirtyNets) 
                        print("And these are the nets mutated from best nets (30%):",str(mutatedNets))
                        
                        # NH - replaced createChildNets with createNets
                        randomNets = createNets(int(conCurrentGame)-len(bestTenNets)+len(xoverNets)+len(mutatedNets)) 
                        print("These are the new random nets (30%):",str(randomNets))
                        
                        # NH - pasting the network lists together
                        player_1_nets = bestTenNets + randomNets + xoverNets + mutatedNets  
                        print("These are player_1_nets for next round:",player_1_nets)
                        #time.sleep(30)
                        
                if player_2_type == 'genn':
                    #if rounds % 9 == 0 and rounds != 0:
                    if rounds != 0:
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createNets(conCurrentGame - len(newNets)) # NH - replaced createChildNets with createNets
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets)
            
#            pools = max(conCurrentGame,os.cpu_count()*4) # NH - need to create enough processes or threads to keep CPU busy
            
            print("Creating",pools,"process or thread pools")
#            ex = concurrent.futures.ProcessPoolExecutor(max_workers=pools)  
            ex = multiprocessing.Pool(pools) 

            result = ex.map(runOneGame,[ x + [i - 1]  \
                                       for i,x in enumerate([x for x in \
                                                             [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,
                                                             games_per_network,player_1_type,player_2_type,
                                                             conCurrentGame,rounds,player_1_nets,
                                                             player_2_nets,trendTracking,
                                                             simulation_player_1,simulation_player_2]] *conCurrentGame  ],1) ]) #chunksize
            
            print("Round result set:",result)
            

            evolutionHealth = [float(i) for i in result]
                  
            player1Wins += sum(int(i) > 0 for i in [int(i) for i in result]) 
            player2Wins += sum(int(i) < 0 for i in [int(i) for i in result])

            draws += sum(int(i) == 0 for i in [int(i) for i in result])  
            leftOverHealth += sum([float(i) for i in result])

            ex.close()  #NH - not needed if using futures.concurrent for multiprocessing
            ex.join()

        if player_1_type is 'genn' or player_1_type is 'agenn':
            writeNetworks(player_1_nets)
        if player_2_type is 'genn' or player_2_type is 'agenn':
            writeNetworks(player_2_nets)
        print("player 1 (" + player_1_type + "):",player1Wins)
        print("player 2 (" + player_2_type + "):",player2Wins)
        """
        if train == 'yes':
            print("\t Short Wins: ",shortWins)
            print("\t mid Wins: ",midWins)
            print("\t range Wins: ",rangeWins)
        """
        print("Draws: ",draws)
        print("Average Health Difference: ",round(abs(leftOverHealth) / (conCurrentGame * generations),4))
        print("Total Time: ",round(time.time() - start,4))
"""        
    if graphOutput =='yes':
        if player_1_type not in ['short','mid','range']:
            createGraphs(1)
        if player_2_type not in ['short','mid','range']:
            createGraphs(2)
"""

if __name__ == "__main__":
    main(sys.argv)

