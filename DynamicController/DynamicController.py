import arcade
import math
import random
import csv
import DynamicController.dynamicControllerFunctions as dcf

from util.constants import RANDOM_SEED, PLAYER_HEALTH

random.seed(RANDOM_SEED)
class DynamicController(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += PLAYER_HEALTH*.5
        self.shield +=1

    def writeWeights(self):
        with open("DynamicController/weightsDynamicController" + self.id + ".csv", 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i in range(2):
                wr.writerow(self.weights[i])

    def readWeights(self,path = None):
        if path == None:
            with open('DynamicController/weightsDynamicController' + self.id + '.csv') as csvfile:
                reader = csv.reader(csvfile)
                weightType = 0
                for row in reader:
                    self.weights[weightType] = [float(i) for i in row]
                    weightType +=1
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
        dcf.playerLogic(self)
        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                fireball.kill()
        if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()
        health_diff = self.health - self.opponent.health
            # If the dynamic controller fails to cause an overall increase of 100 health in the game choose different weights but don't penalize the current weights
        if self.total_time == 300:
            dcf.update_weights(self,False)
            self.total_time = 0
            # If combined health lost is greater than the update rate (100). Change the weights
        if self.health + self.opponent.health <= self.totalHealthBenchmark:
                # Calculate the health difference between the players for the training period
            self.benchmarkDifference = health_diff - self.benchmarkDifference
            self.totalHealthBenchmark -= 100
            self.total_time = 0
            dcf.update_weights(self,True)
