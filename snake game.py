import pygame, sys, random
from pygame.math import Vector2


#creating the snake
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        #images for the snake body:
        self.head_up = pygame.image.load('Snake game/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Snake game/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Snake game/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Snake game/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Snake game/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Snake game/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Snake game/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Snake game/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Snake game/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Snake game/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Snake game/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Snake game/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Snake game/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Snake game/body_bl.png').convert_alpha()                                     
        self.crunch_sound = pygame.mixer.Sound('Snake game/Sound_crunch.wav')

    def Snake_draw(self):
        self.Update_HeadGraphics()
        self.Update_TailGraphics()

        for index, box in enumerate(self.body):#gives us an index of what objects inside of the list
            X_position = int(box.x * Cell_Size)
            Y_position = int(box.y * Cell_Size)         
            box_rectangle = pygame.Rect(X_position, Y_position, Cell_Size, Cell_Size)

            #this would be the direction of the snake will be facing
            if index == 0:
                screen.blit(self.head,box_rectangle)
#this will be the last block covered(so the tail)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, box_rectangle)
            else:
                pre_box = self.body[index + 1] - box
                next_box = self.body[index - 1] - box
                if pre_box.x == next_box.x:
                    screen.blit(self.body_vertical, box_rectangle)#this is the vertical graphics added
                elif pre_box.y == next_box.y:
                    screen.blit(self.body_horizontal, box_rectangle)#this is the horizontal graphics added

            #creating the graphics movements for all the body parts in between

                else:#TOP LEFT
                    if (pre_box == Vector2(-1, 0) and next_box == Vector2(0, -1)) or \
                       (pre_box == Vector2(0, -1) and next_box == Vector2(-1, 0)):
                            screen.blit(self.body_tl, box_rectangle)

                # BOTTOM LEFT
                    elif (pre_box == Vector2(-1, 0) and next_box == Vector2(0, 1)) or \
                         (pre_box == Vector2(0, 1) and next_box == Vector2(-1, 0)):
                              screen.blit(self.body_bl, box_rectangle)

                # TOP RIGHT
                    elif (pre_box == Vector2(1, 0) and next_box == Vector2(0, -1)) or \
                         (pre_box == Vector2(0, -1) and next_box == Vector2(1, 0)):
                              screen.blit(self.body_tr, box_rectangle)

                # BOTTOM RIGHT
                    elif (pre_box == Vector2(1, 0) and next_box == Vector2(0, 1)) or \
                         (pre_box == Vector2(0, 1) and next_box == Vector2(1, 0)):
                              screen.blit(self.body_br, box_rectangle)

    def Update_HeadGraphics(self):#creating the graphics movement for the head
         Head_relation = self.body[1] - self.body[0]
         if Head_relation == Vector2(1,0): self.head = self.head_left
         elif Head_relation == Vector2(-1,0): self.head = self.head_right
         elif Head_relation == Vector2(0,1): self.head = self.head_up
         elif Head_relation == Vector2(0,-1): self.head = self.head_down

    def Update_TailGraphics(self):#creating the graphics movement for the tail
        Tail_relation = self.body[-2] - self.body[-1]
        if Tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif Tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif Tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif Tail_relation == Vector2(0,-1): self.tail = self.tail_down
             


    def Snake_Movement(self):
        if self.new_block == True: # adds on the new block as the length
            copy_body = self.body[:] #the 3 lines of code below will just increase the length of the snake once fruit is eaten
            copy_body.insert(0,copy_body[0] + self.direction)
            self.body = copy_body[:]
            self.new_block = False #this will limit it to one block of length
        else:
            copy_body = self.body[:-1] #the first and second movement of the head but removing the last movement
            copy_body.insert(0,copy_body[0] + self.direction) #current position of the snake head and the direction
            self.body = copy_body[:]

    def inc_block(self):#increases the length of the snake
        self.new_block = True

    def sound_played(self):
        self.crunch_sound.play()

    def reset(self):#brings the snake back to default position when the game is over
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)

#creating the fruit
class FRUIT:
    def __init__(self):
        self.randomise() # randomise the where the fruit will do

    def Fruit_draw(self):
        Fruit_rectangle = pygame.Rect(int(self.pos.x * Cell_Size), int(self.pos.y * Cell_Size), Cell_Size, Cell_Num)
        screen.blit(Apple,Fruit_rectangle)
        #pygame.draw.rect(screen, (153, 0, 76), Fruit_rectangle)

    def randomise(self):
        self.x = random.randint(0, Cell_Num - 1) # x position
        self.y = random.randint(0, Cell_Num - 1) # Y position
        self.pos = Vector2(self.x, self.y)
        


class Main_Base:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def Update(self):
        self.snake.Snake_Movement() #updates the game state
        self.match_check()#when the fruit it eaten it is to be reappeared elsewhere in the game screen
        self.fail_check()

        
    def draw_element(self): #simplied way of drawing the elements of the game
        self.draw_grass()
        self.fruit.Fruit_draw()
        self.snake.Snake_draw()
        self.Draw_Score()

    def match_check(self):
        if self.fruit.pos == self.snake.body[0]:#this is to check is the snake position is equal to the snake head
            self.fruit.randomise()
            self.snake.inc_block() #this will increase the length of the snake once the fruit is eaten
            self.snake.sound_played()
            
            for box in self.snake.body[1:]:
                if box == self.fruit.pos:
                    self.fruit.randomise()
            
    def fail_check(self): #this will somewhat check the end game states such as snake hits itself or the walls of the game
        if not 0 <= self.snake.body[0].x < Cell_Num or not 0 <= self.snake.body[0].y < Cell_Num:#this is to check if the R/L OR U/D for the walls are hit then game over
            self.Game_Over()

        for box in self.snake.body[1:]:#take all the elements that come after the head(1)
            if box == self.snake.body[0]:
                self.Game_Over()


    def Game_Over(self):
        self.snake.reset()


    def draw_grass(self):
        grass_colour = (251, 198, 207)
        for row in range(Cell_Num):
           if row % 2 == 0:
                for col in range(Cell_Num):# this will be drawing the grass in that certain pattern
                    if col % 2 == 0:
                        grass_rectangle = pygame.Rect(col * Cell_Size,row * Cell_Size,Cell_Size,Cell_Size)
                        pygame.draw.rect(screen, grass_colour, grass_rectangle)
           else:
               for col in range(Cell_Num):# this will be drawing the grass in that certain pattern
                   if col % 2 != 0:
                       grass_rectangle = pygame.Rect(col * Cell_Size,row * Cell_Size,Cell_Size,Cell_Size)
                       pygame.draw.rect(screen, grass_colour, grass_rectangle)
                
    def Draw_Score(self):
        score_text = str(len(self.snake.body) - 3)#this gets the score for every length of the snake, 3 is removed as default is the snake size at start of the game
        score_surface = Game_Font.render(score_text,True,(231,84,128))
        score_X = int(Cell_Size * Cell_Num - 60) #remove some pixels (60)
        score_Y = int(Cell_Size * Cell_Num - 40) #both above and this line of code is the position of the score
        score_rect = score_surface.get_rect(center = (score_X,score_Y))
        Apple_rect = Apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(Apple_rect.left, Apple_rect.top, Apple_rect.width + score_rect.width + 6,Apple_rect.height)

        pygame.draw.rect(screen,(251,188,184),bg_rect)#the rectangle to stand out the score
        screen.blit(score_surface,score_rect)
        #this is positioning the an apple next to the score to make it stand out
        screen.blit(Apple, Apple_rect)
        pygame.draw.rect(screen,(231,84,128),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)#this helps to not delay the sound of the crunch when apple is eaten
pygame.init()
Cell_Size = 40
Cell_Num = 20
screen = pygame.display.set_mode((Cell_Num * Cell_Size, Cell_Num * Cell_Size)) #size of the window
speed_clock = pygame.time.Clock() #keeps the consistency of how fast the program runs on all computers
Apple = pygame.image.load('Snake game/apple.png').convert_alpha()#brings out the image for the apple
Game_Font = pygame.font.Font(None, 25)  

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


Main_Game = Main_Base()


while True:
    #draw all the elements (background, snake, fruit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            Main_Game.Update() #updates the game state
        if event.type == pygame.KEYDOWN: #this is going to be triggered anytime the keyboard is used
            if event.key == pygame.K_UP: #key upwards
                if Main_Game.snake.direction.y != 1:
                     Main_Game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN: #key downwards
                if Main_Game.snake.direction.y != -1:
                     Main_Game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT: #key right
                if Main_Game.snake.direction.x != -1:
                     Main_Game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT: #key left
                if Main_Game.snake.direction.x != 1:
                     Main_Game.snake.direction = Vector2(-1, 0)
            
            



    screen.fill((255,182,193)) #colour of the initial background
    Main_Game.draw_element()
    pygame.display.update()
    speed_clock.tick(60)
