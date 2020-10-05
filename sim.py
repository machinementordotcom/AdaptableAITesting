
from arcade import Sprite
from os import path
from math import cos, sin, sqrt
from random import randint, seed
from time import time
#from FSMPlayers.RangePlayerSim import *
#from FSMPlayers.MidRangeSim import *
#from FSMPlayers.ShortRangeSim import *
#from FSMPlayers.AllEnemy import *
# from FSMPlayers.HumanPlayer import *
# from util.inputFunctions import *
# from DynamicController.DynamicControllerSim import *
from GENN.GENN import * 
from util.constants import *
from numpy import zeros
from GENN.GENNFunctions import *
from datetime import datetime
from pandas import DataFrame

seed(RANDOM_SEED)

class Game:
    def __init__(self, width, height, title, games, player_1_type, player_2_type,
                 conGames, rounds, player_1_nets, player_2_nets, bestNets,  #NH repurposed 'trendtracking' as bestNet
                 process_id):
        """
        Initializer
        """
        self.width = width
        self.height = height
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
#        file_path = os.path.dirname(os.path.abspath(__file__))
#        os.chdir(file_path)
        self.grid = zeros(shape = (SCREEN_HEIGHT, SCREEN_WIDTH))
        self.curtime = 0
        self.written = 0
#        self.start = time()
        self.totalGames = games
        self.games = games
        self.player1_type = player_1_type.lower()
        self.player2_type = player_2_type.lower()
        self.player1_score = 0
        self.player2_score = 0
        self.draws = 0
        self.conGames = conGames
        self.rounds = rounds
        self.process_id = process_id
        self.player_1_nets = player_1_nets
        self.player_2_nets = player_2_nets
#        self.healthChanges = 0
#        self.player1_previous_health = PLAYER_HEALTH
#        self.player2_previous_health = PLAYER_HEALTH
#        self.player_1_simulation = player_1_simulation
#        self.player_2_simulation = player_2_simulation
        self.start = 0 # NH - for calculation of CPU move time
        self.end = 0
        self.health_diff = 0
        self.bestNets = bestNets
        
        print("Game Initialized for process ID/network: ",str(process_id))

    def jitter(self):
        self.player1.center_x = randint(0,SCREEN_WIDTH)
        self.player1.center_y = randint(0,SCREEN_HEIGHT)
        self.player2.center_x = randint(0,SCREEN_WIDTH)
        self.player2.center_y = randint(0,SCREEN_HEIGHT)

    def setup(self, model=None):  #RunOneGame comes here first
        
        print("Running self.setup")
        self.player_list = []
        self.arrow_list = []
        self.fireball_list = []
        self.knife_list = []
        self.curtime = 0
        self.start = datetime.now()
        rounds = self.rounds
        game_num = self.games
        
        self.progress_data = DataFrame(
            {'games': [],
             'model_id': [],
             'player_1_type': [],
             'player_2_type': [],
             'conCurrentGames': [],
             'rounds': [],
             'process_id': [],
             'agenn_v': [],
             'player1_center_x': [],
             'player1_center_y': [],
             'player1_shield': [],
             'player2_center_x': [],
             'player2_center_y': [],
             'player2_shield': [],
             'player1_fireball': [],
             'player2_fireball': [],
             'player1_arrow': [],
             'player1_knife': [],
             'player2_knife': [],
             'game_move': [],
             'player1_health': [],
             'player2_health': [],
             'fitness': [],
             'timestamp': []}
)

        # Set up player1
#        print("Setting up player1 as",self.player1_type,self.player_1_simulation)
        if self.player1_type == 'genn' or self.player1_type == 'agenn':

            self.player1 = GENN(KNIGHT_IMAGE,1)
            self.player1.net = self.player_1_nets[self.process_id]

            if rounds % 11 == 0 and rounds != 0 and game_num == 9:  ## In every 10th round models will be retrieved from omega
                original = str(self.player1.net)
                newname = str('gen%dp%d' % (self.rounds, self.process_id))
                self.player1.model = om.models.get(original)
                print("Player %d retrieved from omega" % (self.process_id))
                ## Save model to omega as current round model
                om.models.put(self.player1.model, newname)
                print("Player",original,"saved to omega as",newname)

            elif game_num < 9:  ## If this isn't the first game of the round, keep the same model
                self.player1.model = model
                
#                self.player1.model = om.models.get('gen%dp%d' % (self.rounds, self.process_id))
                
            else: ## if it's the first game in the round, create the network
                self.player1.model = self.player1.net.createNetwork(self.rounds, self.process_id)
                print("Creating new network")
        
        """elif self.player1_type.lower() == 'range':
            from FSMPlayers.RangePlayerSim import RangePlayer
            self.player1 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'mid':
            from FSMPlayers.MidRangeSim import MidRangePlayer
            self.player1 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'short':
            from FSMPlayers.ShortRangeSim import ShortRangePlayer
            self.player1 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'master':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = None
            if self.rounds == 0:
                self.player1.adjustingWeight = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.adjustingWeight = self.totalGames - self.games
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'average':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.rounds == 0:
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
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.rounds == 0:
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
            self.player1.conGames = self.conGames
            self.player1.id = "player1"
            self.player1.adjusting = 'shoot'
            if self.player1.adjusting == 'shoot':
                self.player1.adjustingWeight = abs(self.games) % 21 
            elif self.player1.adjusting == 'move':
                self.player1.adjustingWeight = abs(self.games) % 20
            if self.rounds == 0:
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

                
        else:
            self.player1 = Enemy(KNIGHT_IMAGE,1)
            """

#        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
#        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.center_x = randint(0,SCREEN_WIDTH)
        self.player1.center_y = randint(0,SCREEN_HEIGHT)
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
        self.player1.version = 1
        self.player1.health_diff = 0

        # Set up opponent
        if self.games == 9:  ## If this is the first game in a round, set up range from scratch
            from FSMPlayers.RangePlayerSim import RangePlayer
            self.player2 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.games in [8, 7]:
            pass
        elif self.games == 6:
            from FSMPlayers.MidRangeSim import MidRangePlayer
            self.player2 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.games in [5, 4]:
            pass
        elif self.games == 3:
            from FSMPlayers.ShortRangeSim import ShortRangePlayer
            self.player2 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif game_num in [2, 1]:
            pass
        
            """elif self.player2_type.lower() == 'master':
                self.player2 = DynamicController(KNIGHT_IMAGE,1)
                self.player2.conGames = self.conGames
                self.player2.id = "player2"
                self.player2.adjusting = None
                if self.rounds == 0:
                    self.player2.adjustingWeight = 0
                    self.player2.weights = [[],[]]
                    self.player2.readWeights("DynamicController/masterWeights.csv")
                    self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                    self.player2.benchmarkDifference = 0
                    self.player2.shootRule = None
                    self.player2.moverule = None
                    chooseWeight(self.player2)
                else:
                    self.player2.adjustingWeight = self.totalGames - self.games
                    self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                    self.player2.benchmarkDifference = 0
                    self.player2.weights = [[],[]]
                    self.player2.readWeights("DynamicController/masterWeights.csv")
                    chooseWeight(self.player2)
            elif self.player2_type.lower() == 'average':
                self.player2 = DynamicController(KNIGHT_IMAGE,1)
                self.player2.conGames = self.conGames
                self.player2.id = "player2"
                self.player2.adjusting = 'both'
                if self.rounds == 0:
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
                self.player2.id = "player2"
                self.player2.adjusting = 'both'
                if self.rounds == 0:
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
                    self.player2.adjustingWeight = self.totalGames - self.games
                    self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                    self.player2.benchmarkDifference = 0
                    self.player2.weights = [[],[]]
                    self.player2.readWeights()
                    chooseWeight(self.player2)
            elif self.player2_type is 'genn':
                self.player2 = GENN(KNIGHT_IMAGE,1)
                self.player2.net = self.player_2_nets[self.process_id]
                self.player2.model =  self.player2.net.createNetwork(self.rounds, self.process_id)
            else:
                self.player2 = Enemy(KNIGHT_IMAGE,1)
                """

        self.player2.center_x = randint(0,SCREEN_WIDTH)
        self.player2.center_y = randint(0,SCREEN_HEIGHT)
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
      
        print("Game setup complete for Process ID/Network: ",str(self.process_id))
    
    def end_game(self):
 
        self.player1_score += self.player1.score
        self.player2_score += self.player2.score
                
        if self.games > 0:
            self.games -= 1
        
        # NH - reversed order of games to front load longer-lasting 'range' games
        # NH - added fitness scoring by opponent type, to be averaged at end of round
        if self.games > 6: 
            self.player2_type = 'range'
        elif self.games <= 6 and self.games > 3: 
            self.player2_type = 'mid'
        elif self.games <= 3 and self.games > 0: 
            self.player2_type = 'short'
        
        print("Player",str(self.process_id),"game over.",str(self.games),"games left")
                    
        # NH - added this here, as it seems more fitting to have it here
        
        if self.player1.health <= 0 and self.player2.health <= 0:
            self.player1.health_diff = 0
                       
        if self.player1.shield == 0:
            self.player1.health = self.player1.health + 500
            print("Player1 gets shield bonus, final health is",self.player1.health)
            
        if self.player2.shield == 0:
            self.player1.health = self.player1.health - 500
            print("Player1 gets shield penalty, final health is",self.player1.health)
        
        self.player1.health_diff = self.player1.health - self.player2.health
        self.health_diff += self.player1.health_diff

        if self.games == 0: 
            print("Round over for player",str(self.process_id),", calculating final fitness")
            self.health_diff = self.health_diff / self.totalGames  # Returns average fitness across all games in round
            print("Final fitness is",self.health_diff)
            return self.health_diff
        
        else: 
            self.setup(self.player1.model)
            return True
        
    def init_player(self):
        print('Running init_player')
        self.grid[self.player1.center_y][self.player1.center_x] = 1
        self.grid[self.player2.center_y][self.player2.center_x] = 1
    
    # There are 2 functions for each so it is easy to not interfere 
    # with each other
    def arrow1(self):
        self.arw = ArrowSimulated(self.player1.center_x,self.player1.center_y,ARROW_SPEED,self.player1.box)
        self.player1.arrow_list.append(self.arw)
        
    def arrow2(self):

        self.arw = ArrowSimulated(self.player2.center_x,self.player2.center_y,ARROW_SPEED,self.player2.box)
        self.player2.arrow_list.append(self.arw)
        
    def fire1(self):

        self.fireball = FireballSimulated(self.player1.center_x,self.player1.center_y,ARROW_SPEED,self.player1.box)  
        self.player1.fireball_list.append(self.fireball)
        
    def fire2(self):

        self.fireball = FireballSimulated(self.player2.center_x,self.player2.center_y,ARROW_SPEED,self.player2.box)  
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

        # Attack Data Holder
        player1_fireball = 0
        player2_fireball = 0 
        player1_arrow = 0
        player2_arrow = 0
        player1_knife = 0
        player2_knife = 0
        rounds, val, process_id, games = self.rounds, 1, self.process_id, self.games
        player1, player2 = self.player1, self.player2
        self_height, self_width = self.height, self.width
        center_y_1, center_y_2 = self.player1.center_y, self.player2.center_y
        center_x_1, center_x_2 = self.player1.center_x, self.player2.center_x
        player_1_health, player_2_health = self.player1.health, self.player2.health
        player_1_type, player_2_type = self.player1_type, self.player2_type
        games = self.games
        player1_shield, player2_shield = self.player1.shield, self.player2.shield
        timestamp = datetime.now()
        max_moves = 500
        val = True

        self.curtime += 1
        curtime = self.curtime
        
        player1.update(rounds, process_id)
        player2.update()
        
        
        
        fitness = [player_1_health - player_2_health]
        
        # player 1 collision
        if center_y_1 >= self_height:
            self.player1.center_y = self_height
        if center_y_1 <= 0:
            self.player1.center_y = 0
        if center_x_1 >= self_width:
            self.player1.center_x = self_width
        if center_x_1 <= 0:
            self.player1.center_x = 0
        # player 2 collision
        if center_y_2 >= self_height:
            self.player2.center_y = self_height
        if center_y_2 <= 0:
            self.player2.center_y = 0
        if center_x_2 >= self_width:
            self.player2.center_x = self_width
        if center_x_2 <= 0:
            self.player2.center_x = 0
        
        #fireball movement

        for self.fireball in self.player1.fireball_list:
            if self.collisionCheck(self.player2,self.fireball):
                self.player1.fireball_list.remove(self.fireball)
                self.player2.health -= FIREBALL_DAMAGE
                
                player2_fireball = 1
                
            elif self.fireball.center_x < -5 or self.fireball.center_x > SCREEN_WIDTH +5 or self.fireball.center_y < -5 or self.fireball.center_y > SCREEN_HEIGHT + 5:
                self.player1.fireball_list.remove(self.fireball)
            self.fireball.center_x += self.fireball.vel*cos(self.player1.angle)
            self.fireball.center_y += self.fireball.vel*sin(self.player1.angle)

        #fireball movement
        for self.fireball in self.player2.fireball_list:
            if self.collisionCheck(self.player1,self.fireball):
                self.player2.fireball_list.remove(self.fireball)
                self.player1.health -= FIREBALL_DAMAGE
                
                player1_fireball = 1
                
            elif self.fireball.center_x < -5 or self.fireball.center_x > SCREEN_WIDTH +5 or self.fireball.center_y < -5 or self.fireball.center_y > SCREEN_HEIGHT + 5:
                self.player2.fireball_list.remove(self.fireball)
            self.fireball.center_x += self.fireball.vel*cos(self.player2.angle)
            self.fireball.center_y += self.fireball.vel*sin(self.player2.angle)

        # Arrow movement
        for self.arw in self.player1.arrow_list:
                        # Player 2 and arrow hit check
            if self.collisionCheck(self.player2,self.arw):
                self.player1.arrow_list.remove(self.arw)
                self.player2.health -= ARROW_DAMAGE
                
                player2_arrow = 1
                
            elif self.arw.center_x < -5 or self.arw.center_x > SCREEN_WIDTH+5 or self.arw.center_y < -5 or self.arw.center_y > SCREEN_HEIGHT +5:
                self.player1.arrow_list.remove(self.arw)

            self.arw.center_x += self.arw.vel*cos(self.player1.angle)
            self.arw.center_y += self.arw.vel*sin(self.player1.angle)

        # Arrow movement
        for self.arw in self.player2.arrow_list:
            if self.collisionCheck(self.player1,self.arw):
                self.player2.arrow_list.remove(self.arw)
                self.player1.health -= ARROW_DAMAGE
                
                player1_arrow = 1
                
            elif self.arw.center_x < -5 or self.arw.center_x > SCREEN_WIDTH +5 or self.arw.center_y < -5 or self.arw.center_y > SCREEN_HEIGHT + 5:
                self.player2.arrow_list.remove(self.arw)

            self.arw.center_x += self.arw.vel*cos(self.player2.angle)
            self.arw.center_y += self.arw.vel*sin(self.player2.angle)

        
        #Knife Movement 
        for self.knife in self.player1.knife_list:
            if self.collisionCheck(self.player2,self.knife):
                self.player2.health -= KNIFE_DAMAGE
                
                player2_knife = 1
                
            self.player1.knife_list.remove(self.knife)

        for self.knife in self.player2.knife_list:
            if self.collisionCheck(self.player1,self.knife):
                self.player1.health -= KNIFE_DAMAGE
                
                player1_knife = 1
                
            self.player2.knife_list.remove(self.knife)
        
        ## Reporting in console
        interval = 249
        if not curtime % interval == 0:  ## added intermittent updates instead of every move
            pass
        else:
            self.end = datetime.now()
            try: avg = (self.end-self.start) / interval
            except: 
                avg = 0 
                print("start time unknown")
            print("\nRound:",str(rounds),
                  "\nGames left:",str(games),
                  "\nPlayer:",str(process_id),
                  "\nMove:",str(curtime),
                  "\nPlayer1 Health:", str(player_1_health),
                  "\nPlayer2 Health:", str(player_2_health),
                  "\nPlayer1 Fitness:", str(fitness),
                  "\nAvg move time:", avg
                 )
            self.start = datetime.now()
            

        # aGENN Supervisor
        # NH - making change to use current difference as only metric
        
#        current_fitness = self.player1.health - self.player2.health
        # NH - changed from 'player_1_simulation

        if player_1_type != 'agenn':
            pass
        elif curtime % 99 == 0 and rounds >= 1 and fitness[0] < 0: # To capture top model from gen 0
            self.player1.version += 1
            print("Supervisor sent player",
              str(process_id),
              "back for training. Now player is version",
              str(self.player1.version))
            # Create aGENN log to record all Supervisor actions
            # Write a subroutine to access stream and train model
            model_id = 'gen%dp%d' % (rounds, process_id)
            self.player1.model = aGENN_train(model_id, rounds)
        
        
            #Print The Log Result
        newrow = dict(
            games = games,
            model_id = str('gen%dp%d' % (rounds, process_id)),
            player_1_type = player_1_type,
            player_2_type = player_2_type,
            conCurrentGames = games,
            rounds = rounds,
            process_id = process_id,
            agenn_v = self.player1.version,
            player1_center_x = center_x_1,
            player_1_center_y = center_y_1,
            player1_shield = player1_shield,
            player2_center_x = center_x_2,
            player_2_center_y = center_y_2,
            player2_shield = player2_shield,
            player1_fireball = player1_fireball,
            player2_fireball = player2_fireball,
            player1_arrow = player1_arrow,
            player2_arrow = player2_arrow,
            player1_knife = player1_knife,
            player2_knife = player2_knife,
            game_move = curtime, 
            player1_health = player_1_health,
            player2_health = player_2_health,
            health_diff = fitness, # NH - replaced separate health points above
            timestamp = timestamp,
            )
        
#        self.progress_data = self.progress_data.append(newrow, ignore_index=True)
        
        if curtime % 1 != 0:
            pass
        else:         
            dataFrame = DataFrame(newrow)
            file_name = 'data_log.csv'
            if path.exists(file_name):
                dataFrame.to_csv(file_name, mode='a', header=False, index=False)
            else:
                dataFrame.to_csv(file_name, mode='w', header=True, index=False)
                
#            self.progress_data = self.progress_data[0:0]  #remove all rows in dataframe
      


       
        # Check for end of game state
        if curtime >= max_moves:
            print("Game has reached max moves of",str(max_moves))
            
            if player_1_health == player_2_health:
                self.draws += 1
                print("Game ends in a draw")
                val = self.end_game()
                
            elif player_1_health > player_2_health:
                self.player1.score +=1
                print("Player1 wins")
                val = self.end_game()
                
            else:
                self.player2.score +=1
                print("Player2 wins")
                val = self.end_game()
             
        elif player_1_health <= 0 and player_2_health <= 0:
            print("Both players are at zero health")
            self.draws += 1
            print("Game ends in a draw")
            val = self.end_game()
                
        elif player_2_health <= 0:
            self.player1.score += 1 
            val = self.end_game()
            
        elif player_1_health <= 0:
            self.player2.score += 1 
            val = self.end_game()
                           
        return val
        
