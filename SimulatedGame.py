import arcade
import os
import math
import random
import sys
import time
from FSMPlayers.RangePlayer import *
from FSMPlayers.MidRangePlayer import *
from FSMPlayers.ShortRangePlayer import *
from FSMPlayers.AllEnemy import *
from util.inputFunctions import *
from DynamicController.DynamicController import *

from util import constants
from util.constants import KNIGHT_IMAGE, FIREBALL_DAMAGE, ARROW_DAMAGE, KNIFE_DAMAGE


class SimulatedGame(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title,iterations,player_1_type,player_2_type):
        """
        Initializer
        """
        super().__init__(width, height, title)
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
        self.start = time.time()
        self.totalIterations = iterations
        self.iterations = iterations
        self.player1_type = player_1_type.lower()
        self.player2_type = player_2_type.lower()

        # Sprite lists
        self.player_list = None
        self.arrow_list = None
        self.fireball_list = None
        self.hitbox_list = None

        # Set up the player
        self.player2_sprite = None
        self.player1 = None
        self.player1_score = 0
        self.player2_score = 0
        self.draws = 0

    def end_game(self):
        self.player1_score += self.player1.score
        self.player2_score += self.player2.score
        self.iterations -= 1

        if self.iterations == 0:
            print("player 1 (" + self.player1_type + ") :",str(self.player1_score))
            file = open("player1score.txt","w")
            file.write(str(self.player1_score))
            file.close()
            print("player 2 (" + self.player2_type + ") :",str(self.player2_score))
            file = open("player2score.txt","w")
            file.write(str(self.player2_score)) 
            file.close()
            print("Draws :",self.draws)
            print("Total Time: ",time.time() - self.start)
            print('\a')
            raise Exception("End")
            # return False
            # sys.exit()
        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        spacer()
        print("Total iterations %d out of %d" % (abs(self.iterations - self.totalIterations) +1, self.totalIterations) )
        self.player_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.knife_list = arcade.SpriteList()

        # Set up the player
        if self.player1_type.lower() == 'range':
            self.player1 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'mid':
            self.player1 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'short':
            self.player1 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'master':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.id = "player1"
            self.player1.adjusting = None
            if self.iterations == self.totalIterations:
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
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.iterations == self.totalIterations:
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
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.iterations == self.totalIterations:
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
        else:
            self.player1 = Enemy(KNIGHT_IMAGE,1)

        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.center_x = random.randint(10,900)
        self.player1.center_y = random.randint(10,600)
        self.player1.score = 0
        self.player1.health = PLAYER_HEALTH
        self.player1.curtime = 0
        self.player1.total_time = 0
        self.player1.hitbox_list = arcade.SpriteList()
        self.player1.arrow_list = arcade.SpriteList()
        self.player1.fireball_list = arcade.SpriteList()
        self.player1.knife_list = arcade.SpriteList()
        self.player1.knife_num = 0
        self.player1.shield = 0

        # Set up bad guy
        if self.player2_type.lower() == 'range':
            self.player2 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'mid':
            self.player2 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'short':
            self.player2 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'master':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.id = "player2"
            self.player2.adjusting = None
            if self.iterations == self.totalIterations:
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
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.iterations == self.totalIterations:
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
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.iterations == self.totalIterations:
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
        else:
            self.player2 = Enemy(KNIGHT_IMAGE,1)

        self.player2.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player2.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player2.center_x = random.randint(10,900)
        self.player2.opponent = self.player1
        self.player2.center_y = random.randint(10,600)
        self.player2.type = random.choice(["range","mid","short"])
        self.player2.health = PLAYER_HEALTH
        self.player2.score = 0
        self.player2.curtime = 0
        self.player2.total_time = 0
        self.player2.type = self.player2_type.lower()
        self.player2.knife_num = 0
        self.player2.shield = 0
        self.player_list.append(self.player2)
        self.player2.hitbox_list = arcade.SpriteList()
        self.player2.arrow_list = arcade.SpriteList()
        self.player2.fireball_list = arcade.SpriteList()
        self.player2.knife_list = arcade.SpriteList()
        self.player1.opponent_hitbox_list = self.player2.hitbox_list
        self.player2.opponent_hitbox_list = self.player1.hitbox_list
        self.player1.opponent = self.player2
        self.player_list.append(self.player1)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
    
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        
        self.player_list.draw()
        self.player1.arrow_list.draw()
        self.player1.fireball_list.draw()
        self.player2.arrow_list.draw()
        self.player2.fireball_list.draw()
        self.knife_list.draw()
        self.player2.knife_list.draw()
        self.player1.hitbox_list.draw()
        self.player2.hitbox_list.draw()
        # Draw player health
        x = self.player1.center_x
        y = self.player1.center_y
        arcade.draw_rectangle_filled(x, y - 16, 24, 4, (255, 0, 0))
        arcade.draw_rectangle_filled(x - math.ceil((24 - (self.player1.health / 4.16)) / 2), y - 16, math.ceil(self.player1.health / 4.16), 4, (0, 255, 0))
         
        # Draw player2 health
        x = self.player2.center_x
        y = self.player2.center_y
        arcade.draw_rectangle_filled(x, y - 16, 24, 4, (255, 0, 0))
        arcade.draw_rectangle_filled(x - math.ceil((24 - (self.player2.health / 4.16)) / 2), y - 16, math.ceil(self.player2.health / 4.16), 4, (0, 255, 0))


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            sys.exit()

    # Functions that change with time
    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites
        # self.arrow_list.update()
        #self.physics_engine.update()
        # self.fireball_list.update()
        self.player_list.update()
        self.player2.fireball_list.update()
        self.player2.arrow_list.update()
        self.player1.fireball_list.update()
        self.player1.arrow_list.update()
        self.player1.hitbox_list.update()
        self.player2.hitbox_list.update()

        #player collision
        if self.player1.center_x <= 0:
            self.player1.center_x = 0
        elif self.player1.center_x >= SCREEN_WIDTH:
            self.player1.center_x = SCREEN_WIDTH
        if self.player1.center_y <= 0:
            self.player1.center_y = 0
        elif self.player1.center_y >= SCREEN_HEIGHT:
            self.player1.center_y = SCREEN_HEIGHT
        #player2 collision
        if self.player2.center_x <= 0:
            self.player2.center_x = 0
        elif self.player2.center_x >= SCREEN_WIDTH:
            self.player2.center_x = SCREEN_WIDTH
        if self.player2.center_y <= 0:
            self.player2.center_y = 0
        elif self.player2.center_y >= SCREEN_HEIGHT:
            self.player2.center_y = SCREEN_HEIGHT


        for knife in self.knife_list:
            knife.center_x = self.player1.center_x
            knife.center_y = self.player1.center_y
            knife.angle = self.player1.angle+180
        
        for knife in self.player2.knife_list:
            knife.center_x = self.player2.center_x
            knife.center_y = self.player2.center_y
            knife.angle = self.player2.angle+180
            
        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                fireball.kill()
       
        # Hit function for fireball)
        fireball_hit1 = arcade.check_for_collision_with_list(self.player2, self.player1.fireball_list)
        for fireball in fireball_hit1:
            fireball.kill()
            self.player2.health -= FIREBALL_DAMAGE

        fireball_hit2 = arcade.check_for_collision_with_list(self.player1, self.player2.fireball_list)
        for fireball in fireball_hit2:
            fireball.kill()
            self.player1.health -= FIREBALL_DAMAGE
       
        # Hit function for arrrow
        arrow_hit1 = arcade.check_for_collision_with_list(self.player2, self.player1.arrow_list) # for bad guy
        for arrow in arrow_hit1:
            arrow.kill()
            self.player2.health -= ARROW_DAMAGE
        arrow_hit2 = arcade.check_for_collision_with_list(self.player1, self.player2.arrow_list) # for bad guy
        for arrow in arrow_hit2:
            arrow.kill()
            self.player1.health -= ARROW_DAMAGE
        # Hit function for knife
        knife_hit1 = arcade.check_for_collision_with_list(self.player2, self.player1.knife_list) # for bad guy
        for knife in knife_hit1:
            knife.kill()
            self.player2.health -= KNIFE_DAMAGE
            self.player1.knife_num = 0
            
        knife_hit2 = arcade.check_for_collision_with_list(self.player1, self.player2.knife_list) # for bad guy
        for knife in knife_hit2:
            knife.kill()
            self.player1.health -= KNIFE_DAMAGE
            self.player2.knife_num = 0
        
        # If health is zero kill them
        if self.player1.health <= 0 and self.player2.health <= 0:
            self.draws += 1
            self.end_game()
        elif self.player2.health <= 0:
            self.player2.kill()
            self.player1.score += 1 
            self.end_game()
            
        elif self.player1.health <= 0:
            self.player1.kill()  
            self.player2.score += 1 
            self.end_game()