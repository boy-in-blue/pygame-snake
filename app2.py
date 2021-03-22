from random import randint, choice
import pygame

SIZE = WIDTH, HEIGHT = 400, 800
BLUE = (145, 196, 200)
YELLOW = (212, 210, 149)
BLACK = (0, 0, 0)
BLUER = (83, 119, 133)
BRIGHT_GREEN = (153, 229, 80)
FPS = 30


class Pygamer:
    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.images = {}
        self.masks = {}
        self.instances = {}
        self.money = int()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.upgrades = {}

    def start(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)

    def draw_background(self, color):
        self.screen.fill(color)

    def kill_switch(self, events, switches: list = [pygame.K_ESCAPE]):
        if events in switches:
            self.running = False
        else:
            pass

    def load_image(self, key_url_pair: list):
        for i in key_url_pair:
            self.images[i[0]] = pygame.image.load(i[1])
            self.instances[i[0]] = []

    def spawn_image(self, key: str, coords=[0, 0]):
        self.instances[key].append([0, coords])

    def draw_image(self, keys: list):
        for key in keys:
            for i in self.instances[key]:
                if i[0] is not None:
                    self.screen.blit(self.images[key], i[1])

    def move_image(self, keys: list):
        for key in keys:
            for i in self.instances[key]:
                if i[0] is not None:
                    i[0] += 0.1
                    # i[1][0] += choice([1, -1])
                    # i[1][1] = 0.5*10*((i[0])**2)
                    i[1][1] += 0.5*10 * ((i[0]**2) - ((i[0]-0.1)**2))

    def out_of_map_check(self, key):
        image_dimension = self.images[key].get_rect()
        for i in self.instances[key]:
            if i[0] is not None:
                if i[1][0] < 0 - image_dimension.w or i[1][0] > WIDTH + image_dimension.w or i[1][1] < 0 - image_dimension.h or i[1][1] > HEIGHT + image_dimension.h:
                    i[0] = None
                    print("Silenced Stray")
                    print(self.instances[key])

#    def create_upgrades(self, key=None, title: str, cost: int):

    def destroy_stray(self, key):
        self.instances[key] = [i for i in self.instances[key] if i[0] is not None]

    def draw_center(self, key):
        rect = self.images[key].get_rect()
        return self.screen.blit(self.images[key], ((WIDTH-rect.w)/2, (HEIGHT-rect.h)/2))

    def create_mask(self, key):
        self.masks[key] = pygame.mask.from_surface(self.images[key])

    def get_mask_check(self, key: str, coord: tuple, offset_coord: tuple):
        rect = self.images[key].get_rect()
        try:
            self.masks[key].get_at((coord[0] - offset_coord.x, coord[1] - offset_coord.y))
            return True
        except IndexError:
            return False

    def print_money(self, pos: tuple):
        self.screen.blit(self.font.render(str(self.money), True, BRIGHT_GREEN), pos)


if __name__ == '__main__':
    pgr = Pygamer()
    pgr.start(SIZE)
    pgr.load_image([('note', 'note.png'), ('coin', 'coin.png'), ('coin4x', 'coin4x.png')])
    pgr.create_mask('coin4x')
    while pgr.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pgr.running = False
            elif event.type == pygame.KEYDOWN:
                pgr.kill_switch(event.key, [pygame.K_ESCAPE, pygame.K_CAPSLOCK])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4,):
                    pgr.spawn_image('note', [randint(0, WIDTH-1), randint(-1, 0)])
                elif event.button in (5,):
                    pgr.spawn_image('coin', [randint(0, WIDTH-1), randint(-1, 0)])
                elif event.button in (1,):
                    click = click_x, click_y = event.pos
                    if pgr.get_mask_check('coin4x', click, bigcoin):
                        pgr.money += 1
                        pgr.spawn_image('coin', [randint(0, WIDTH-1), randint(-1, 0)])

            else:
                pass
        pgr.move_image(['note', 'coin'])
        pgr.draw_background(BLUE)
        bigcoin = pgr.draw_center('coin4x')
        pygame.draw.line(pgr.screen, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
        pygame.draw.line(pgr.screen, BLACK, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
        pgr.draw_image(['note', 'coin'])
        pgr.print_money((10, 10))
        pygame.display.update()
        pgr.out_of_map_check('note')
        pgr.out_of_map_check('coin')
        pgr.destroy_stray('note')
        pgr.destroy_stray('coin')
        pgr.clock.tick(FPS)
"""1 - left click
2 - middle click
3 - right click
4 - scroll up
5 - scroll down"""
