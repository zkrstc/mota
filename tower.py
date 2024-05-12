import os
import sys 
import pygame
from pygame.locals import *
def control_tank(event):
    speed =  [x,y]=[0,0]
    speed_offset=1
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key==pygame.K_a:
            speed[0]-=speed_offset
        if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
            speed[0]=speed_offset
        if event.key == pygame.K_UP or event.key==pygame.K_w:
            speed[1] -= speed_offset
        if event.key == pygame.K_DOWN or event.key==pygame.K_s:
            speed[1]=speed_offset
    if event.type == pygame.KEYUP:
     if event.type in [pygame.K_UP,pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_w]:
         speed = [0,0]
    return speed 
fps=120
clock=pygame.time.Clock()
def play_tank():
    pygame.init()
    window_size = Rect(0,0,600,400)
    speed = [1,1]
    color_black=(255,255,255)
    screen=pygame.display.set_mode(window_size.size)
    tank_image=pygame.image.load('image/1.png')
    tank_rect=tank_image.get_rect()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        cur_speed = control_tank(event)
        tank_rect=tank_rect.move(cur_speed).clamp(window_size)
        screen.blit(tank_image,tank_rect)
        pygame.display.update()
play_tank()