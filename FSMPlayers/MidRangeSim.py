
from math import cos, sin, degrees, radians, sqrt, atan2
from random import choices
from util.constants import *
from arcade import Sprite

class MidRangePlayer(Sprite):
    def check_for_collision(self,player,projectiles):
        for projectile in projectiles:
            start_x = projectile.center_x
            start_y = projectile.center_y
            if start_x - projectile.box <= player.center_x + player.box or start_x + projectile.box >= player.center_x - player.box and start_y + projectile.box <= player.center_y - player.box or start_y + projectile.box >= player.center_y - player.box:
                    return True
            while start_x > 0 and start_y > 0 and start_x < SCREEN_WIDTH and start_y < SCREEN_HEIGHT:
                start_x += projectile.vel*cos(angle)
                start_y += projectile.vel*sin(angle)
                if start_x - projectile.box <= player.center_x + player.box or start_x + projectile.box >= player.center_x - player.box and start_y + projectile.box <= player.center_y - player.box or start_y + projectile.box >= player.center_y - player.box:
                    return True
        return False
    def equipshield(self):
        self.health += PLAYER_HEALTH*.5
        self.shield +=1
    def throwfire(self):
        fireball = Fireball() #"images/fire.png", .1)
        fireball.center_x = self.center_x
        fireball.center_y = self.center_y
        fireball.start_x = self.center_x # for tracking 
        fireball.start_y = self.center_y # fireball distance
        fireball.angle = self.angle-90
        fireball.change_x = -ARROW_SPEED*sin(radians(self.angle))
        fireball.change_y = ARROW_SPEED*cos(radians(self.angle))
        fireball.vel = ARROW_SPEED
        fireball.box = BOX
        self.fireball_list.append(fireball)

        hit = HitBox() #"images/fire.png")
        hit._set_alpha(0)
        hit._set_height(sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -sin(radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + cos(radians(hit.angle)) * hit.height/2
        hit.vel = ARROW_SPEED
        hit.box = BOX

        fireball.hit = hit
        self.hitbox_list.append(hit)

    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.angle = degrees(atan2(y_diff,x_diff))-90
        self.d = sqrt(x_diff**2 +y_diff**2)
        if len(self.opponent_hitbox_list) > 0:
            if self.check_for_collision(self,self.opponent_hitbox_list) and self.health <PLAYER_HEALTH*.7:
                randmove_x = choices([1,-1])[0]
                randmove_y = choices([1,-1])[0]
                self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP) * randmove_x
                self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP) * randmove_y
            elif abs(y_diff) + abs(x_diff) != 0: 
                self.change_x = (x_diff)/(abs(y_diff) + abs(x_diff))
                self.change_y = (y_diff)/(abs(y_diff) + abs(x_diff))
                if self.d > 200:
                    self.center_x += self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    self.center_y += self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                else:
                    if abs(self.center_x - 0) > 5 and abs(SCREEN_WIDTH - self.center_x) > 5:
                        self.center_x += -self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if self.center_y > SCREEN_HEIGHT/2:
                            self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            self.center_y += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)

                    if abs(self.center_y - 0) > 5 and abs(SCREEN_HEIGHT - self.center_y) > 5:
                        self.center_y += -self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if self.center_x > SCREEN_WIDTH/2:
                            self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            self.center_x += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)
        else:
            if abs(y_diff) + abs(x_diff) != 0: 
                self.change_x = (x_diff)/(abs(y_diff) + abs(x_diff))
                self.change_y = (y_diff)/(abs(y_diff) + abs(x_diff))
                if self.d > 200:
                    self.center_x += self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    self.center_y += self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                else:
                    if abs(self.center_x - 0) > 5 and abs(SCREEN_WIDTH - self.center_x) > 5:
                        self.center_x += -self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if self.center_y > SCREEN_HEIGHT/2:
                            self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            self.center_y += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)

                    if abs(self.center_y - 0) > 5 and abs(SCREEN_HEIGHT - self.center_y) > 5:
                        self.center_y += -self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if self.center_x > SCREEN_WIDTH/2:
                            self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            self.center_x += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)
        
        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_y <= 0:
            self.center_y = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH
        if self.center_x <= 0:
            self.center_x = 0

        if self.curtime >=30:
            if self.d <= 300:
                self.throwfire()
            self.curtime = 0

        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                self.fireball_list.remove(fireball)
        if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
            self.equipshield()
