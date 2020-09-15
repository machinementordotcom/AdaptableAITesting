
import omegaml as om
import sys
import csv 
import arcade
import numpy as np
from util.constants import *
import math
import random

class GENN(arcade.Sprite):

    def shootarrow(self):
      arrow = Arrow("images/arrow.png",.1)
      arrow.center_x = self.center_x
      arrow.center_y = self.center_y
      arrow.start_x = self.center_x # for tracking 
      arrow.start_y = self.center_y
      arrow.angle = self.angle-90
      arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
      arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
      arrow.vel = ARROW_SPEED
      arrow.box = BOX

      self.arrow_list.append(arrow)

      hit = HitBox("images/fire.png")
      hit._set_alpha(0)
      hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
      hit._set_width(ARROW_IMAGE_HEIGHT)
      hit.angle = self.angle
      hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
      hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
      hit.vel = ARROW_SPEED
      hit.box = BOX
      arrow.hit = hit
      self.hitbox_list.append(hit)
        
    def equipshield(self):
      self.health += PLAYER_HEALTH*.5
      self.shield +=1
        
    def throwfire(self):
      fireball = Fireball("images/fire.png", .1)
      fireball.center_x = self.center_x
      fireball.center_y = self.center_y
      fireball.start_x = self.center_x # for tracking 
      fireball.start_y = self.center_y # fireball distance
      fireball.angle = self.angle-90
      fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
      fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
      fireball.vel = ARROW_SPEED
      fireball.box = BOX
      self.fireball_list.append(fireball)
      hit = HitBox("images/fire.png")
      hit._set_alpha(0)
      hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
      hit._set_width(ARROW_IMAGE_HEIGHT)
      hit.angle = self.angle
      hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
      hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
      hit.vel = ARROW_SPEED
      hit.box = BOX
      fireball.hit = hit
      self.hitbox_list.append(hit)

    def shortattack(self):
      knife = Knife("images/knife.png",.1)
      knife.center_x = self.center_x
      knife.center_y = self.center_y
      knife.angle = self.angle-180
      knife.box = BOX 
      self.knife_num += 1 # prevents multiple knifes from being created
      self.knife_list.append(knife)

    def writeWeights(self):
      with open("GENN/weightsDynamicController" + self.id + "-" + str(self.conCurrentGameId) + ".csv", 'w') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for i in range(2):
            wr.writerow(self.weights[i])
            
    def readWeights(self,path = None):
     tempWeights = [[],[]] 
     if path == None:
         for i in range(self.conGames):
            with open('GENN/weightsDynamicController' + self.id + "-" + str(self.conCurrentGameId) + '.csv') as csvfile:
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
        if len(self.opponent_hitbox_list) >= 3:
            opp_proj_1_x = self.opponent_hitbox_list[0].center_x
            opp_proj_1_y = self.opponent_hitbox_list[0].center_y
            opp_proj_2_x = self.opponent_hitbox_list[1].center_x
            opp_proj_2_y = self.opponent_hitbox_list[1].center_y
            opp_proj_3_x = self.opponent_hitbox_list[2].center_x
            opp_proj_3_y = self.opponent_hitbox_list[2].center_y
        elif len(self.opponent_hitbox_list) == 2:
            opp_proj_1_x = self.opponent_hitbox_list[0].center_x
            opp_proj_1_y = self.opponent_hitbox_list[0].center_y
            opp_proj_2_x = self.opponent_hitbox_list[1].center_x
            opp_proj_2_y = self.opponent_hitbox_list[1].center_y
            opp_proj_3_x = 0
            opp_proj_3_y = 0
        elif len(self.opponent_hitbox_list) == 1:
            opp_proj_1_x = self.opponent_hitbox_list[0].center_x
            opp_proj_1_y = self.opponent_hitbox_list[0].center_y
            opp_proj_2_x = 0
            opp_proj_2_y = 0
            opp_proj_3_x = 0
            opp_proj_3_y = 0
        else:
            opp_proj_1_x = 0
            opp_proj_1_y = 0
            opp_proj_2_x = 0
            opp_proj_2_y = 0
            opp_proj_3_x = 0
            opp_proj_3_y = 0
      
        inputs_raw = [[self.center_x,
                       self.center_y,
                       self.opponent.center_x,
                       self.opponent.center_y, # What??  Two entries for x, none for y.  Fixing now!
                       self.health,
                       self.opponent.health,
                       self.total_time,
                       self.shield,
                       self.opponent.shield,
                       self.curtime,
                       len(self.opponent_hitbox_list),
                       opp_proj_1_x,
                       opp_proj_1_y,
                       opp_proj_2_x,
                       opp_proj_2_y,
                       opp_proj_3_x, 
                       opp_proj_3_y]]
        
        inputs_scaled = [[self.center_x / 1000,
                       self.center_y / 1000,
                       self.opponent.center_x / 1000,
                       self.opponent.center_y / 1000, # What??  Two entries for x, none for y.  Fixing now!
                       self.health / 1000,
                       self.opponent.health / 1000,
                       self.total_time / 1000,
                       self.shield,
                       self.opponent.shield,
                       self.curtime / 3000,
                       len(self.opponent_hitbox_list) / 100,
                       opp_proj_1_x / 1000,
                       opp_proj_1_y / 1000,
                       opp_proj_2_x / 1000,
                       opp_proj_2_y / 1000,
                       opp_proj_3_x / 1000, 
                       opp_proj_3_y / 1000
                         ]]
         
#        print("inputs_scaled",inputs_scaled)
    
 
      
      ## NH added code to store model and require GPU for net creation
#      model_id = str(self)  ## This should happen outside and get passed in
#      om.models.put(self.model,model_id) ## This should only happen once for each model
#      model_id = str(self.process_id)
#      result = om.runtime.require('gpu').model(model_id).predict(np.asarray(inputs))
#      choices = result.get()
                
        import pandas as pd
        import time
        from sklearn.preprocessing import MinMaxScaler
        
        
#        scaler = MinMaxScaler(feature_range = (-1, 1))
#        inputs_array = np.asarray(inputs_raw).reshape([17,-1])  # NH - inputs were not shaped correctly for scaling
        
#        print("inputs_array",inputs_array)
#        inputs_scaled = scaler.fit_transform(inputs_array) # NH - inputs were not scaled at all
      
        
        inputs = np.asarray(inputs_scaled).reshape(-1,17)
       
        choices_raw = self.model.predict(inputs, verbose=0)
#        print("Choices - scaled predictions:",choices_raw[0][0],choices_raw[1][0])
        
        ## Separate move prediction and un-scale it
        
        choices1 = np.asarray(list(choices_raw[0][0])).reshape(2,-1)
        choices2 = np.asarray(list(choices_raw[1][0])).reshape(3,-1)
#        print("Choices reshaped",choices1,choices2)
        
        choices = [[choices1[0][0] * 1000,
                    choices1[1][0] * 1000,
                    choices2[0][0],
                    choices2[1][0],
                    choices2[2][0]
                   ]]
#        print(choices)
        
#        print(choices[0][0],choices[0][1],choices[0][2],choices[0][3],choices[0][4])
        
#        print("Choices unscaled",choices)
#        time.sleep(1)
        
#        choices = choices_unscaled.reshape(1,5)
#        print("Choices are",choices)
#        time.sleep(1)
        
        # Prepare model output for stream
        choices_a = np.asarray(choices).reshape(-1)
#        print("Choices:",choices_a)

        #Print The Log Result
        io_stream = dict(
            self_id = [str(self)],
            center_x = [self.center_x],
            center_y = [self.center_y],
            opponent_center_x = [self.opponent.center_x],
            opponent_center_y = [self.opponent.center_y],
            player_health = [self.health],
            opponent_health = [self.opponent.health],
            total_time = [self.total_time],
            player_shield = [self.shield],
            opponent_shield = [self.opponent.shield],
            curtime = [self.curtime],
            opponent_hitbox = [len(self.opponent_hitbox_list)],
            proj_1_x = [opp_proj_1_x],
            proj_1_y = [opp_proj_1_y],
            proj_2_x = [opp_proj_2_x],
            proj_2_y = [opp_proj_2_y],
            proj_3_x = [opp_proj_3_x], 
            proj_3_y = [opp_proj_3_y],
            predict1 = [choices[0][0]],
            predict2 = [choices[0][1]],
            predict3 = [choices[0][2]],
            predict4 = [choices[0][3]],
            predict5 = [choices[0][4]]
                                 )
#        print(io_stream)        
        
#        print("\nModel input:\n\n:",inputs,"\n\nModel predicts:\n\n",np.array(choices))

        if self.curtime % 1 == 0:  #enabled for every move
            dataFrame = pd.DataFrame(io_stream)
            file_name = "io_stream.csv"
   
            if os.path.exists(file_name):
                dataFrame.to_csv(file_name, mode='a', header=False, index=False)

            else:
                dataFrame.to_csv(file_name, mode='w', header=True, index=False)  

        
#        model = om.runtime.model(self)
#        choices = model.predict(np.asarray(inputs)).get()
        
        ## The coordinate predictions made in the first two fields 
        # are multiplied by static speed and the player moves there
        self.center_x += MOVEMENT_SPEED * choices[0][0] #[0]
        self.center_y += MOVEMENT_SPEED * choices[0][1] #[0]

        ## Adjustments are made in case player runs off edge of screen
        if self.center_y >= SCREEN_HEIGHT -20:
            self.center_y = SCREEN_HEIGHT -20
        if self.center_y <= 0 + 20:
            self.center_y = 0 + 20
        if self.center_x >= SCREEN_WIDTH -20:
            self.center_x = SCREEN_WIDTH -20
        if self.center_x <= 0 + 20:
            self.center_x = 0 + 20

        # Distance is measured between player and opponent
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        
        # Further adjustments are made for movement
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = -math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = -math.sin(self.angle)*MOVEMENT_SPEED
   
        """ ## The below section is entirely for trend reporting, which has been replaced

        ## If player is to the right of opponent AND predict x is negative
        ## and if player is above opponent AND predict y is negative ##
        ## OR if player is to the left of opponent and predict x is positive
        ## AND if player is above opponent and predict y is negative
        ## OR if player is to the left of opponent and predict x is positive
        ## AND if player is below opponent and predict y is positive
        ## OR if player is to the right of opponent and predict x is negative
        ## AND if player is below opponent and predict y is positive
 
        if self.center_x > self.opponent.center_x and choices[0][0] < 0 \
        and self.center_y > self.opponent.center_y and choices[0][1] < 0 \
        or self.center_x < self.opponent.center_x and choices[0][0] > 0 \
        and self.center_y > self.opponent.center_y and choices[1][0] < 0 \
        or self.center_x < self.opponent.center_x and choices[0][0] > 0 \
        and self.center_y < self.opponent.center_y and choices[1][0] > 0 \
        or self.center_x > self.opponent.center_x and choices[0][0] < 0 \
        and self.center_y < self.opponent.center_y and choices[1][0] > 0:
        ## In other words, if the prediction will move the player TOWARD the opponent,
        # then log the movement or "trend".  The rest of the expression completes
        # the log.
            self.trends['towardsOpponent'] += 1
            if self.lastMovement == "Away":
                self.trends['movementChanges'] +=1 
                self.currentTrend = 0
            else:
                self.currentTrend +=1 
                if self.currentTrend > self.trends['biggestTrend']:
                    self.trends['biggestTrend'] = self.currentTrend
            self.lastMovement = "Towards"
        else:
            self.trends['awayOpponent'] += 1
            if self.lastMovement == "Towards":
                self.trends['movementChanges'] +=1 
                self.currentTrend = 0
            else:
                self.currentTrend +=1 
                if self.currentTrend > self.trends['biggestTrend']:
                    self.trends['biggestTrend'] = self.currentTrend
            self.lastMovement = "away"
        """    
        ## NH - this entire section allowed for games to transpire 
        # even though no actual predictions were taking place.
        # The models were returning 1-1-1-1-1 on every single move
        # due to lack of variable scaling.  Even so, the code below
        # created random attacks on opponents which would succeed
        # randomly.
        
        ## First, the random moves loop applies to every move after 
        ## if self.curtime >= 30:
        
        ## Making a change here to use random moves ONLY within the first 30
        ## and use model predictions every other time.
        
        if self.curtime <= 30:
            
            ## If all three attack prediction variables are equal,
            # then choose an attack at random
            if choices[0][2] == choices[0][3] == choices[0][4]:
                attack = random.choices(['short','mid','range'])[0]
                if attack == 'short': 
                    self.shortattack()
                    self.trends['knife'] = self.trends['knife'] + 1
                elif attack == 'mid': 
                    self.throwfire()
                    self.trends['fire'] = self.trends['fire'] + 1    
                else: 
                    self.shootarrow()
                    self.trends['arrow'] = self.trends['arrow'] + 1
                    
        ## If it's still within 30 moves of the game's beginning, then
        # if var1 is greater than var2 and var1 is greater than var3,
        # attack short (knife)
        elif choices[0][2] > choices[0][3] and choices[0][2] > choices[0][4]:
            self.shortattack()
        
        ## else if var 2 is greater than var 3, attack mid (fireball)
        elif choices[0][3] > choices[0][4]:
            self.throwfire()
            
        ## otherwise shoot an arrow and reset the game_move variable to zero    
        else:
            self.shootarrow()
 #           self.game_move = 0
            
        for arrow in self.arrow_list:
            if arrow.center_x>SCREEN_WIDTH + 10 \
            or arrow.center_y>SCREEN_HEIGHT + 10 \
            or arrow.center_x< -10 or arrow.center_y< -10 :
                arrow.hit.kill()
                arrow.kill()
            for fireball in self.fireball_list:
                diff_x = fireball.start_x-fireball.center_x
                diff_y = fireball.start_y-fireball.center_y
                fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
                if fireball_dist>200:
                    self.fireball_list.remove(fireball)

        if self.health <= PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()

