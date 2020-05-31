import sys
import os
sys.stdout = open(os.devnull, 'w')
from MyGame import *
import arcade
from sim import *

from util import neural_net

from util import inputFunctions

from GENN.GENNFunctions import *
import time
import multiprocessing
from operator import add
from operator import itemgetter 
import pandas as pd
import re 
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from util.constants import SCREEN_WIDTH, \
    SCREEN_HEIGHT, \
    SCREEN_TITLE

sys.stdout = sys.__stdout__

def runOneGame(a):
    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11])
    x.setup()
    val = True
    while val:
        val = x.update()
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

def main(args):
    """ Main method """

    graphics = 'no'
    graphOutput = 'no'
    train = 'no'
    trendTracking = 'no'
    evolutions = False
    spacer()

    if train == 'yes':

        conCurrentGame = 1
        iterations = 1
        simulation_player_1 = 'agenn'
        simulation_player_2 = 'genn'
        player_2_type = 'genn'
        graphics = 'no'
        player_1_type = 'agenn'
        trendTracking = 'yes'
        graphOutput = 'no'
        report_interval = 1
        debug = True   
    
        
        print('Inititating training with %s concurrent games between %s and %s player types'%(conCurrentGame,simulation_player_1,simulation_player_2))
    else:
        conCurrentGame = inputFunctions.get_int_choice('How many games would you like played at the same time (Recommended amount based on computer cores '+str(multiprocessing.cpu_count())+"):",1,1000)
        iterations = inputFunctions.get_int_choice('Enter the amount of generations to be played: ',1,5000)
        trendTracking = inputFunctions.get_str_choice("Would you like to track trends",'yes','no')
        graphOutput = inputFunctions.get_str_choice("Would you like to create graphical outputs?",'yes','no')
        simulation_player_1 = inputFunctions.get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc','genn','agenn')
        if simulation_player_1.lower() == "freeplay":
            player_1_type = "human"
            graphics = 'yes'
        elif simulation_player_1.lower() == "fsm":
            player_1_type = inputFunctions.get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
        elif simulation_player_1.lower() == "dc":
            player_1_type = inputFunctions.get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random','train')
        elif simulation_player_1.lower() == "genn":
            player_1_type = "genn"
        elif simulation_player_1.lower() == "agenn":
            player_1_type = "agenn"
        simulation_player_2 = inputFunctions.get_str_choice("What type of simulation do you want for player 2?",'fsm','dc','freeplay','genn','agenn')
        if simulation_player_2 == "freeplay":
            player_2_type = "human"
            graphics = 'yes'
        if simulation_player_2 == "fsm":
            player_2_type = inputFunctions.get_str_choice("What type of player is player 2?",'short','mid','range','pq')
        elif simulation_player_2.lower() == "dc":
            player_2_type = inputFunctions.get_str_choice("What type of dynamic controller is player 2 ?",'master','average','random')
        elif simulation_player_2.lower() == "genn":
            player_2_type = "genn"
        elif simulation_player_2.lower() == "agenn":
            player_2_type = "agenn"
        if graphics == 'no':
            graphics = inputFunctions.get_str_choice('Run Graphically?: ','yes','no')
    
    if player_1_type == 'genn' and train == 'yes':
        evolutions = True
        player_1_nets = createNets(conCurrentGame)
    elif player_1_type == 'agenn' and train == 'yes':
        evolutions = True
        player_1_nets = createNets(conCurrentGame, adaptive = True)
    elif player_1_type == 'genn' and train == 'no':
        player_1_nets = readNets(conCurrentGame)
    elif player_1_type == 'agenn' and train == 'no':
        player_1_nets = readNets(conCurrentGame,adaptive = True)
    else: player_1_nets = None
    
    if player_2_type == 'genn' and train == 'yes':
        evolutions = True
        player_2_nets = createNets(conCurrentGame)
    elif player_2_type == 'agenn' and train == 'yes':
        evolutions = True
        player_2_nets = createNets(conCurrentGame, adaptive = True)
    elif player_2_type == 'genn' and train == 'no':
        player_2_nets = readNets(conCurrentGame)
    elif player_2_type == 'agenn' and train == 'no':
        player_2_nets = readNets(conCurrentGame,adaptive = True)
    else: player_2_nets = None
    
    if graphics == 'yes':
        window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,iterations,player_1_type,player_2_type,
                        player_1_nets, player_2_nets)
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
        for game in range(iterations):
            inputFunctions.spacer()
            print("Total iterations %d out of %d" % (game + 1, iterations) )
            if evolutions == True and train == 'yes':
                if game % report_interval== 0 and game != 0:
                    if player_1_type == 'genn':
                        print(evolutionHealth)
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_1_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_1_nets = newNets + temp
                        player_1_nets = mutateNets(player_1_nets, adaptive = False)
                    if player_1_type == 'agenn':
                        print(evolutionHealth)
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_1_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets), adaptive = True)
                        player_1_nets = newNets + temp
                        player_1_nets = mutateNets(player_1_nets, adaptive = True)
                    if player_2_type == 'genn':
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets, adaptive =False)
                    if player_2_type == 'agenn':
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets), adaptive = True)
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets, adaptive =True)
            p = multiprocessing.Pool(multiprocessing.cpu_count())
                # map will always return the results in order, if order is not important in the future use pool.imap_unordered()
            if train == 'yes':
                if game % 9 < 3: player_2_type == 'short'
                elif game % 9 < 6: player_2_type == 'mid'
                else: player_2_type == 'range'
            clock = time.time()
            result = p.map(runOneGame,[ x + [i - 1]  for i,x in enumerate([ x for x in [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,1,player_1_type,player_2_type,conCurrentGame,game,player_1_nets,player_2_nets, trendTracking]] *conCurrentGame  ],1) ])
            
            print('Game simulation finished in %s seconds'%(time.time()-clock))
            if game == 0 or game % 3 == 0: evolutionHealth = [float(i) for i in result]
            else: evolutionHealth = list(map(add, [float(i) for i in result], evolutionHealth)) 
            player1Wins += sum(int(i) > 0 for i in [int(i) for i in result]) 
            player2Wins += sum(int(i) < 0 for i in [int(i) for i in result])
            print('player 1 wins: %s  /n  player 2 wins: %s/n'%(player1Wins,player2Wins))
            if train == 'yes':
                if game % 9 < 3: shortWins += sum(int(i) < 0 for i in [int(i) for i in result])
                elif game % 9 < 6: midWins += sum(int(i) < 0 for i in [int(i) for i in result])
                else: rangeWins += sum(int(i) < 0 for i in [int(i) for i in result])
            draws += sum(int(i) == 0 for i in [int(i) for i in result])  
            leftOverHealth += sum([float(i) for i in result])
            p.close()
            p.join()
        
        clock = time.time()
        if player_1_type == 'genn' or player_1_type == 'agenn':
            writeNetworks(player_1_nets)
        if player_2_type == 'genn' or player_2_type == 'agenn':
            writeNetworks(player_2_nets)
        
        print('Network weights written in %s seconds'%(time.timer()-clock))
        print("player 1 (" + player_1_type + "):",player1Wins)
        print("player 2 (" + player_2_type + "):",player2Wins)
        if train == 'yes':
            print("\t Short Wins: ",shortWins)
            print("\t mid Wins: ",midWins)
            print("\t range Wins: ",rangeWins)
        print("Draws: ",draws)
        print("Average Health Difference: ",round(abs(leftOverHealth) / (conCurrentGame * iterations),4))
        print("Total Time: ",round(time.time() - start,4))
    if graphOutput =='yes':
        if player_1_type not in ['short','mid','range']:
            createGraphs(1)
        if player_2_type not in ['short','mid','range']:
            createGraphs(2)
        
if __name__ == "__main__":
    main(sys.argv)

