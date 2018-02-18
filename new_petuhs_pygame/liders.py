import pygame
#from flappybird import load_images
import sys
import random
WIN_WIDTH = 284 * 2  # Размер заднего фона : 284x512 px
WIN_HEIGHT = 512
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def FormatTable():
    with open('save.txt', 'r') as save:
        table = {}
        for i in save.readlines():
            try:
                if i.split()[0] not in table.keys():
                    table[i.split()[0]] = int(i.split()[1])
                else:
                    if table[i.split()[0]] < int(i.split()[1]):
                        table[i.split()[0]] = int(i.split()[1])
            except:
                pass
    from operator import itemgetter
    array = sorted(table.items(), key=itemgetter(1), reverse=True)
    array = array[:10]
    with open('save.txt', 'w') as save:
        for i in array:
            save.write(str(i[0]) + '    ' + str(i[1]) + '\n')



def AddPoint(name, score):
    with open('save.txt', 'a') as save:
        if name == 'Semyon':
            score += 100
        if name.strip() == '':
            name = 'Anonimous'
        save.write(str(name) + ' ' + str(score) + '\n')
    FormatTable()


def Print_Table():
    #images = load_images()
    with open('save.txt', 'r') as save:
        introText = map(lambda x: x.strip(), save.readlines())

    screen.fill(pygame.Color('green'))
   # screen.blit(images['petuh'], (0, 0))
    font = pygame.font.Font(None, 30)
    textCoord = 50
    for line in introText:
        Rand_Colors = ['red','black','blue','yellow','white']
        stringRendered = font.render(line, 1, pygame.Color(random.choice(Rand_Colors)))
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
            elif event.type == pygame.KEYDOWN and pygame.K_SPACE:
                import flappybird
                flappybird.main().game()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit();
                sys.exit();
        pygame.display.flip()
