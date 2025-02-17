import arcade
import math
import random
from util.constants import * 

class RangePlayer(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += PLAYER_HEALTH*.5
        self.shield +=1
    def shootarrow(self):
        arrow = Arrow("images/arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.start_x = self.center_x # for tracking 
        arrow.start_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)
        hit = HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        arrow.hit = hit
        self.hitbox_list.append(hit)

    def update(self):
        self.curtime += 1
        if len(self.opponent_hitbox_list) > 0:
            if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list):
                randmove_x = random.choices([1,-1])[0]
                randmove_y = random.choices([1,-1])[0]
                x_change = MOVEMENT_SPEED * randmove_x
                y_change = MOVEMENT_SPEED * randmove_y
            else:
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
        else:
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
        self.center_x += x_change
        self.center_y += y_change

            
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = -math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = -math.sin(self.angle)*MOVEMENT_SPEED
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            self.shootarrow()
            self.curtime = 0
        for arrow in self.arrow_list:
            if arrow.center_x>SCREEN_WIDTH + 10 or arrow.center_y>SCREEN_HEIGHT + 10 or arrow.center_x< -10 or arrow.center_y< -10 :
                arrow.hit.kill()
                arrow.kill()
        if self.health <= PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()