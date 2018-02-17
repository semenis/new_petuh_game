import pygame
from flappybird import load_images
import sys

WIN_WIDTH = 284 * 2  # Размер заднего фона : 284x512 px
WIN_HEIGHT = 512
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
def AddPoint(name, score):
    with open('save.txt', 'a') as save:
        if name == 'Semyon':
            score+=100
        save.write(str(name)+' '+str(score)+'\n')
def Print_Table():
    images = load_images()
    with open('save.txt','r') as save:
        introText = map(lambda x: x.strip(), save.readlines())

    screen.fill(pygame.Color('green'))
    screen.blit(images['petuh'], (0, 0))
    font = pygame.font.Font(None, 30)
    textCoord = 50
    for line in introText:
        stringRendered = font.render(line, 1, pygame.Color('blue'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 10
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

                pygame.quit();
                sys.exit();
        pygame.display.flip()

