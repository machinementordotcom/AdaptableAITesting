import math
import arcade
from util import constants
from util.constants import MOVEMENT_SPEED, PLAYER_HEALTH \
    , SHORT_SPEED_HANDICAP, SCREEN_WIDTH, SCREEN_HEIGHT, BOX

import random


class ShortRangePlayer(arcade.Sprite):
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

    def shortattack(self):
        knife = constants.Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        knife.box = BOX 
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)
        # self.hitbox_list.append(hit)

    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        if len(self.opponent_hitbox_list) > 0:
            if self.check_for_collision(self,self.opponent_hitbox_list) and self.health <PLAYER_HEALTH*.45:
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

        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_y <= 0:
            self.center_y = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH
        if self.center_x <= 0:
            self.center_x = 0

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
