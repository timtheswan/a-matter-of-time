import pygame
from pygame.sprite import Sprite
from pygame.locals import *
import os,sys
import time
import random

random.seed()

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1368,800)) #screen = pygame.display.set_mode((1368,800),pygame.FULLSCREEN)



def text_box(text,top = False):
    skip = False
    if not top:
        y = 550
    else:
        y = 150
    starty =  y
    pause = 4000
    dia = ""
    extra = ""
    textfont = pygame.font.Font(pygame.font.get_default_font(), 50)
    for x in text:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if mouse[0] in range(0,1407) and mouse[1] in range(0,799):
                    skip = True
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                skip = True
            if event.type == QUIT:
                pygame.quit()
                quit()
        if x == "$":
            extra = dia
            dia = ""
            starty += 80
            new_words = textfont.render(extra,True, (0,0,0))
        else:
            dia = dia + x
            words = textfont.render(dia,True, (0,0,0))
        if not top:
            screen.fill((0,0,0),(10,510,1388,280))
            screen.fill((255,255,255),(20,520,1368,260))
            if y == starty:
                screen.blit(words, (50,starty))
            else:
                screen.blit(new_words, (50,y))
                screen.blit(words, (50,starty))
        else:
            screen.fill((0, 0, 0), (-490, 90, 1388, 280))
            screen.fill((255, 255, 255), (-480, 80, 1368, 260))
            if y == starty:
                screen.blit(words, (50, starty))
            else:
                screen.blit(new_words, (50, y))
                screen.blit(words, (50, starty))
        pygame.display.flip()
        clock.tick(60)
        if not skip:
            time.sleep(0.05)
    while True:
        ms = clock.tick(60)
        pause = pause - ms
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if mouse[0] in range(0,1407) and mouse[1] in range(0,799):
                    return
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                return
            if event.type == QUIT:
                pygame.quit()
                quit()
        if pause < 0:
            return


class Piece():

    def __init__(self, image, position, platform=False, wall=False):
        self.image = image
        self.position = position
        self.platform = platform
        self.wall = wall

class Button(Piece):

    def __init__(self,image,point,destination,action):
        Piece.__init__(self,image,point)
        self.point = point
        self.destination = destination
        if (self.destination[0] +30) < 400:
            if(self.destination[1] +20) < 200:
                self.dest = ((destination[0]*32)-(22*32),(destination[1]*32)-(13*32))
            else:
                self.dest = ((destination[0] * 32) - (22 * 32), 170*32)
        elif(self.destination[1] +20) < 200:
            self.dest = (348*32,(destination[1]*32)-(13*32))
        else:
            self.dest = (348*32, 170*32)


        self.action = action

    def perform(self,game_map,main_cam):
        for x in self.action:
            print(x[0])
            if x[0] == 1:
                print("oops")
                for y in range(x[1]):
                    if self.destination[0] % 2 == 0 and (self.destination[1]-y) % 2 == 0:
                        game_map[self.destination[0]][self.destination[1]-y] = Piece(BTL, (self.destination[0], self.destination[1]-y))
                    elif self.destination[0] % 2 == 1 and (self.destination[1]-y) % 2 == 0:
                        game_map[self.destination[0]][self.destination[1]-y] = Piece(BTR, (self.destination[0], self.destination[1]-y))
                    elif self.destination[0] % 2 == 0 and (self.destination[1]-y) % 2 == 1:
                        game_map[self.destination[0]][self.destination[1]-y] = Piece(BBL, (self.destination[0], self.destination[1]-y))
                    elif self.destination[0] % 2 == 1 and (self.destination[1]-y) % 2 == 1:
                        game_map[self.destination[0]][self.destination[1]-y] = Piece(BBR, (self.destination[0], self.destination[1]-y))
                x[0] = 0
                if x[2] == 0:
                    pause = 2000
                    while True:
                        ms = clock.tick(60)
                        pause = pause - ms
                        if pause < 1400:
                            for i in range(44):
                                for j in range(26):
                                    offsetx = main_cam.position[0] % 32
                                    offsety = main_cam.position[1] % 32
                                    screen.blit(game_map[int(main_cam.position[0] // 32) + i][
                                                    int(main_cam.position[1] // 32) + j].image,
                                                ((i * 32) - offsetx, (j * 32) - offsety))
                            pygame.display.flip()
                        if pause < 0:
                            break
                    return
                self.destination = x[2]
            elif x[0] == 0:
                print("oops")
                for y in range(x[1]):
                    if self.destination[0] % 2 == 0 and (self.destination[1] - y) % 2 == 0:
                        game_map[self.destination[0]][self.destination[1] - y] = Piece(texture0, (
                        self.destination[0], self.destination[1] - y),True,True)
                    elif self.destination[0] % 2 == 1 and (self.destination[1] - y) % 2 == 0:
                        game_map[self.destination[0]][self.destination[1] - y] = Piece(texture0, (
                        self.destination[0], self.destination[1] - y),True,True)
                    elif self.destination[0] % 2 == 0 and (self.destination[1] - y) % 2 == 1:
                        game_map[self.destination[0]][self.destination[1] - y] = Piece(texture0, (
                        self.destination[0], self.destination[1] - y),True,True)
                    elif self.destination[0] % 2 == 1 and (self.destination[1] - y) % 2 == 1:
                        game_map[self.destination[0]][self.destination[1] - y] = Piece(texture0, (
                        self.destination[0], self.destination[1] - y),True,True)
                x[0] = 1
                if x[2] == 0:
                    pause = 2000
                    while True:
                        ms = clock.tick(60)
                        pause = pause - ms
                        if pause < 1400:
                            for i in range(44):
                                for j in range(26):
                                    offsetx = main_cam.position[0] % 32
                                    offsety = main_cam.position[1] % 32
                                    screen.blit(game_map[int(main_cam.position[0] // 32) + i][
                                                    int(main_cam.position[1] // 32) + j].image,
                                                ((i * 32) - offsetx, (j * 32) - offsety))
                            pygame.display.flip()
                        if pause < 0:
                            break
                    return
                self.destination = x[2]
            print(x[0])
            if x[0] == 2:
                print("i'm here")
                for y in range(x[1]):
                    if (self.destination[0]+y) % 2 == 0 and self.destination[1] % 2 == 0:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(texture0, (
                        self.destination[0]+y, self.destination[1]),True,True)
                    elif (self.destination[0]+y) % 2 == 1 and self.destination[1] % 2 == 0:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(texture0, (
                        self.destination[0]+y, self.destination[1]),True,True)
                    elif (self.destination[0]+y) % 2 == 0 and self.destination[1] % 2 == 1:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(texture0, (
                        self.destination[0]+y, self.destination[1]),True,True)
                    elif (self.destination[0]+y) % 2 == 1 and self.destination[1] % 2 == 1:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(texture0, (
                        self.destination[0]+y, self.destination[1]),True,True)
                x[0] = 3
                if x[2] == 0:
                    pause = 2000
                    while True:
                        ms = clock.tick(60)
                        pause = pause - ms
                        if pause < 1400:
                            for i in range(44):
                                for j in range(26):
                                    offsetx = main_cam.position[0] % 32
                                    offsety = main_cam.position[1] % 32
                                    screen.blit(game_map[int(main_cam.position[0] // 32) + i][
                                                    int(main_cam.position[1] // 32) + j].image,
                                                ((i * 32) - offsetx, (j * 32) - offsety))
                            pygame.display.flip()
                        if pause < 0:
                            break
                    return
                self.destination = x[2]
            elif x[0] == 3:
                print("oops")
                for y in range(x[1]):
                    if (self.destination[0]+y) % 2 == 0 and self.destination[1] % 2 == 0:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(BTL, (
                        self.destination[0]+y, self.destination[1]))
                    elif (self.destination[0]+y) % 2 == 1 and self.destination[1] % 2 == 0:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(BTR, (
                        self.destination[0]+y, self.destination[1]))
                    elif (self.destination[0]+y) % 2 == 0 and self.destination[1] % 2 == 1:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(BBL, (
                        self.destination[0]+y, self.destination[1]))
                    elif (self.destination[0]+y) % 2 == 1 and self.destination[1] % 2 == 1:
                        game_map[self.destination[0]+y][self.destination[1]] = Piece(BBR, (
                        self.destination[0]+y, self.destination[1]))
                x[0] = 2
                if x[2] == 0:
                    pause = 2000
                    while True:
                        ms = clock.tick(60)
                        pause = pause - ms
                        if pause < 1400:
                            for i in range(44):
                                for j in range(26):
                                    offsetx = main_cam.position[0] % 32
                                    offsety = main_cam.position[1] % 32
                                    screen.blit(game_map[int(main_cam.position[0] // 32) + i][
                                                    int(main_cam.position[1] // 32) + j].image,
                                                ((i * 32) - offsetx, (j * 32) - offsety))
                            pygame.display.flip()
                        if pause < 0:
                            break
                    return
                self.destination = x[2]
        pause = 2000
        while True:
            ms = clock.tick(60)
            pause = pause - ms
            if pause < 0:
                break
class Camera():
    
    def __init__(self,position):
        self.position = list(position)
        self.prior = position
        self.target = 0
        self.camera_lock = True
        self.arrived = False

    def move_cam(self,destination,player):
        self.prior = (self.position[0],self.position[1])
        self.target = destination
        self.camera_lock = False
        player.pause = True

    def to_movement(self,button,game_map):
        slicex = (self.target[0] - self.prior[0])/32
        slicey = (self.target[1] - self.prior[1])/32
        if not(self.target[0] == self.position[0] and self.target[1] == self.position[1]):
            self.position[0] += slicex
            self.position[1]+= slicey
        else:
            self.arrived = True
            button.perform(game_map,self)
        return game_map

    def from_movement(self,player):
        slicex = (self.prior[0] - self.target[0]) / 32
        slicey = (self.prior[1] - self.target[1]) / 32
        print(self.prior)
        print(self.position)
        if not (self.prior[0] == self.position[0] and self.prior[1] == self.position[1]):
            self.position[0] += slicex
            self.position[1] += slicey
        else:
            self.arrived = False
            self.camera_lock = True
            player.pause = False


class Entity(Sprite):

    def __init__(self, position):
        Sprite.__init__(self)
        self.position = position
        self.positionx = position[0]
        self.positiony = position[1]
        self.global_positionx = position[0]
        self.global_positiony = position[1]
        self.velocityx = 0
        self.velocityy = 0
        self.origin = (self.positionx + 64, self.positiony + 64)
        self.jump_value = False
        self.dead = False
        self.pause = False
        self.rewind = False
        self.rewind_tape = []
        self.facing = "right"


    def check_map(self,game_map,camera,checkTouching):
        # print(self.global_positionx,self.global_positiony)
        self.origin = (self.global_positionx + 64, self.global_positiony + 64)
        centerx = int(self.origin[0] // 32) - 2
        centery = int(self.origin[1] // 32)

        touchingWall = False

        changePos = False

        if self.jump_value:
            if game_map[centerx][centery].platform or game_map[centerx - 1][centery].platform:
                self.velocityy = -30

        try:
            if not checkTouching:
                if centerx < 0 or centery < 0:
                    raise Exception("Negative index")
                if game_map[centerx][centery].platform:
                    if self.velocityy > 0:
                        self.velocityy = 0
                        self.global_positiony = (centery - 2) * 32 + 6
                        self.positiony = self.global_positiony - camera.position[1]
                        changePos = True
                else:
                    if not (game_map[centerx - 1][centery].platform or game_map[centerx][centery].platform):
                        self.velocityy += 2
                if game_map[centerx][centery - 4].platform or game_map[centerx - 1][centery - 4].platform or \
                        game_map[centerx][centery - 4].platform:
                    if self.velocityy < 0:
                        self.velocityy = 0
                        # self.global_positiony = (centery - 2) * 32 + 6
                        # self.positiony = self.global_positiony - camera.position[1]
            if game_map[centerx - 2][centery - 1].wall or game_map[centerx-2][centery - 2].wall or game_map[centerx - 2][centery - 4].wall:
                if checkTouching:
                    touchingWall = True
                else:
                    if self.velocityx < 0:
                        self.velocityx = 0

                        self.global_positionx = ((centerx) * 32)
                        self.positionx = self.global_positionx - camera.position[0] - 6
                        changePos = True
            if game_map[centerx + 1][centery-1].wall or game_map[centerx + 1][centery - 2].wall or game_map[centerx + 1][centery - 4].wall:
                if checkTouching:
                    touchingWall = True
                else:
                    if self.velocityx > 0:
                        self.velocityx = 0
                        self.global_positionx = (centerx) * 32
                        self.positionx = self.global_positionx - camera.position[0] + 18
                        changePos = True
            if checkTouching:
                return touchingWall
        except:
            self.dead = True
        return changePos

class Player(Entity):

    def __init__(self, position):
        Entity.__init__(self,position)
        self.interact = False

        self.cycle = 0
        self.images_runL = []
        self.images_runL.append(pygame.image.load("albertL0.png"))
        self.images_runL.append(pygame.image.load("albertL1.png"))
        self.images_runL.append(pygame.image.load("albertL2.png"))

        self.images_runR = []
        self.images_runR.append(pygame.image.load("albertR0.png"))
        self.images_runR.append(pygame.image.load("albertR1.png"))
        self.images_runR.append(pygame.image.load("albertR2.png"))

        self.Ridle = pygame.image.load("albertRIdle.png")
        self.Lidle = pygame.image.load("albertLIdle.png")


        self.image = pygame.image.load("albertRIdle.png")
        self.right = pygame.image.load("Static_Main_RightB.png")
        self.left = pygame.image.load("Static_Main_LeftC.png")
        self.rect = self.image.get_rect()
        self.fastforward = False
        self.left_move = False
        self.right_move = False
        self.rect.center = position
        self.button = 0
        self.timer = 1200
        self.FDialog = True
        self.SDialog = True
        self.win = False

    def animate(self):

        self.cycle+=1
        if self.cycle==15:
            self.cycle=0

        if self.cycle%5==0:
            print("Animate!", self.cycle)
            if self.facing=="left":
                self.image = self.images_runL[self.cycle//5]
            elif self.facing=="right":
                self.image = self.images_runR[self.cycle//5]


    def testDeathPrelim(self):
        # if logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]=='p':

        for i in logical_map[self.global_positiony // 32 - 5:self.global_positiony // 32 + 2]:
            if 'b' in i[self.global_positionx // 32 - 2:self.global_positionx // 32 + 2]:
                return True
        return False

    def testAllTouching(self,enemies,buttons,door,camera):
        if not self.fastforward:
            for i in enemies:
                if i.rect.collidepoint(self.positionx,self.positiony) or i.rect.collidepoint(self.positionx,self.positiony+64):
                    self.dead = True
                    break
        if self.interact:
            for x in buttons:
                point = (x.point[0]-camera.position[0]-32,x.point[1]-camera.position[1])
                if self.rect.collidepoint(point[0],point[1]):
                    camera.move_cam(x.dest,self)
                    for enemy in enemies:
                        enemy.pause = True
                    self.button = x
                    self.interact = False

            point = (door.point[0]-camera.position[0]-32,door.point[1]-camera.position[1])
            if self.rect.collidepoint(point[0],point[1]):
                self.dead = True
                self.win = True
                door.open()
    def Dialog(self,camera):
        if self.FDialog:
            Fpoint = (96*32,190*32)
            Fpoint = (Fpoint[0] - camera.position[0], Fpoint[1] - camera.position[1])
            if self.rect.collidepoint(Fpoint[0], Fpoint[1]):
                File = open("Catch_Dialog.txt")
                for line in File:
                    text_box(line,True)
                File.close()
                self.FDialog = False
                self.right_move = False
                self.left_move = False
                self.jump_value = False
        if self.SDialog:
            Spoint = (450,640)
            Spoint = (Spoint[0] - camera.position[0], Spoint[1] - camera.position[1])
            if self.rect.collidepoint(Spoint[0], Spoint[1]):
                File = open("At_Start_Dialog.txt")
                for line in File:
                    text_box(line,True)
                File.close()
                self.SDialog = False
                self.right_move = False
                self.left_move = False
                self.jump_value = False

    def player_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.dead = True
            if event.type ==KEYDOWN and event.key == K_w:
                self.jump_value = True
            if event.type == KEYUP and event.key == K_w:
                self.jump_value = False
            if event.type ==KEYDOWN and event.key == K_d:
                self.right_move = True
            if event.type ==KEYUP and event.key == K_d:
                self.right_move = False
                self.image=self.Ridle

            if event.type ==KEYDOWN and event.key ==K_a:
                self.left_move = True

            if event.type == KEYUP and event.key == K_a:
                self.left_move = False
                self.image=self.Lidle

            if event.type == KEYDOWN and event.key == K_DOWN:
                 if self.timer > 0:
                   self.pause = True
                 else:
                   self.pause = False
            if event.type == KEYDOWN and event.key == K_UP:
                self.pause = False
            if event.type == KEYDOWN and event.key == K_LEFT:
                if self.timer > 0:
                  self.rewind = True
                else:
                  self.rewind = False

            if event.type == KEYUP and event.key == K_LEFT:
                self.rewind = False
            if event.type == KEYDOWN and event.key == K_RIGHT:
                if self.timer > 0:
                  self.fastforward = True
                else:
                  self.fastforward = False
            if event.type == KEYUP and event.key == K_RIGHT:
                self.fastforward = False
            if event.type == KEYDOWN and event.key == K_e:
                self.interact = True
            if event.type == KEYUP and event.key == K_e:
                self.interact = False

    def movement(self):
        self.velocityx = 0
        if self.right_move:
            if self.fastforward:
                self.velocityx += 25
            else:
                self.velocityx +=15
        if self.left_move:
            if self.fastforward:
                self.velocityx -= 25
            else:
                self.velocityx -=15
        if self.velocityx > 0:
            # self.image = self.Ridle
            self.facing = "right"
        elif self.velocityx < 0:
            # self.image = self.Lidle
            self.facing = "left"


    def update(self, game_map, camera):
        if not logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]=='p':
            print("Failure to Sync Logic Board (Check Player Update)",logical_map[int(self.global_positiony//32)][self.global_positionx//32])


        if self.right_move or self.left_move:
            self.animate()
        # print(temp==logical_map)
        # printMap()
        logical_map[int(self.global_positiony//32)][int(self.global_positiony//32)]='e'
        if not (self.pause or self.rewind):


            if not self.check_map(game_map,camera,False):

                if self.velocityy > 26:
                    self.velocityy = 26
                self.global_positiony += self.velocityy
                self.global_positionx += self.velocityx
                self.positionx = self.global_positionx - camera.position[0]
                self.positiony = self.global_positiony - camera.position[1]
            else:
                if self.velocityy > 26:
                    self.velocityy = 26
                self.global_positiony += self.velocityy
                self.global_positionx += self.velocityx
                self.positionx += self.velocityx
                self.positiony += self.velocityy


            if self.positionx > 1000:
                camera.position[0] += self.positionx - 1000
                self.positionx = 1000
            elif self.positionx < 400:
                camera.position[0] += self.positionx - 400
                self.positionx = 400
            if self.positiony > 600:
                camera.position[1] += self.positiony - 600
                self.positiony = 600
            elif self.positiony < 200:
                camera.position[1] += self.positiony - 200
                self.positiony = 200

            self.position = (self.positionx, self.positiony)
            self.rewind_tape.append(((self.global_positionx, self.global_positiony), self.position))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if self.timer <= 1198 and not self.fastforward:
                self.timer += 2
            elif self.fastforward:
                self.timer -= 10

        elif self.rewind and not self.pause:
            try:
                temp_position, self.position = self.rewind_tape.pop()
                self.global_positionx = temp_position[0]
                self.global_positiony = temp_position[1]
                camera.position[0] = self.global_positionx - self.position[0]
                camera.position[1] = self.global_positiony - self.position[1]
                self.positionx = self.position[0]
                self.positiony = self.position[1]
                self.rect = self.image.get_rect()
                self.rect.center = self.position
            except:
                pass
            self.timer -= 5
        elif self.pause:
            self.timer -= 1
        if self.timer <= 0:
            self.pause = False
            self.rewind = False
            self.fastforward = False
        if not camera.camera_lock:
            self.positionx = self.global_positionx - camera.position[0]
            self.positiony = self.global_positiony - camera.position[1]
            self.position = (self.positionx, self.positiony)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if not camera.arrived:
                camera.to_movement(self.button,game_map)
            else:
                camera.from_movement(self)
            if self.timer <= 1197:
                self.timer += 3

        logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]='p'
        # print("Ey, I Ran")

class Enemy(Entity):

    def __init__(self,position,type):
        Entity.__init__(self,position)
        if type == "robot":
            self.R = pygame.image.load("badGuy1.png")
            self.L = pygame.image.load("badGuy2.png")
            self.speed = 12

        elif type == "agent":
            self.R = pygame.image.load("secretAgentR.png")
            self.L = pygame.image.load("secretAgentL.png")
            self.speed = 2

        if type=="square":
            self.R = pygame.image.load("square2.png")
            self.L = pygame.image.load("square2.png")


        self.image = self.R

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.origin = (self.positionx+64,self.positiony+64)
        self.type=type
        self.queue=[["right",1]]
        self.chasing = False


    def update(self, game_map, camera, player):
        if not logical_map[int(self.global_positiony // 32)][int(self.global_positionx // 32)] == 'b':
            print("Failure to Sync Logic Board (Check Player Update)",
                  logical_map[int(self.global_positiony // 32)][self.global_positionx // 32])

        self.rewind = player.rewind
        logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]='e'
        self.lineOfSight()
        if camera.camera_lock:
            self.pause = False
        if not (self.pause or self.rewind):

            self.check_map(game_map,camera,False)
            self.move(camera, game_map)
            if self.velocityy >= 26:
                self.velocityy = 26
            self.global_positionx += self.velocityx
            self.global_positiony += self.velocityy
            self.positionx = self.global_positionx - camera.position[0]
            self.positiony = self.global_positiony - camera.position[1]
            self.position = (self.positionx, self.positiony)
            self.rewind_tape.append((self.global_positionx,self.global_positiony))
            self.rect = self.image.get_rect()
            self.rect.center = self.position

        elif self.rewind and not self.pause:
            try:
                self.global_positionx,self.global_positiony = self.rewind_tape.pop()
                self.positionx = self.global_positionx - camera.position[0]
                self.positiony = self.global_positiony - camera.position[1]
                self.position = (self.positionx, self.positiony)
                self.rect = self.image.get_rect()
                self.rect.center = self.position
            except:
                pass
        elif self.pause:
            self.positionx = self.global_positionx - camera.position[0]
            self.positiony = self.global_positiony - camera.position[1]
            self.position = (self.positionx, self.positiony)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
        logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]='b'


    def move(self, camera, game_map):

        logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]='e'
        if self.chasing:
            if self.facing=="right":
                self.velocityx=self.speed*2
            else:
                self.velocityx=-1*self.speed*2
        else:
            if self.queue[0][1]==1:
                self.queue.pop(0)

            if len(self.queue)==0:
                self.queue.append(self.generateRandomMove())

            if self.check_map(game_map,camera,True):

                if self.queue[0][0]=="right":
                    self.queue[0][0]="left"
                    self.global_positionx-=64
                    self.velocityx=self.speed*-1
                elif self.queue[0][0]=="left":
                    self.queue[0][0]="right"
                    self.global_positionx+=64
                    self.velocityx=self.speed
            if self.queue[0][0] == "right":
                self.facing="right"
                self.image=self.R
                self.velocityx = self.speed

            elif self.queue[0][0]== "left":
                self.facing="left"
                self.image=self.L
                self.velocityx = -1*self.speed

            self.queue[0][1]-=1

        logical_map[int(self.global_positiony//32)][int(self.global_positionx//32)]='b'



    def generateRandomMove(self):

        choose = random.randint(1,2)

        if choose==1:
            return ["right",random.randint(1,5)*60]

        if choose==2:
            return ["left",random.randint(1,5)*60]

        if choose==3:
            return ["idle",random.randint(1,5)*60]

    def lineOfSight(self):
        locY=self.global_positiony//32
        locX=self.global_positionx//32

        onLevel = False
        for i in logical_map[locY-2:locY+1]:
            if "p" in i:
                onLevel=True
        if onLevel:
            if self.look(locY,locX,self.facing,12):
                self.chasing=True
            else:
                self.chasing=False
                # if self.chasing:
                #     print("Success!")

    def look(self,locY,locX,facing,range):
        # print("Looking")
        if range==0:
            # print("Range, too far")
            return False

        if facing=="right":
            locX+=1

        else:
            locX-=1
        # if not 'g' in [logical_map[locY-3][locX],logical_map[locY-4][locX],logical_map[locY+5][locX]]:
        #     print("No Ground")
        #     return False
        if 'p' in [logical_map[locY][locX],logical_map[locY-1][locX],logical_map[locY+1][locX]]:
            return True

        return self.look(locY,locX,facing,range-1)

class door(Entity):

    def __init__(self,position):
        Entity.__init__(self, position)
        self.image=pygame.image.load("DoorClose.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.point = (position[0]+90,position[1])

    def update(self,camera):
        self.positionx = self.global_positionx - camera.position[0]
        self.positiony = self.global_positiony - camera.position[1]
        self.position = (self.positionx, self.positiony)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def open(self):
        self.image=pygame.image.load("DoorOpen.png")

def printMap():

    for i in logical_map[:50]:
        for j in i[:50]:
            print(j,' ',end='')
        print()
    print("----------------------------------------------------------------------------------------------")
    print()

def build_map():
    game_map = [[0]*200 for i in range(400)]
    for row in range(400):
        for col in range(200):
            logical_map[row].append('e')
        logical_map.append([])
    button_list =[]
    for row in range(400):
        for col in range(200):

            logical_map[int(row//32)][int(col//32)] = 'g'
            if 0 <= row <= 4 or 395 <= row <= 399:
                game_map[row][col] = Piece(texture0,(row,col),True,True)
            elif 0 <= col <= 4 or 195 <= col <= 199:
                game_map[row][col] = Piece(texture0,(row,col),True,True)
            elif 20 <= col <= 21 and 0 <= row <= 35:
                game_map[row][col] = Piece(texture2,(row,col),True)
            elif 20 <= col <= 21 and 47 <= row <= 80:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif 5 <= col <= 20 and 61 <= row <= 62:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 35 <= col <= 37 and 0 <= row <= 72:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif 42 <= col <= 43 and 0 <= row <= 78:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif 30 <= col <= 31 and 43 <= row <= 48:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif 25 <= col <= 26 and 33 <= row <= 38:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif 22 <= col <= 194 and 79 <= row <= 80:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 5 <= col <= 186 and 89 <= row <= 90:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 5 <= col <= 194 and 149 <= row <= 150:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif col == 40 and row == 5:
                game_map[row][col] = Button(texture2, (((row+2)*32)+24, col*32),(61,19),[[1,6,(62,19)],[1,6,0]])
                button_list.append(game_map[row][col])
            elif col == 180 and row == 91:
                game_map[row][col] = Button(texture2, (((row+2)*32)+24, col*32),(110,194),[[0,4,0]])
                button_list.append(game_map[row][col])
            elif col == 192 and row == 126:
                game_map[row][col] = Button(texture2, (((row+2)*32)+24, col*32),(124,189),[[3,3,0]])
                button_list.append(game_map[row][col])
            elif col == 173 and row == 134:
                game_map[row][col] = Button(texture2, (((row+2)*32)+24, col*32),(80,174),[[2,10,(90,173)],[1,6,(89,173)],[1,6,(80,173)],[1,6,(79,173)],[1,6,0]])
                button_list.append(game_map[row][col])
            elif col == 185 and row == 70:
                game_map[row][col] = Button(texture2, (((row+2)*32)+24, col*32),(54,187),[[1,7,(53,187)],[1,7,(33,188)],[2,12,0]])
                button_list.append(game_map[row][col])
            elif col == 185 and row == 70:
                game_map[row][col] = Button(texture2, (((row + 2) * 32) + 24, col * 32), (54, 187),[[1, 7, (53, 187)], [1, 7, (33, 188)], [2, 12, 0]])
                button_list.append(game_map[row][col])
            elif  col == 194 and 94 <= row <= 100:
                game_map[row][col] = Piece(texture2, (row, col), True,True)
            elif  col == 193 and 95 <= row <= 100:
                game_map[row][col] = Piece(texture2, (row, col), True,True)
            elif  col == 192 and 96 <= row <= 100:
                game_map[row][col] = Piece(texture2, (row, col), True,True)
            elif  col == 191 and 97 <= row <= 100:
                game_map[row][col] = Piece(texture2, (row, col), True,True)
            elif  col == 190 and 98 <= row <= 110:
                game_map[row][col] = Piece(texture2, (row, col), True,True)
            elif 183 <= col <= 184 and 91 <= row <= 97:
                game_map[row][col] = Piece(texture2, (row, col), True)
            elif  174 <= col <= 175 and 91 <= row <= 100:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 176 and 99 <= row <= 103:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 177 and 102 <= row <= 105:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 178 and 104 <= row <= 107:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 179 and 106 <= row <= 109:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 180 and 108 <= row <= 111:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 181 and 110 <= row <= 113:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 182 and 112 <= row <= 115:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 183 and 114 <= row <= 117:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  184 <= col <= 190 and 116 <= row <= 119:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  189 <= col <= 190 and 119 <= row <= 123:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  col == 189 and 124 <= row <= 126:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  175 <= col <= 194 and 127 <= row <= 128:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif 150 <= col <= 170 and 127 <= row <= 128:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif  175 <= col <= 176 and 125 <= row <= 134:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  169 <= col <= 176 and 135 <= row <= 136:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  169 <= col <= 170 and 127 <= row <= 134:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  168 <= col <= 169 and 74 <= row <= 80:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif  168 <= col <= 190 and 72 <= row <= 73:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif 188 <= col <= 190 and  60 <= row <= 71:
                game_map[row][col] = Piece(texture0, (row, col), True,True)
            elif 188 <= col <= 190 and  44 <= row <= 54:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 182 <= col <= 190 and 59 <= row <= 60:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 181 <= col <= 182 and 47 <= row <= 60:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 182 <= col <= 190 and 46 <= row <= 47:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 182 <= col <= 190 and 53 <= row <= 54:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 188 <= col <= 190 and  27 <= row <= 39:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 182 <= col <= 190 and 19 <= row <= 20:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 181 <= col <= 182 and 19 <= row <= 27:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 182 <= col <= 190 and 26 <= row <= 27:
                game_map[row][col] = Piece(texture0, (row, col), True, True)
            elif 188 <= col <= 190 and 10 <= row <= 20:
                game_map[row][col] = Piece(texture0, (row, col), True, True)











            else:
                logical_map[int(row//32)][int(col//32)] = 'e'
                if row%2==0 and col%2==0:
                    game_map[row][col] = Piece(BTL, (row,col))
                elif row%2==0 and col%2==1:
                    game_map[row][col] = Piece(BBL, (row,col))
                elif row%2==1 and col%2==0:
                    game_map[row][col] = Piece(BTR, (row,col))
                elif row%2==1 and col%2==1:
                    game_map[row][col] = Piece(BBR, (row,col))



    return game_map,button_list

def cleanLogic():
    count=0
    for i in range(len(logical_map)):
        if "p" not in logical_map[i]:
            continue
        for jeff in range(len(logical_map[i])):
            if logical_map[i][jeff]=="p":
                count+=1
                logical_map[i][jeff]="e"
    # print("Count",count)
    logical_map[player.global_positiony//32][player.global_positionx//32]='p'


game_back = pygame.Surface(screen.get_size()).convert()
game_back.fill((255,255,255))
soundtrack = pygame.mixer.Sound("Soundtrack.ogg")
soundtrack.play()
texture0 = pygame.image.load("square1.png")
BTL = pygame.image.load("topLeftBkgd.png")
BTR = pygame.image.load("topRightBkgd.png")
BBL = pygame.image.load("bottomLeftBkgd.png")
BBR = pygame.image.load("bottomRightBkgd.png")

logical_map = [[]]

texture2 = pygame.image.load("square4.png")
playerTexture = pygame.image.load("Static_Main_Big.png")
end_font = pygame.font.Font(pygame.font.match_font('Helvetica'),200)
title_font = pygame.font.Font(pygame.font.match_font('Helvetica'),100)
menu_font = pygame.font.Font(pygame.font.match_font('Helvetica'),50)
small_font = pygame.font.Font(pygame.font.match_font('Helvetica'),25)
menu_back = pygame.Surface(screen.get_size()).convert()
menu_back.fill((0,0,0))

Main_loop = True
Dialouge = False

if Dialouge:
    File = open("Open_Dialog.txt")
    for line in File:
        text_box(line)
    File.close()
if Dialouge:
    time.sleep(1)
    Start = title_font.render("A DeadCat Production", True, (0, 255, 255))
    screen.blit(menu_back, (0, 0))
    screen.blit(Start, (230, 300))
    pygame.display.flip()
    time.sleep(3)
    Start = menu_font.render("In cooperation with Pixel Train Productions", True, (0, 255, 255))
    screen.blit(menu_back, (0, 0))
    screen.blit(Start, (230, 350))
    pygame.display.flip()
    time.sleep(3)

    File = open("Start-Up_Dialog.txt")
    for line in File:
        text_box(line)
    File.close()

buttonIdle = pygame.image.load("Button.png")
buttonHover = pygame.image.load("Button_Hover.png")
buttonClick = pygame.image.load("Button_Click.png")
done = False


while Main_loop:
    
    title = title_font.render("It's a Matter of Time!",True,(0,255,255))
    start = menu_font.render("Play",True,(0,0,0))
    quit_b = menu_font.render("Quit",True,(0,255,255))
    time_label = small_font.render("Time: ",True,(200,0,0))
    button1 = pygame.image.load("Button.png")
    button2 = pygame.image.load("Button.png")
    texture2 = pygame.image.load("platform.png")
    texture0 = pygame.image.load("WallC.png")


    Game_Start = False

    while not Game_Start:
        start_x = 400
        start_y = 250
        quit_x = 400
        quit_y = 400



        for event in pygame.event.get():

            mouse = pygame.mouse.get_pos()
            start = menu_font.render("Play", True, (0, 0, 0))
            quit_b = menu_font.render("Quit", True, (0, 0, 0))

            button1 = buttonIdle
            button2 = buttonIdle
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if mouse[0] in range(start_x-80,start_x+180) and mouse[1] in range(start_y,start_y+60):
                    button1 = buttonClick

                if mouse[0] in range(quit_x-80, quit_x+180) and mouse[1] in range(quit_y,quit_y+60):
                    button2 = buttonClick

            elif event.type== MOUSEBUTTONUP and event.button == 1:
                if mouse[0] in range(start_x-80, start_x + 180) and mouse[1] in range(start_y, start_y + 60):
                    Game_Start = True
                    break
                if mouse[0] in range(quit_x-80, quit_x+180) and mouse[1] in range(quit_y,quit_y+60):
                    pygame.quit()
                    quit()
                    break
            elif event.type == MOUSEMOTION:
                if  mouse[0] in range(start_x-80, start_x+180) and mouse[1] in range(start_y,start_y+60):
                    start = menu_font.render("Play", True, (0, 0, 0))
                    button1 = buttonHover
                if mouse[0] in range(quit_x-80, quit_x+180) and mouse[1] in range(quit_y,quit_y+60):
                    button2 = buttonHover
                    quit_b = menu_font.render("Quit",True, (0,0,0))

            # else:



        screen.blit(menu_back, (0,0))
        screen.blit(button1, (start_x-74, start_y))
        screen.blit(start, (start_x, start_y))
        screen.blit(button2, (quit_x - 74, quit_y))
        screen.blit(quit_b, (quit_x, quit_y))
        screen.blit(title, (200, 50))

        screen.blit(playerTexture, (800, 200))
        pygame.display.flip()

    main_cam = Camera((0,0))

    player = Player((450,550))
    group = pygame.sprite.Group(player)
    exit = door((300, 574))
    doors = pygame.sprite.Group(exit)
    enemies = pygame.sprite.Group()
    for i in range(1):
        enemies.add(Enemy((300,1250),"robot"))
        enemies.add(Enemy((32*115, 32*190), "robot"))
        enemies.add(Enemy((400,850),"agent"))
        enemies.add(Enemy((32*176, 94*32), "agent"))
        enemies.add(Enemy((32 * 64, 32 * 190), "robot"))
        enemies.add(Enemy((32 * 55, 32 * 190), "robot"))




    done = False
    game_map,buttons = build_map()
    game_timer = 0
    timsInt = 60

    while not done:
        dt = clock.tick(60)
        game_timer = game_timer - dt
        
        player.player_event()
        player.movement()

        if player.update(game_map,main_cam):
            done=True

        enemies.update(game_map,main_cam,player)
        exit.update(main_cam)
        # if player.testDeathPrelim():
        #     print("Preliminary Death")
        player.testAllTouching(enemies, buttons,exit, main_cam)


        timsInt-=1
        if timsInt==0:
            cleanLogic()
            timsInt=20

        try:
            for i in range(44):
                for j in range(26):
                    offsetx = main_cam.position[0]%32
                    offsety = main_cam.position[1]%32
                    screen.blit(game_map[int(main_cam.position[0]//32)+i][int(main_cam.position[1]//32)+j].image,((i*32)-offsetx,(j*32)-offsety))
        except:
            pass
        screen.blit(time_label,(15,25))
        for i in range(0,player.timer//5,2):
          screen.fill((0,255,0), (70+i,30,10,20))
        doors.draw(screen)
        enemies.draw(screen)
        group.draw(screen)
        pygame.display.flip()
        #player.Dialog(main_cam)
        if player.dead:
            done = True

    if not player.win:
        game_over_sub = title_font.render("Your Time Has Run Out!", True, (0, 255, 255))
        game_over = end_font.render("Game Over", True, (0, 255, 255))
        screen.blit(menu_back, (0, 0))
        screen.blit(game_over, (250, 100))
        screen.blit(game_over_sub, (235, 400))
        pygame.display.flip()
        time.sleep(4)
    else:
        time.sleep(0.5)
        game_over_sub = title_font.render("Congratulations", True, (0, 255, 255))
        game_over = end_font.render("You Win!", True, (0, 255, 255))
        screen.blit(menu_back, (0, 0))
        screen.blit(game_over, (250, 100))
        screen.blit(game_over_sub, (235, 400))
        pygame.display.flip()
        time.sleep(4)



