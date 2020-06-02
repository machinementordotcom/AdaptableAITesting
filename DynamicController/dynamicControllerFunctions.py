import random
import re 
import math

import arcade

from util.constants import RANDOM_SEED, ARROW_SPEED, \
    SCREEN_WIDTH, SCREEN_HEIGHT, ARROW_IMAGE_HEIGHT, \
    MOVEMENT_SPEED
from util import constants


random.seed(RANDOM_SEED)


def excludeSums(nums,id):
    if (id > len(nums)): raise Exception("problem with summing function")
    return sum(nums[0:id]+nums[id+1:])

def shortattack(self,angle_adjustment):
        knife = constants.Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180 + angle_adjustment
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)

def throwfireball(self,angle_adjustment):
    fireball = constants.Fireball("images/fire.png", .1)
    fireball.center_x = self.center_x
    fireball.center_y = self.center_y
    fireball.start_x = self.center_x 
    fireball.start_y = self.center_y 
    fireball.angle = self.angle-90 + angle_adjustment
    fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
    fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
    self.fireball_list.append(fireball)
    hit = constants.HitBox("images/fire.png")
    hit._set_alpha(0)
    hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
    hit._set_width(ARROW_IMAGE_HEIGHT)
    hit.angle = self.angle
    hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
    hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
    fireball.hit = hit
    self.hitbox_list.append(hit)

def shootarrow(self,angle_adjustment):
    arrow = constants.Arrow("images/arrow.png",.1)
    arrow.center_x = self.center_x
    arrow.center_y = self.center_y
    arrow.start_x = self.center_x 
    arrow.start_y = self.center_y
    arrow.angle = self.angle-90 + angle_adjustment
    arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
    arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
    self.arrow_list.append(arrow)
    hit = constants.HitBox("images/fire.png")
    hit._set_alpha(0)
    hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
    hit._set_width(ARROW_IMAGE_HEIGHT)
    hit.angle = self.angle
    hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
    hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
    arrow.hit = hit
    self.hitbox_list.append(hit)

def moveTowards(self):
    y_change = 0
    x_change = 0
    if self.opponent.center_x - self.center_x < 0:
        x_change += MOVEMENT_SPEED
    else:
        x_change -= MOVEMENT_SPEED
    if self.opponent.center_y - self.center_y < 0:
        y_change += MOVEMENT_SPEED
    else:
        y_change -= MOVEMENT_SPEED

def moveAway(self):
    x_diff = self.opponent.center_x - self.center_x
    y_diff = self.opponent.center_y - self.center_y
    if x_diff > 0:
        self.center_x += MOVEMENT_SPEED 
    elif x_diff < 0:
        self.center_x -= MOVEMENT_SPEED 
    if y_diff > 0:
        self.center_y += MOVEMENT_SPEED 
    elif y_diff < 0:
        self.center_y -= MOVEMENT_SPEED

def chooseType(sampleWeights):
    rules = ["rule" + str(i) for i in range(1,len(sampleWeights)+1)]
    return random.choices(population = rules,weights = sampleWeights, k = 1)[0]

def chooseWeight(self):
    if self.adjusting == 'both':
        self.shootRule = chooseType(self.weights[0])
        self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
        self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
        self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
        self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
        self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]

    elif self.adjusting == 'shoot':
        self.shootRule = "rule" + str(self.adjustingWeight + 1)
        self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
        self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
        self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
        self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
        self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]

    elif self.adjusting == 'move':
        self.shootRule = chooseType(self.weights[0])
        if 0 <= self.adjustingWeight <= 6:
            temp = [50,100,150,200,250,300,350]
            self.move_away_choice = temp[self.adjustingWeight]#random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
            self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
            self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
            self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
            self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]
        elif 7 <= self.adjustingWeight <= 13:
            temp = [50,100,150,200,250,300,350]
            self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
            self.move_toward_choice = temp[self.adjustingWeight - 7]#random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
            self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
            self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
            self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]
        elif 14 <= self.adjustingWeight <= 15:
            temp = ["away","toward"]
            self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
            self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
            self.move_direction_choice = temp[self.adjustingWeight - 14]#random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
            self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
            self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]
        elif 16 <= self.adjustingWeight <= 17:
            temp = [-1,1]
            self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
            self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
            self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
            self.x_dodge_direction_choice = temp[self.adjustingWeight - 16]#random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
            self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]
        elif 18 <= self.adjustingWeight <= 19:
            temp = [-1,1]
            self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
            self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
            self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
            self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
            self.y_dodge_direction_choice = temp[self.adjustingWeight - 18]#random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]
    elif self.adjusting == None:
        self.shootRule = chooseType(self.weights[0])
        self.move_away_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][0:7], k = 1)[0]
        self.move_toward_choice = random.choices(population = [50,100,150,200,250,300,350],weights = self.weights[1][7:14], k = 1)[0]
        self.move_direction_choice = random.choices(population = ["away","toward"],weights = self.weights[1][14:16], k = 1)[0]
        self.x_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][16:18], k = 1)[0]
        self.y_dodge_direction_choice = random.choices(population = [-1,1],weights = self.weights[1][18:20], k = 1)[0]

    else:
        raise Exception("Error with the weights you're adjusting dynamicControllerFunctions.py line 140")

def playerLogic(self):
    # SHOOTING LOGIC 
        # Shooting Angle rules 
    if self.curtime >= 30:
        self.curtime = 0
        if self.shootRule == 'rule1':shootarrow(self,1)
        elif self.shootRule == 'rule2':shootarrow(self,2)
        elif self.shootRule == 'rule3':shootarrow(self,3)
        elif self.shootRule == 'rule4':shootarrow(self,-1)
        elif self.shootRule == 'rule5':shootarrow(self,-2)
        elif self.shootRule == 'rule6':shootarrow(self,-3)
        elif self.shootRule == 'rule7':shootarrow(self,0)
        elif self.shootRule == 'rule8':throwfireball(self,1)
        elif self.shootRule == 'rule9':throwfireball(self,2)
        elif self.shootRule == 'rule10':throwfireball(self,3)
        elif self.shootRule == 'rule11':throwfireball(self,-1)
        elif self.shootRule == 'rule12':throwfireball(self,-2)
        elif self.shootRule == 'rule13':throwfireball(self,-3)
        elif self.shootRule == 'rule14':throwfireball(self,0)
        elif self.shootRule == 'rule15':shortattack(self,1)
        elif self.shootRule == 'rule16':shortattack(self,2)
        elif self.shootRule == 'rule17':shortattack(self,3)
        elif self.shootRule == 'rule18':shortattack(self,-1)
        elif self.shootRule == 'rule19':shortattack(self,-2)
        elif self.shootRule == 'rule20':shortattack(self,-3)
        elif self.shootRule == 'rule21':shortattack(self,0)

    ### MOVEMENT LOGIC
    if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list):
        self.center_x += self.x_dodge_direction_choice * MOVEMENT_SPEED
        self.center_y += self.y_dodge_direction_choice * MOVEMENT_SPEED
    elif self.move_direction_choice == "away":
        if self.d < self.move_away_choice:
            moveAway(self)
    elif self.move_direction_choice == "toward":
        if self.d > self.move_toward_choice:
            moveTowards(self)

def changeWeights(self,adjusting,aW):
    learning_rate = 0.1
    v = 1.1 * (1 + learning_rate * abs(self.benchmarkDifference/100))
    if self.benchmarkDifference < 0:
        v = 1/v
    elif self.benchmarkDifference == 0:
        v = 1
    health_diff = self.health - self.opponent.health
    if adjusting is None:
        pass
    elif adjusting == 'shoot': 
        weightClass = 0
        weightGroup = self.weights[weightClass]
        small = 0
        big = 20
    elif adjusting == 'move': 
        weightClass = 1
        if  0 <= aW <= 6:
            weightGroup = self.weights[weightClass][0:7]
            small = 0 
            big = 6
        elif  7 <= aW <= 13:
            weightGroup = self.weights[weightClass][7:14]
            small = 7 
            big = 13
        elif  14 <= aW <= 15:
            weightGroup = self.weights[weightClass][14:16]
            small = 14 
            big = 15
        elif  16 <= aW <= 17:
            weightGroup = self.weights[weightClass][16:18]
            small = 16 
            big = 17
        elif  18 <= aW <= 19:
            weightGroup = self.weights[weightClass][18:20]
            small = 18 
            big = 19
    if adjusting != None:
        self.weights[weightClass][aW] *= v  
            # if the weight has been adjusted to 1 or greater set it to .99 and give the other weights equal probabilities 
        if self.weights[weightClass][aW] >= 1:
            self.weights[weightClass][aW] = 0.99
            for i in range(small,big + 1):
                if i == aW:
                    self.weights[weightClass][aW] = .99
                else:
                    self.weights[weightClass][i] = (1 - .99) / (len(weightGroup) -1)
                # if the weight is less than 1 increase the weight and adjust other weights accordingly
        else:
            w = (1 - self.weights[weightClass][aW]) / excludeSums(weightGroup,aW - small)
            for i in range(small,big + 1):
                if i == aW:
                    pass
                else:
                    self.weights[weightClass][i] *= w  

def update_weights(self,ind):
    if ind:
        self.writeWeights()
        if self.adjusting == 'both':
            changeWeights(self,'shoot',int(re.findall(r'\d+',self.shootRule)[0]) - 1)
            changeWeights(self,'move',[50,100,150,200,250,300,350].index(self.move_away_choice))
            changeWeights(self,'move',[50,100,150,200,250,300,350].index(self.move_toward_choice) + 7)
            changeWeights(self,'move',["away","toward"].index(self.move_direction_choice) + 14)
            changeWeights(self,'move',[-1,1].index(self.x_dodge_direction_choice) + 16)
            changeWeights(self,'move',[-1,1].index(self.y_dodge_direction_choice) + 18)
        elif self.adjusting is not None:
            changeWeights(self,self.adjusting,self.adjustingWeight)
    chooseWeight(self)

