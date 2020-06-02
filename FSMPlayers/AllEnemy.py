import arcade
import math
from util import constants
from util.constants import ARROW_SPEED, MOVEMENT_SPEED


class Enemy(arcade.Sprite):
    def throwfire(self):
        fireball = constants.Fireball("images/fire.png", .1)
        fireball.center_x = self.center_x
        fireball.center_y = self.center_y
        fireball.start_x = self.center_x # for tracking 
        fireball.start_y = self.center_y # fireball distance
        fireball.angle = self.angle-90
        fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        
        self.fireball_list.append(fireball)

    def shootarrow(self):
        arrow = constants.Arrow("images/arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)

    def equipshield(self):
        self.set_texture(1)
        self.health += 50
        self.shield +=1

    def shortattack(self):
        knife = constants.Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)

    def update(self):
        self.curtime += 1 
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            if self.d <= 400:
                
                self.throwfire()
            
            elif self.d <=250 and self.knife_num == 0:
                
                self.shortattack()
            else:
            
                self.shootarrow()
            
            self.curtime = 0
        if self.health <=50 and self.shield < 1:
            self.equipshield()