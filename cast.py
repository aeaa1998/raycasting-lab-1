import pygame
from math import pi, cos, sin, atan2
import time




def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("UIGAME", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        screen.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, GREEN, LIGHT_GREEN, game_loop)
        button("Quit", 550, 450, 100, 50, RED, LIGHT_RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_win():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Has Ganado!", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)



def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 12, 12)
LIGHT_RED = (220,20,60)
GREEN = (127,255,0)
BACKGROUND = (0, 255, 255)
LIGHT_GREEN = (152,251,152)

display_width = 1000
display_height = 500

clock = pygame.time.Clock()
wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')
wall4 = pygame.image.load('./wall4.png')
wall5 = pygame.image.load('./wall5.png')
chest = pygame.image.load('./chest.png')

textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
}

win = [{
    "x": 100,
    "y": 100,

}
]

enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": pygame.image.load('./sprite2.png')
  },
  {
    "x": 280,
    "y": 190,
    "texture": pygame.image.load('./sprite3.png')
  },
  {
    "x": 225,
    "y": 340,
    "texture": pygame.image.load('./sprite4.png')
  },
  {
    "x": 220,
    "y": 425,
    "texture": pygame.image.load('./sprite1.png')
  },
  {
    "x": 320,
    "y": 420,
    "texture": pygame.image.load('./sprite2.png')
  }
]

class Raycaster(object):
  def __init__(self, screen, win_game):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "a": pi/3,
      "fov": pi/3
    }
    self.map = []
    self.mapWithKeys = {}
    self.win_game = win_game
    # self.clear()

  def move(self, x, y):
      new_x = r.player["x"] + x
      new_y = r.player["y"] + y
      move = self.check_move(new_x, new_y)
      if move == "move":
          r.player["x"] += x
          r.player["y"] += y
      elif move == "win":
          self.win_game()


  def check_move(self, x, y):
      if x in self.mapWithKeys:
          if y in self.mapWithKeys[x]:
              if self.mapWithKeys[x][y] != "win":
                  return None
              else:
                  return "win"

      return "move"

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 50):
      for cy in range(y, y + 50):
        tx = int((cx - x)*128 / 50)
        ty = int((cy - y)*128 / 50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)

      i = int(x/50)
      j = int(y/50)

      if self.map[j][i] != ' ':
        hitx = x - i*50
        hity = y - j*50

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / 50)

        return d, self.map[j][i], tx

      self.point(int(x), int(y), (255, 255, 255))

      d += 1

  def draw_stake(self, x, h, texture, tx):
    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      ty = int(((y - start)*128)/(end - start))
      c = texture.get_at((tx, ty))
      self.point(x, y, c)

  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])   # why atan2? https://stackoverflow.com/a/12011762
    
    # print(">", sprite_a)
    # while sprite_a - self.player["a"] > pi:
    #  sprite_a -= 2*pi
    # while sprite_a - self.player["a"] < -pi:
    #  sprite_a += 2*pi
    # print(">>", sprite_a)

    sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
    sprite_size = (500/sprite_d) * 70

    sprite_x = 500 + (sprite_a - self.player["a"])*500/self.player["fov"] + 250 - sprite_size/2
    sprite_y = 250 - sprite_size/2

    sprite_x = int(sprite_x)
    sprite_y = int(sprite_y)
    sprite_size = int(sprite_size)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        if x > 500:
          tx = int((x - sprite_x) * 128/sprite_size)
          ty = int((y - sprite_y) * 128/sprite_size)
          c = sprite["texture"].get_at((tx, ty))
          if c != (152, 0, 136, 255):
            self.point(x, y, c)

  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
            if x in self.mapWithKeys:
                self.mapWithKeys[x][y] = self.map[j][i]
            else:
                self.mapWithKeys[x] = {}
                self.mapWithKeys[x][y] = self.map[j][i]

            self.draw_rectangle(x, y, textures[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(0, 500):
      a = self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
      d, c, tx = self.cast_ray(a)
      x = 500 + i
      di = (d*cos(a-self.player["a"]))
      if di > 0:
        h = 500/(d*cos(a-self.player["a"])) * 70
        self.draw_stake(x, h, textures[c], tx)

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (0, 0, 0))
      self.draw_sprite(enemy)

    for w in win:
        if w["x"] in self.mapWithKeys:
            self.mapWithKeys[w["x"]][w["y"]] = "win"
        else:
            self.mapWithKeys[w["x"]] = {}
            self.mapWithKeys[w["x"]][w["y"]] = "win"
        self.point(w["x"], w["y"], (0, 0, 0))
        # self.draw_sprite(w)

pygame.init()
screen = pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF|pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
r = Raycaster(screen, game_win)
r.load_map('./map.txt')

c = 0


def game_loop():
    while True:
      screen.fill((113, 113, 113))
      r.render()

      for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
          exit(0)
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_a:
            r.player["a"] -= pi/10
          elif e.key == pygame.K_d:
            r.player["a"] += pi/10

          elif e.key == pygame.K_RIGHT:
              r.move(10, 0)

          elif e.key == pygame.K_LEFT:
              r.move(-10, 0)
              # new_x = r.player["x"] - 10
              # if new_x in r.mapWithKeys:
              #     if r.player["y"] in r.mapWithKeys[new_x]:

          elif e.key == pygame.K_UP:
              r.move(0, 10)
          elif e.key == pygame.K_DOWN:
              r.move(0, -10)

          if e.key == pygame.K_f:
            if screen.get_flags() and pygame.FULLSCREEN:
                pygame.display.set_mode((display_width, display_height))
            else:
                pygame.display.set_mode((display_width, display_height),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

      pygame.display.flip()

game_intro()
game_loop()
