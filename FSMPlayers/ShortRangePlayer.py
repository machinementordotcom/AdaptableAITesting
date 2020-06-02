import arcade
import math
import random
from util import constants
from util.constants import MOVEMENT_SPEED, PLAYER_HEALTH\
    , ARROW_IMAGE_HEIGHT, SHORT_SPEED_HANDICAP


class ShortRangePlayer(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += PLAYER_HEALTH*.5
        self.shield +=1
        
    def shortattack(self):
        knife = constants.Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)

        hit = constants.HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(5)
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        
        knife.hit = hit
        # self.hitbox_list.append(hit)
    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        if len(self.opponent_hitbox_list) > 0:
            if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list) and self.health <PLAYER_HEALTH*.45:
                randmove_x = random.choices([1,-1])[0]
                randmove_y = random.choices([1,-1])[0]
                self.center_x += MOVEMENT_SPEED * randmove_x
                self.center_y += MOVEMENT_SPEED * randmove_y
            else:
                if x_diff > 0:
                    self.center_x += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                elif x_diff < 0:
                    self.center_x -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                if y_diff > 0:
                    self.center_y += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                elif y_diff < 0:
                    self.center_y -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
        else:
            if x_diff > 0:
                self.center_x += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
            elif x_diff < 0:
                self.center_x -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
            if y_diff > 0:
                self.center_y += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
            elif y_diff < 0:
                self.center_y -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)

        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            if self.d <= 50:
                self.shortattack()
            self.curtime = 0
        if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()
