from random import randint
import pygame
from app2 import Pygamer, BLUE, YELLOW, BLACK, BLUER
import numpy as np

SIZE = WIDTH, HEIGHT = 400, 400
CHUNK = 16
FPS = 15


class SnakeGamer(Pygamer):
    def __init__(self):
        super().__init__()
        self.direction = [1, 0]
        self.snake_body = []
        self.food = []
        self.digest_food = False

    def create_board_matrix(self):
        self.board = np.zeros((WIDTH//CHUNK, HEIGHT//CHUNK), np.int8)
        return self.board

    def spawn_snake(self):
        self.board[(w := np.random.randint(0, WIDTH//CHUNK)), (h := np.random.randint(0, WIDTH//CHUNK))] = 1
        self.snake_body.append([w, h])
        self.board[w-1, h] = 1
        self.snake_body.append([w-1, h])
        self.snake_body.append([w-2, h])
        self.snake_body.append([w-3, h])
        #self.board[w-2, h] = True
        #self.board[w-3, h] = True

    def move_snake(self):

        new_x = self.snake_body[0][0] + self.direction[0]
        new_y = self.snake_body[0][1] + self.direction[1]

        new_x %= WIDTH//CHUNK
        new_y %= HEIGHT//CHUNK

        if new_x == self.food[0][0] and new_y == self.food[0][1]:
            self.digest_food = True
            self.food.pop(0)
            self.spawn_food()

        self.snake_body.insert(0, [new_x, new_y])

        if self.digest_food:
            self.digest_food = False
        else:
            self.snake_body.pop(-1)

        self.board[:, :] = 0

        for i in self.snake_body:
            self.board[tuple(i)] = 1

        # self.board[tuple(self.snake_body[0])] = False
        # self.snake_body[0] = self.snake_head[0]
        # self.snake_body[1] = self.snake_head[1]
        # self.board[tuple(self.snake_head)] = False
        # self.snake_head[0] += self.direction[0]
        # self.snake_head[1] += self.direction[1]
        # self.snake_head[0] %= WIDTH//CHUNK
        # self.snake_head[1] %= HEIGHT//CHUNK
        # self.board[tuple(self.snake_head)] = True
        # self.board[tuple(self.snake_body)] = True

    def draw_snake(self):
        a = np.where(self.board)
        for i in zip(a[0], a[1]):
            for w in range(CHUNK):
                for h in range(CHUNK):
                    self.screen.set_at((CHUNK*i[0]+w, CHUNK*i[1]+h), BLACK)

    def draw_food(self):
        for i in self.food:
            for w in range(CHUNK):
                for h in range(CHUNK):
                    self.screen.set_at((CHUNK*i[0]+w, CHUNK*i[1]+h), BLACK)
        print(self.food)

    def draw_grid(self, gap, axis_color=BLACK, grid_color=BLUER):
        for i in range(0, WIDTH, gap):
            if i == WIDTH/2:
                pygame.draw.line(self.screen, axis_color, (i, 0), (i, HEIGHT))
            else:
                pygame.draw.line(self.screen, grid_color, (i, 0), (i, HEIGHT))

        for i in range(0, HEIGHT, gap):
            if i == HEIGHT/2:
                pygame.draw.line(self.screen, axis_color, (0, i), (WIDTH, i))
            else:
                pygame.draw.line(self.screen, grid_color, (0, i), (WIDTH, i))

    def snake_direction(self, keypress):
        if keypress == 'w':
            self.direction = [0, -1]
        elif keypress == 'a':
            self.direction = [-1, 0]
        elif keypress == 's':
            self.direction = [0, 1]
        elif keypress == 'd':
            self.direction = [1, 0]
        else:
            pass

    def spawn_food(self):
        w = np.random.randint(0, WIDTH//CHUNK)
        h = np.random.randint(0, HEIGHT//CHUNK)
        self.food.append((w, h))


if __name__ == '__main__':
    pgr = SnakeGamer()
    pgr.start(SIZE)
    pgr.create_board_matrix()
    pgr.spawn_snake()
    pgr.spawn_food()
    while pgr.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pgr.running = False
            elif event.type == pygame.KEYDOWN:
                pgr.kill_switch(event.key, [pygame.K_ESCAPE, pygame.K_CAPSLOCK])
                if event.key == pygame.K_w:
                    pgr.snake_direction('w')
                elif event.key == pygame.K_a:
                    pgr.snake_direction('a')
                elif event.key == pygame.K_s:
                    pgr.snake_direction('s')
                elif event.key == pygame.K_d:
                    pgr.snake_direction('d')
                else:
                    pass
            else:
                pass
        pgr.move_snake()
        pgr.draw_background(BLUE)
        pgr.draw_grid(CHUNK, BLUER, YELLOW)
        pgr.draw_snake()
        pgr.draw_food()
        pygame.display.update()
        pgr.clock.tick(FPS)
