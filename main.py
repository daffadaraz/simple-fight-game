import pygame, pygame_gui, sys
from pygame import mixer
from fighter import Fighter
from button import Button

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boxing Game")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#UI FOR TEXT INPUT
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
MAX_SCORE = 2
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((SCREEN_WIDTH/4, 275), (SCREEN_WIDTH/2, 50)), manager=manager,object_id='#main_text_entry',initial_text=str(MAX_SCORE))
text_input.set_allowed_characters('numbers')

#define colours
RED = (225, 52, 30)
BLUE = (30, 203, 225)
YELLOW = (212, 174, 97)
WHITE = (255, 255, 255)
GREEN = (138, 194, 85)

#load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
punch1_fx = pygame.mixer.Sound("assets/audio/punch-1.mp3")
punch1_fx.set_volume(0.5)
punch2_fx = pygame.mixer.Sound("assets/audio/punch-2.mp3")
punch2_fx.set_volume(0.5)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
BG = pygame.image.load("assets/images/background/MainmenuBG.png").convert_alpha()

#load spritesheets
boxer1_sheet = pygame.image.load("assets/images/boxer1/boxer1.png").convert_alpha()
boxer2_sheet = pygame.image.load("assets/images/boxer2/boxer2.png").convert_alpha()
#define number of steps in each animation
BOXER1_ANIMATION_STEPS = [6, 3, 1, 4, 4, 3, 6, 1]
BOXER2_ANIMATION_STEPS = [6, 3, 1, 4, 4, 3, 6, 1]

# #load vicory image
# victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
# p1_win = pygame.image.load("assets/images/icons/p1wins.png").convert_alpha()
# p2_win = pygame.image.load("assets/images/icons/p2wins.png").convert_alpha()

#define font
count_font = pygame.font.Font("assets/fonts/anton.ttf", 80)
score_font = pygame.font.Font("assets/fonts/anton.ttf", 30)
turok_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
font = pygame.font.Font("freesansbold.ttf",24)

def get_font(size): # get font based on deseired size
  return pygame.font.Font("assets/fonts/anton.ttf", size)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_text_center(text, font, text_col, x = 0, y = 0):
  img = font.render(text, True, text_col)
  rect = img.get_rect(center=(SCREEN_WIDTH/2 - x, SCREEN_HEIGHT/2 - y))
  screen.blit(img, rect)

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

#game loop
def play():
  #define game variables
  intro_count = 3
  last_count_update = pygame.time.get_ticks()
  score = [0, 0]#player scores. [P1, P2]
  round_over = False
  ROUND_OVER_COOLDOWN = 2000

  #define fighter variables
  BOXER1_SIZE = 162
  BOXER1_SCALE = 6
  BOXER1_OFFSET = [72, 70, 550, 450]
  BOXER1_DATA = [BOXER1_SIZE, BOXER1_SCALE, BOXER1_OFFSET]
  BOXER2_SIZE = 162
  BOXER2_SCALE = 6
  BOXER2_OFFSET = [72, 70, 450, 450]
  BOXER2_DATA = [BOXER2_SIZE, BOXER2_SCALE, BOXER2_OFFSET]

  #create two instances of fighters
  fighter_1 = Fighter(1, 200, 310, False, BOXER1_DATA, boxer1_sheet, BOXER1_ANIMATION_STEPS, punch1_fx)
  fighter_2 = Fighter(2, 700, 310, True, BOXER2_DATA, boxer2_sheet, BOXER2_ANIMATION_STEPS, punch2_fx)

  #dialog
  messages = ["First Message by Boxer 1",
            "First Message by Boxer 2",
            "Second Message by Boxer 1",
            "Second Message by Boxer 2"
            ]
  characters = [fighter_1,
                fighter_2,
                fighter_1,
                fighter_2
                ]
  snip = font.render('',True,'White')
  counter = 0
  speed = 3
  active_message = 0
  active_character = 0
  message = messages[active_message]
  character = characters[active_character]
  done = False
  dialog_done = False
  run = True

  round_start = True
  last = pygame.time.get_ticks()
  cooldown = 500    

  while run:
    clock.tick(FPS)

    if pygame.time.get_ticks() - last > cooldown:
      round_start = False

    #draw background
    draw_bg()

    if dialog_done == False and round_start == False:
      
      character.draw_dialog(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

      # s = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
      # s.set_alpha(128)
      #pygame.draw.rect(screen, "black", [0 , SCREEN_HEIGHT-150, SCREEN_WIDTH, 200], 1)
      s = pygame.Surface((SCREEN_WIDTH, 150))  # the size of your rect
      s.set_alpha(128)                # alpha level
      s.fill((0,0,0))           # this fills the entire surface
      screen.blit(s, (0,SCREEN_HEIGHT-150))    # (0,0) are the top-left coordinates

      if counter < speed * len(message):
        counter += 1
      elif counter >= speed * len(message):
        done = True

      snip = font.render(message[0:counter//speed],True,'White')
      screen.blit(snip, (10, SCREEN_HEIGHT-120))
      
      fighter_1.update()
      fighter_2.update()

    if dialog_done:
      #show player stats
      draw_health_bar(fighter_1.health, 20, 20)
      draw_health_bar(fighter_2.health, 580, 20)
      draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
      draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

      #update countdown
      if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
      else:
        #display count timer
        # draw_text(str(intro_count), count_font, RED, (SCREEN_WIDTH / 2)-20, SCREEN_HEIGHT / 3)
        draw_text_center(str(intro_count), count_font, RED, 0, 100)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
          intro_count -= 1
          last_count_update = pygame.time.get_ticks()

      #update fighters
      fighter_1.update()
      fighter_2.update()

      #draw fighters
      fighter_1.draw(screen)
      fighter_2.draw(screen)

      #check for player defeat
      if round_over == False:
        if fighter_1.alive == False and fighter_2.alive == False:
          score[0] += 1
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
        elif fighter_1.alive == False:
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
          score[0] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
      elif (score[1] == MAX_SCORE or score[0] == MAX_SCORE) and round_over == True:
        if score[0] == MAX_SCORE and score[1] == MAX_SCORE:
          draw_text_center("DRAW!", turok_font, YELLOW, 0, 100)
        elif score[0] == MAX_SCORE:
          # screen.blit(p1_win, (360, 150))
          draw_text_center("P1 WINS!", turok_font, RED, 0, 100)
        else:
          draw_text_center("P2 WINS!", turok_font, BLUE, 0, 100)
          # screen.blit(p2_win, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
          run = False
      else:
        #display victory image
        draw_text_center("ROUND OVER !", count_font, YELLOW, 0, 100)
        # screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
          round_over = False
          intro_count = 3
          fighter_1 = Fighter(1, 200, 310, False, BOXER1_DATA, boxer1_sheet, BOXER1_ANIMATION_STEPS, punch1_fx)
          fighter_2 = Fighter(2, 700, 310, True, BOXER2_DATA, boxer2_sheet, BOXER2_ANIMATION_STEPS, punch2_fx)

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      #for dialog
      if event.type == pygame.KEYDOWN:
        if done and active_message < len(messages)-1:
          done = False
          active_message += 1
          message = messages[active_message]
          active_character += 1
          character = characters[active_character]
          counter = 0
        elif done and active_message == len(messages)-1:
          dialog_done = True

    #update display
    pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("#3e3e3e")

        OPTIONS_TEXT = get_font(45).render("MAX ROUND", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH/2, 200))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH/2, 400), text_input="BACK", font=get_font(75), base_color="#97b9d2", hovering_color="white")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        UI_REFRESH_RATE = clock.tick(60)/1000
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(screen)

        for event in pygame.event.get():
            manager.process_events(event)
            if (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#main_text_entry'):
              global MAX_SCORE
              if (len(event.text) > 0):
                try:
                  MAX_SCORE = int(event.text) 
                  if(MAX_SCORE == 0):
                    MAX_SCORE = 1
                    text_input.set_text(str(MAX_SCORE))
                except:
                  MAX_SCORE = 1
                  text_input.set_text(str(MAX_SCORE))
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
  while True:
    screen.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("BOXING THE GAME", True, YELLOW)
    MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 75))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(SCREEN_WIDTH/2, 225), 
                        text_input="PLAY", font=get_font(75), base_color="#ebebeb", hovering_color="#b1b1b1")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(SCREEN_WIDTH/2, 375), 
                        text_input="OPTIONS", font=get_font(75), base_color="#ebebeb", hovering_color="#b1b1b1")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(SCREEN_WIDTH/2, 525), 
                        text_input="QUIT", font=get_font(75), base_color="#ebebeb", hovering_color="#b1b1b1")

    screen.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                play()
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                options()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
    pygame.display.update()

# play()
main_menu()

#exit pygame
# pygame.quit()