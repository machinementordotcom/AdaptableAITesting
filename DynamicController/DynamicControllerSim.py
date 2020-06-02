import math
import random
import arcade
import csv
import DynamicController.DynamicControllerSimFunctions as dcsf
import numpy as np
from util.constants import RANDOM_SEED, \
    PLAYER_HEALTH, SCREEN_WIDTH, SCREEN_HEIGHT

random.seed(RANDOM_SEED)


class DynamicController(arcade.Sprite):
    def check_for_collision(self,player,projectiles):
        for projectile in projectiles:
            start_x = projectile.center_x
            start_y = projectile.center_y
            if start_x - projectile.box <= player.center_x + player.box or start_x + projectile.box >= player.center_x - player.box and start_y + projectile.box <= player.center_y - player.box or start_y + projectile.box >= player.center_y - player.box:
                    return True
            while start_x > 0 and start_y > 0 and start_x < SCREEN_WIDTH and start_y < SCREEN_HEIGHT:
                start_x += projectile.vel*math.cos(angle)
                start_y += projectile.vel*math.sin(angle)
                if start_x - projectile.box <= player.center_x + player.box or start_x + projectile.box >= player.center_x - player.box and start_y + projectile.box <= player.center_y - player.box or start_y + projectile.box >= player.center_y - player.box:
                    return True
        return False

    def equipshield(self):
        self.health += PLAYER_HEALTH*.5
        self.shield +=1

    def writeWeights(self):
        with open("DynamicController/weightsDynamicController" + self.id + "-" + str(self.conCurrentGameId) + ".csv", 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i in range(2):
                wr.writerow(self.weights[i])

    def readWeights(self,path = None):
        tempWeights = [[],[]] 
        if path == None:
            for i in range(self.conGames):
                with open('DynamicController/weightsDynamicController' + self.id + "-" + str(self.conCurrentGameId) + '.csv') as csvfile:
                    reader = csv.reader(csvfile)
                    weightType = 0
                    for row in reader:
                        tempWeights[weightType].append([float(i) for i in row])
                        weightType +=1
            self.weights[0] = np.average(np.array(tempWeights[0]),axis = 0).tolist()
            self.weights[1] = np.average(np.array(tempWeights[1]),axis = 0).tolist()
        else:
            with open(path) as csvfile:
                reader = csv.reader(csvfile)
                weightType = 0
                for row in reader:
                    self.weights[weightType] = [float(i) for i in row]
                    weightType +=1

    def update(self):
        self.curtime += 1
        self.total_time += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        dcsf.playerLogic(self)
        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                self.fireball_list.remove(fireball)
        if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()
        health_diff = self.health - self.opponent.health
            # If the dynamic controller fails to cause an overall increase of 100 health in the game choose different weights but don't penalize the current weights
        if self.total_time == 300:
            dcsf.update_weights(self,False)
            self.total_time = 0
            # If combined health lost is greater than the update rate (100). Change the weights
        if self.health + self.opponent.health <= self.totalHealthBenchmark:
                # Calculate the health difference between the players for the training period
            self.benchmarkDifference = health_diff - self.benchmarkDifference
            self.totalHealthBenchmark -= 100
            self.total_time = 0
            dcsf.update_weights(self,True)
