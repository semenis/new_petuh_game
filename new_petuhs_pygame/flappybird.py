import math
import os
import random
from random import randint
from collections import deque
import pygame
from pygame.locals import *
import sys
#import time
#import datetime


FPS = 60
ANIMATION_SPEED = 0.18  # пикселей в мс
WIN_WIDTH = 284 * 2     # Размер заднего фона : 284x512 px
WIN_HEIGHT = 512
screen_rect = (0, 0, WIN_WIDTH, WIN_HEIGHT)

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

class Bird(pygame.sprite.Sprite):
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3
    def __init__(self, x, y, msec_to_climb, images):

        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)





class Pipess(pygame.sprite.Sprite):
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False
        self.image = pygame.Surface((Pipess.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -                  
             3 * Bird.HEIGHT -            
             3 * Pipess.PIECE_HEIGHT) /  
            Pipess.PIECE_HEIGHT         
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        
        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*Pipess.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - Pipess.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

       
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * Pipess.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))

        
        self.top_pieces += 1
        self.bottom_pieces += 1

        
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        return self.top_pieces * Pipess.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        return self.bottom_pieces * Pipess.PIECE_HEIGHT

    @property
    def visible(self):
        return -Pipess.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return Rect(self.x, 0, Pipess.WIDTH, Pipess.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


def load_images():
    def load_image(img_file_name):
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img
    return {'pero':load_image('star.png'),'background': load_image('background.png'),'petuh' : load_image('petuh.png'),'pipe-end': load_image('pipe_end.png'), 'pipe-body': load_image('pipe_body.png'),'bird-wingup': load_image('bird_wing_up.png'),'bird-wingdown': load_image('bird_wing_down.png')}


def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps


def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    images = load_images()
    fire = [images['pero']]
    rand_angle = range(1,359)
    for scale in (5,10,20):
        fire.append(pygame.transform.rotate(pygame.transform.scale(fire[0], (scale, scale)),random.choice(rand_angle)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = 0.2

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
      #  self.image = pygame.transform.rotate(self.image,5)
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()
def create_particles(position):
    # количество создаваемых частиц
    particle_count = 16
    # возможные скорости
    numbers = range(-5, 12)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))
all_sprites = pygame.sprite.Group()


def main():
    def startScreen():
        images = load_images()
        introText = ["НОВЫЕ ПЕТУХИ: PYGAME", "",
                     "Правила игры:",
                     "Нажимайте кнопки: вверх, ввод, пробел ",
                     "или ПКМ, чтобы петух прыгнул",
                     "не врезайтесь в трубы!"]

       # screen.fill(pygame.Color('blue'))
        screen.blit(images['petuh'], (0, 0))
        font = pygame.font.Font(None, 30)
        textCoord = 50
        for line in introText:
            stringRendered = font.render(line, 1, pygame.Color('green'))
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
                    return  # начинаем игру
            pygame.display.flip()
    def EndScreen(score=0):
        images = load_images()
        introText = ["ВЫ ПРОИГРАЛИ", "",
                     "Пожалуйста, не ломайте компьютер,",
                     "Не кидайте мышку или клавиатуру,",
                     "Не бейте создателя,",
                     "Ваш счет: % i" % score,
                     "Любая кнопка выключит игру,",
                     "Кнопка ПРОБЕЛ начнет заново"
                     ]

        screen.fill(pygame.Color('blue'))
        screen.blit(images['petuh'], (0, 0))
        font = pygame.font.Font(None, 30)
        textCoord = 50
        for line in introText:
            stringRendered = font.render(line, 1, pygame.Color('red'))
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
                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    game()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

                    pygame.quit();
                    sys.exit();
            pygame.display.flip()


    pygame.display.set_caption('Новые петухи')
    startScreen()

    def game():
        clock = pygame.time.Clock()
        score_font = pygame.font.SysFont(None, 32, bold=True)
        images = load_images()
        bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2, (images['bird-wingup'], images['bird-wingdown']))

        pipes = deque()

        frame_clock = 0
        score = 0
        done = paused = False
        while not done:
            clock.tick(FPS)
            if not (paused or frame_clock % msec_to_frames(Pipess.ADD_INTERVAL)):
                pp = Pipess(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)

            for e in pygame.event.get():
                if e.type == MOUSEBUTTONDOWN:
                    create_particles(e.pos)
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    done = True
                    break
                elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                    paused = not paused
                elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                        e.key in (K_UP, K_RETURN, K_SPACE)):
                    bird.msec_to_climb = Bird.CLIMB_DURATION

            if paused:
                continue

            pipe_collision = any(p.collides_with(bird) for p in pipes)
            if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                create_particles((bird.x,bird.y))
                #timer = time.time()
                #TIME_TO_CONTINUE=2
                #while time.time() - timer < TIME_TO_CONTINUE:

                done = True

            for x in (0, WIN_WIDTH / 2):
                screen.blit(images['background'], (x, 0))

            while pipes and not pipes[0].visible:
                pipes.popleft()

            for p in pipes:
                p.update()
                screen.blit(p.image, p.rect)
            all_sprites.update()
            bird.update()

            screen.blit(bird.image, bird.rect)
            all_sprites.draw(screen)

            for p in pipes:
                if p.x + Pipess.WIDTH < bird.x and not p.score_counted:
                    score += 1
                    p.score_counted = True

            score_surface = score_font.render(str(score), True, (255, 255, 255))
            score_x = WIN_WIDTH/2 - score_surface.get_width()/2
            screen.blit(score_surface, (score_x, Pipess.PIECE_HEIGHT))

            pygame.display.flip()
            frame_clock += 1
        EndScreen(score)

    game()

if __name__ == '__main__':
    main()
