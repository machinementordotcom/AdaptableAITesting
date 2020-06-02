import arcade
import math
from util import constants
from util.constants import ARROW_SPEED, MOVEMENT_SPEED


class HumanPlayer(arcade.Sprite):
    # def moveW(self):
    #         self.center_y += MOVEMENT_SPEED
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
    # def update(self):
    #     for fireball in self.fireball_list:
    #         diff_x = fireball.start_x-fireball.center_x
    #         diff_y = fireball.start_y-fireball.center_y
    #         fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
    #         if fireball_dist>200:
    #             fireball.kill()
 