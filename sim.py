
import numpy as np
import arcade
import os
import math
import random
import sys
import time

from DynamicController.DynamicControllerSimFunctions import chooseWeight
from FSMPlayers.RangePlayerSim import *
from FSMPlayers.MidRangeSim import *
from FSMPlayers.ShortRangeSim import *
from FSMPlayers.AllEnemy import *
from FSMPlayers.HumanPlayer import *
from util.inputFunctions import *
from DynamicController.DynamicControllerSim import *
from GENN.GENN import * 
from util.neural_net import *
import multiprocessing
import numpy as np 
import json

from util.constants import RANDOM_SEED, \
    SCREEN_HEIGHT, \
    SCREEN_WIDTH, \
    PLAYER_HEALTH, \
    KNIGHT_IMAGE, \
    ARROW_DAMAGE, \
    FIREBALL_DAMAGE, \
    KNIFE_DAMAGE, ARROW_SPEED

from util import constants

random.seed(RANDOM_SEED)

class Game:
    def __init__(self,width , height, title, iterations, player_1_type, player_2_type,conGames,currentGame,player_1_nets,player_2_nets,trendTracking,process_id):
        """
        Initializer
        """
        self.width = width
        self.height = height
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.grid = np.zeros(shape = (SCREEN_HEIGHT, SCREEN_WIDTH))
        self.curtime = 0
        self.written = 0

        self.trendTracking = trendTracking
        self.start = time.time()
        self.totalIterations = iterations
        self.iterations = iterations
        self.player1_type = player_1_type.lower()
        self.player2_type = player_2_type.lower()
        self.player1_score = 0
        self.player2_score = 0
        self.draws = 0
        self.conGames = conGames
        self.currentGame = currentGame
        self.process_id = process_id
        self.player_1_nets = player_1_nets
        self.player_2_nets = player_2_nets
        self.healthChanges = 0
        self.player1_previous_health = PLAYER_HEALTH
        self.player2_previous_health = PLAYER_HEALTH

    def jitter(self):
        self.player1.center_x = random.randint(0,SCREEN_WIDTH)
        self.player1.center_y = random.randint(0,SCREEN_HEIGHT)
        self.player2.center_x = random.randint(0,SCREEN_WIDTH)
        self.player2.center_y = random.randint(0,SCREEN_HEIGHT)

    def writeTrends(self):
        if self.written == 0 and self.iterations == self.totalIterations:
            with open("player1Trends.txt",'w+') as myfile:
                myfile.write(json.dumps(self.player1.trends))
                myfile.close()
            with open("player2Trends.txt",'w+') as myfile:
                myfile.write(json.dumps(self.player2.trends))
                myfile.close()
        else:
            with open("player1Trends.txt",'a') as myfile:
                myfile.write(json.dumps(self.player1.trends))
                myfile.close()
            with open("player2Trends.txt",'a') as myfile:
                myfile.write(json.dumps(self.player2.trends))
                myfile.close()    
        self.written += 1    
        self.player1.trends = {'arrow':0,'fire':0,'knife':0,'towardsOpponent' :0, 'awayOpponent':0,"movementChanges":0,"biggestTrend":0}
        self.player2.trends = {'arrow':0,'fire':0,'knife':0,'towardsOpponent' :0, 'awayOpponent':0,"movementChanges":0,"biggestTrend":0}

    def setup(self):
        self.player_list = []
        self.arrow_list = []
        self.fireball_list = []
        self.knife_list = []
        # self.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames

        # Set up the player
        if self.player1_type.lower() == 'range':
            self.player1 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'mid':
            self.player1 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'short':
            self.player1 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'master':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = None
            if self.currentGame == 0:
                self.player1.adjustingWeight = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.adjustingWeight = self.totalIterations - self.iterations
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'average':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.currentGame == 0:
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights()
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'random':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.currentGame == 0:
                shootWeights = [1/21] * 21
                moveWeights = [1/7] * 14 + [1/2] * 6
                self.player1.weights = [shootWeights,moveWeights]
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights()
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'train':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'shoot'
            if self.player1.adjusting == 'shoot':
                self.player1.adjustingWeight = abs(self.iterations) % 21 
            elif self.player1.adjusting == 'move':
                self.player1.adjustingWeight = abs(self.iterations) % 20
            if self.currentGame == 0:
                shootWeights = [0.349706412,0.003654498,0.007241115,0.007261579,0.056467904,0.014784824,0.07526815 ,0.008607914,0.009829359,0.025498057,0.007078288,0.006121223,0.023625114,0.013999045,0.01048127 ,0.010960692,0.009995443,0.009819444,0.00860488 ,0.011003079,0.329991729]#[1/21] * 21
                moveWeights = [0.252059263 ,0.412954499,0.063124614,0.091279546,0.107225891,0.017778723,0.055577464,0.124954272,0.141280095,0.131862092,0.050910787,0.083675091,0.16745422 ,0.299863443,0.087444364,0.912555636,0.642013021,0.357986979,0.463211574,0.536788426]#[1/7] * 14 + [1/2] * 6
                self.player1.weights = [shootWeights,moveWeights]
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights()
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'genn':
            self.player1 = GENN(KNIGHT_IMAGE,1)
            self.player1.net = self.player_1_nets[self.process_id]
            self.player1.model =  self.player1.net.createNetwork()
        elif self.player1_type.lower() == 'agenn':  # JTW add option for adaptive network
            self.player1 = GENN(KNIGHT_IMAGE,1)
            self.player1.net = self.player_1_nets[self.process_id]
            self.player1.model =  self.player1.net.createNetwork(adaptive = True)

        else:
            self.player1 = Enemy(KNIGHT_IMAGE,1)

        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.center_x = random.randint(0,SCREEN_WIDTH)
        self.player1.center_y = random.randint(0,SCREEN_HEIGHT)
        self.player1.score = 0
        self.player1.health = PLAYER_HEALTH
        self.player1.curtime = 0
        self.player1.total_time = 0
        self.player1.hitbox_list = []
        self.player1.arrow_list = []
        self.player1.fireball_list = []
        self.player1.knife_list = []
        self.player1.knife_num = 0
        self.player1.shield = 0
        self.player1.box = 150
        self.player1.trends = {'arrow':0,'fire':0,'knife':0,'towardsOpponent' :0, 'awayOpponent':0,"movementChanges":0,"biggestTrend":0}
        self.player1.lastMovement = ""        
        self.player1.currentTrend = 0

        # Set up bad guy
        if self.player2_type.lower() == 'range':
            self.player2 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'mid':
            self.player2 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'short':
            self.player2 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'master':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.conGames = self.conGames
            self.player2.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player2.id = "player2"
            self.player2.adjusting = None
            if self.currentGame == 0:
                self.player2.adjustingWeight = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.adjustingWeight = self.totalIterations - self.iterations
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                chooseWeight(self.player2)
        elif self.player2_type.lower() == 'average':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.conGames = self.conGames
            self.player2.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.currentGame == 0:
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights()
                chooseWeight(self.player2)
        elif self.player2_type.lower() == 'random':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.conGames = self.conGames
            self.player2.conCurrentGameId = multiprocessing.current_process()._identity[0]%self.conGames
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.currentGame == 0:
                self.player2.adjustingWeight = 0
                shootWeights = [1/21] * 21
                moveWeights = [1/7] * 14 + [1/2] * 6
                self.player2.weights = [shootWeights,moveWeights]
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.adjustingWeight = self.totalIterations - self.iterations
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights()
                chooseWeight(self.player2)
        elif self.player2_type.lower() == 'genn':
            self.player2 = GENN(KNIGHT_IMAGE,1)
            self.player2.net = self.player_2_nets[self.process_id]
            self.player2.model =  self.player2.net.createNetwork()
        elif self.player2_type.lower() == 'agenn':  # JTW add option for adaptive network
            self.player2 = GENN(KNIGHT_IMAGE,1)
            self.player2.net = self.player_2_nets[self.process_id]
            self.player2.model =  self.player2.net.createNetwork(adaptive = True)
        else:
            self.player2 = Enemy(KNIGHT_IMAGE,1)

        self.player2.center_x = random.randint(0,SCREEN_WIDTH)
        self.player2.center_y = random.randint(0,SCREEN_HEIGHT)
        self.player2.health = PLAYER_HEALTH
        self.player2.score = 0
        self.player2.curtime = 0
        self.player2.total_time = 0
        self.player2.type = self.player2_type.lower()
        self.player2.knife_num = 0
        self.player2.shield = 0
        self.player_list.append(self.player2)
        self.player2.hitbox_list = []
        self.player2.arrow_list = []
        self.player2.fireball_list = []
        self.player2.knife_list = []
        self.player1.opponent_hitbox_list = self.player2.hitbox_list
        self.player2.opponent_hitbox_list = self.player1.hitbox_list
        self.player2.opponent = self.player1
        self.player1.opponent = self.player2
        self.player2.box = 150
        self.player2.trends = {'arrow':0,'fire':0,'knife':0,'towardsOpponent' :0, 'awayOpponent':0,"movementChanges":0,"biggestTrend":0}
        self.player2.lastMovement = ""
        self.player2.currentTrend = 0

    def end_game(self):
        self.player1_score += self.player1.score
        self.player2_score += self.player2.score
        self.iterations -= 1


    def init_player(self):
        
        self.grid[self.player1.center_y][self.player1.center_x] = 1
        self.grid[self.player2.center_y][self.player2.center_x] = 1
    
    # There are 2 functions for each so it is easy to not interfere 
    # with each other
    def arrow1(self):
        self.arw = constants.ArrowSimulated(self.player1.center_x,self.player1.center_y,ARROW_SPEED,self.player1.box)
        self.player1.arrow_list.append(self.arw)
        
    def arrow2(self):

        self.arw = constants.ArrowSimulated(self.player2.center_x,self.player2.center_y,ARROW_SPEED,self.player2.box)
        self.player2.arrow_list.append(self.arw)
        
    def fire1(self):

        self.fireball = constants.FireballSimulated(self.player1.center_x,self.player1.center_y,ARROW_SPEED,self.player1.box)
        self.player1.fireball_list.append(self.fireball)
        
    def fire2(self):

        self.fireball = constants.FireballSimulated(self.player2.center_x,self.player2.center_y,ARROW_SPEED,self.player2.box)
        self.player2.fireball_list.append(self.fireball)
    
    def equip_shield1(self):

        self.player1.health += 50
        self.player1.shield += 1
    
    def equip_shield2(self):

        self.player2.health += 50
        self.player2.shield += 1

    def collisionCheck(self,player,projectile):
        if (
                (     player.center_x - player.box <= projectile.center_x + projectile.box and player.center_x + player.box >= projectile.center_x + projectile.box
                or   player.center_x - player.box <= projectile.center_x - projectile.box and player.center_x + player.box >= projectile.center_x - projectile.box
                or   player.center_x - player.box <= projectile.center_x and player.center_x + player.box >= projectile.center_x  )
                and 
                (    player.center_y - player.box <= projectile.center_y + projectile.box and player.center_y + player.box >= projectile.center_y + projectile.box
                or   player.center_y - player.box <= projectile.center_y - projectile.box and player.center_y + player.box >= projectile.center_y - projectile.box  
                or   player.center_y - player.box <= projectile.center_y and player.center_y + player.box >= projectile.center_y  
                )
            ):
            return True
        return False
    def update(self):
        # sets a timer that game and perspective players use
        # not sure if necessary
        self.curtime += 1 
        self.player1.update()
        self.player2.update()
        if self.trendTracking == 'yes': 
            if self.curtime % 900 == 0: self.writeTrends()

        # player 1 collision
        if self.player1.center_y >= self.height:
            self.player1.center_y = self.height
        if self.player1.center_y <= 0:
            self.player1.center_y = 0
        if self.player1.center_x >= self.width:
            self.player1.center_x = self.width
        if self.player1.center_x <= 0:
            self.player1.center_x = 0
        # player 2 collision
        if self.player2.center_y >= self.height:
            self.player2.center_y = self.height
        if self.player2.center_y <= 0:
            self.player2.center_y = 0
        if self.player2.center_x >= self.width:
            self.player2.center_x = self.width
        if self.player2.center_x <= 0:
            self.player2.center_x = 0


        
        # Stop at hit boxes
        # Only needs to be done for one player
        # if self.player1.center_x - self.player1.box <= self.player2.center_x + self.player2.box:
        #     self.player1.center_x = self.player2.center_x + self.player2.box + self.player1.box
        # elif self.player1.center_x + self.player1.box >= self.player2.center_x - self.player2.box:
        #     self.player1.center_x = self.player2.center_x - self.player2.box - self.player1.box
        # if self.player1.center_y - self.player1.box <= self.player2.center_y + self.player2.box:
        #     self.player1.center_y = self.player2.center_y + self.player2.box + self.player1.box
        # elif self.player1.center_y + self.player1.box >= self.player2.center_y - self.player2.box:
        #     self.player1.center_y = self.player2.center_y - self.player2.box - self.player1.box
        


        #fireball movement
        for self.fireball in self.player1.fireball_list:
            if self.collisionCheck(self.player2,self.fireball):
                self.player1.fireball_list.remove(self.fireball)
                self.player2.health -= FIREBALL_DAMAGE
            elif self.fireball.center_x < -5 or self.fireball.center_x > SCREEN_WIDTH +5 or self.fireball.center_y < -5 or self.fireball.center_y > SCREEN_HEIGHT + 5:
                self.player1.fireball_list.remove(self.fireball)
            self.fireball.center_x += self.fireball.vel*math.cos(self.player1.angle)
            self.fireball.center_y += self.fireball.vel*math.sin(self.player1.angle)

        #fireball movement
        for self.fireball in self.player2.fireball_list:
            if self.collisionCheck(self.player1,self.fireball):
                self.player2.fireball_list.remove(self.fireball)
                self.player1.health -= FIREBALL_DAMAGE
            elif self.fireball.center_x < -5 or self.fireball.center_x > SCREEN_WIDTH +5 or self.fireball.center_y < -5 or self.fireball.center_y > SCREEN_HEIGHT + 5:
                self.player2.fireball_list.remove(self.fireball)
            self.fireball.center_x += self.fireball.vel*math.cos(self.player2.angle)
            self.fireball.center_y += self.fireball.vel*math.sin(self.player2.angle)
    

        # Arrow movement
        for self.arw in self.player1.arrow_list:
                        # Player 2 and arrow hit check
            if self.collisionCheck(self.player2,self.arw):
                self.player1.arrow_list.remove(self.arw)
                self.player2.health -= ARROW_DAMAGE
            elif self.arw.center_x < -5 or self.arw.center_x > SCREEN_WIDTH+5 or self.arw.center_y < -5 or self.arw.center_y > SCREEN_HEIGHT +5:
                self.player1.arrow_list.remove(self.arw)

            self.arw.center_x += self.arw.vel*math.cos(self.player1.angle)
            self.arw.center_y += self.arw.vel*math.sin(self.player1.angle)

        # Arrow movement
        for self.arw in self.player2.arrow_list:
            if self.collisionCheck(self.player1,self.arw):
                self.player2.arrow_list.remove(self.arw)
                self.player1.health -= ARROW_DAMAGE
            elif self.arw.center_x < -5 or self.arw.center_x > SCREEN_WIDTH +5 or self.arw.center_y < -5 or self.arw.center_y > SCREEN_HEIGHT + 5:
                self.player2.arrow_list.remove(self.arw)

            self.arw.center_x += self.arw.vel*math.cos(self.player2.angle)
            self.arw.center_y += self.arw.vel*math.sin(self.player2.angle)
        

        for self.knife in self.player1.knife_list:
            if self.collisionCheck(self.player2,self.knife):
                self.player2.health -= KNIFE_DAMAGE
            self.player1.knife_list.remove(self.knife)

        for self.knife in self.player2.knife_list:
            if self.collisionCheck(self.player1,self.knife):
                self.player1.health -= KNIFE_DAMAGE
            self.player2.knife_list.remove(self.knife)


        
                
        # If health is zero kill them
        if self.player1.health <= 0 and self.player2.health <= 0:
            self.draws += 1
            self.end_game()
            if self.iterations == 0: return "0"
            else: self.setup()
        elif self.player2.health <= 0:
            self.player1.score += 1 
            self.end_game()
            if self.player1.shield == 0:
                if self.iterations == 0: return self.player1.health - self.player2.health + 500
                else: self.setup()
            else:
                if self.iterations == 0: return self.player1.health - self.player2.health
                else: self.setup()
        elif self.player1.health <= 0:
            self.player2.score += 1 
            self.end_game()
            if self.player2.shield == 0:
                if self.iterations == 0: 
                    self.writeTrends()
                    return self.player1.health - self.player2.health - 500
                else: self.setup()
            else:
                if self.iterations == 0: 
                    self.writeTrends()
                    return self.player1.health - self.player2.health
                else: self.setup()
        if self.player1.health == self.player1_previous_health and self.player2_previous_health == self.player2.health: self.healthChanges += 1
        else: self.healthChanges = 0
        if self.healthChanges > 1500: 
            self.jitter()
            self.healthChanges = 0
        self.player1_previous_health = self.player1.health
        self.player2_previous_health = self.player2.health
        return True
        
