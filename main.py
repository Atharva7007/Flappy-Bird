import pygame
import random, os
pygame.init()

screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Flappy Bird")

background = pygame.image.load("bgd.png")

font = pygame.font.Font("freesansbold.ttf", 32)

class FlappyBird:

    def __init__(self):
        self.angle = 0
        self.Flappy = pygame.image.load("bird.png")
        self.Flappy_up = pygame.transform.rotate(self.Flappy, 30)
        self.Flappy_down = pygame.transform.rotate(self.Flappy, self.angle)
        self.x = 80
        self.y = 240
        self.y_change = 0
        self.playerImg = self.Flappy
        self.t = 0 # time
        self.g = 6 # gravity

    def create_flappy(self):
        screen.blit(self.playerImg, (self.x, self.y))

    def jump(self):
        self.y_change = -3
        self.playerImg = self.Flappy_up
        self.t = 0.5
        self.angle = 0

    def move(self): # Simulating gravity and jumping mechanics
        self.t += 0.013
        if self.angle > -90:
            self.angle += -1.45
        self.y_change = self.t + self.g * (self.t ** 2) / 2 # s = ut + 1/2 a t^2 formula

        self.Flappy_down = pygame.transform.rotate(self.Flappy, self.angle)
        self.playerImg = self.Flappy_down

class Pipes:

    def __init__(self):

        self.pipe_width = 70
        self.pipe_gap = 120
        self.pipe_length = 546
        self.vel = 2
        self.bpipeImg = pygame.image.load(r"bpipe.png")
        self.tpipeImg = pygame.image.load(r"tpipe.png")

        self.num_of_pipes = 50
        self.bpipe_x = []
        self.bpipe_y = []

        self.tpipe_x = []
        self.tpipe_y = []

        for i in range(self.num_of_pipes):
            self.bpipe_x.append(620)
            self.bpipe_y.append(random.randint(190, 450))

            self.tpipe_x.append(620)
            self.tpipe_y.append(self.bpipe_y[i] - self.pipe_gap - self.pipe_length)

    def create_pipe(self, x, y):
        if x > -65:
            if y < 0:
                screen.blit(self.tpipeImg, (x, y))
            else:
                screen.blit(self.bpipeImg, (x, y))


def main():
    running = True
    play_game = False
    dead = False
    jumping = False

    while running:
        bird = FlappyBird()
        pipe = Pipes()
        pipe_count = 1
        score_value = 0
        instr = "Press Enter to play"
        instruction = font.render(instr, True, (255, 255, 255))

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        bird.create_flappy()
        screen.blit(instruction, (70, 50))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    play_game = True
                    dead = False

        while play_game:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    play_game = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                        jumping = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        bird.move()
                        jumping = False

            if bird.playerImg == bird.Flappy:
                bird.move()

            if not jumping:
                bird.move()

            bird.y += bird.y_change

            bird.create_flappy()
            pipe.create_pipe(pipe.bpipe_x[0], pipe.bpipe_y[0])
            pipe.create_pipe(pipe.tpipe_x[0], pipe.tpipe_y[0])

            for i in range(1, pipe.num_of_pipes):
                if pipe.bpipe_x[i - 1] < 300: # To maintain distance between pipes create pipe when pipe before it is behind the 300 pixel mark
                    pipe.create_pipe(pipe.bpipe_x[i], pipe.bpipe_y[i])
                    pipe.create_pipe(pipe.tpipe_x[i], pipe.tpipe_y[i])
                    pipe_count = i + 1

            if pipe_count > 1:
                for i in range(1, pipe_count):
                    pipe.bpipe_x[i] -= pipe.vel
                    pipe.tpipe_x[i] -= pipe.vel

            pipe.bpipe_x[0] -= pipe.vel
            pipe.tpipe_x[0] -= pipe.vel

            if bird.y > 460:
                play_game = False
                dead = True
                screen.blit(instruction, (70, 50))

            # check for collision with a pipe
            for i in range(pipe_count):
                if pipe.bpipe_x[i] < 120 and pipe.bpipe_x[i] > 10:
                    if bird.y + 39 > pipe.bpipe_y[i]:  # detect collision
                        play_game = False
                        dead = True
                        screen.blit(instruction, (70, 50))
                    if bird.y + 12 < (pipe.bpipe_y[i] - pipe.pipe_gap):  # detect collision
                        play_game = False
                        dead = True
                        screen.blit(instruction, (70, 50))

            for i in range(pipe_count):
                if pipe.bpipe_x[i] < 35 and pipe.bpipe_x[i] > 0:
                    score_value = i + 1

            score = font.render("Score: " + str(score_value), True, (255, 255, 255))
            screen.blit(score, (10, 10))

            pygame.display.update()

        del bird
        del pipe

        if not dead:
            pygame.display.update()

main()
