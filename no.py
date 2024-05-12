import pygame
import time
import sys
import os

from pygame.locals import *
pygame.init()

window_size = Rect(0,0,600,400)
speed = [1,1]
color_black=(255,255,255)
screen=pygame.display.set_mode(window_size.size)
tank_image=pygame.image.load('image/1.png')
tank_rect=tank_image.get_rect()
pygame.key.stop_text_input()
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                print('no')
            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                print('nof')
            if event.key == pygame.K_UP or event.key==pygame.K_w:
                print('nodd')
            if event.key == pygame.K_DOWN or event.key==pygame.K_s:
                print('noss')
    screen.blit(tank_image,tank_rect)
    pygame.display.update()