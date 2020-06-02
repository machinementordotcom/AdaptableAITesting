import math
import random
import arcade
from util import constants
from util.constants import ARROW_SPEED, \
    MOVEMENT_SPEED, PLAYER_HEALTH, SCREEN_WIDTH, \
    SCREEN_HEIGHT, ARROW_IMAGE_HEIGHT, BOX


class RangePlayer(arcade.Sprite):
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

    def shootarrow(self):
        arrow = constants.Arrow("images/arrow.png",.1)
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

        hit = constants.HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        hit.vel = ARROW_SPEED
        hit.box = constants.BOX
        arrow.hit = hit
        self.hitbox_list.append(hit)

    def update(self):
        self.curtime += 1
        if len(self.opponent_hitbox_list) > 0:
            if self.check_for_collision(self,self.opponent_hitbox_list):
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

        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_y <= 0:
            self.center_y = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH
        if self.center_x <= 0:
            self.center_x = 0

            
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = -math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = -math.sin(self.angle)*MOVEMENT_SPEED
        if self.curtime >=30:
            self.shootarrow()
            self.curtime = 0
        for arrow in self.arrow_list:
            if arrow.center_x>SCREEN_WIDTH + 10 or arrow.center_y>SCREEN_HEIGHT + 10 or arrow.center_x< -10 or arrow.center_y< -10 :
                arrow.hit.kill()
                arrow.kill()
        if self.health <= PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()