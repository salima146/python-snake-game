import pygame, sys, random
from pygame.math import Vector2


#creating the snake
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def Snake_draw(self):
        for box in self.body:
            X_position = int(box.x * Cell_Size)
            Y_position = int(box.y * Cell_Size)         
            box_rectangle = pygame.Rect(X_position, Y_position, Cell_Size, Cell_Size)
            pygame.draw.rect(screen, (153, 109, 115), box_rectangle)

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



            

#creating the fruit
class FRUIT:
    def __init__(self):
        self.randomise() # randomise the where the fruit will do

    def Fruit_draw(self):
        Fruit_rectangle = pygame.Rect(int(self.pos.x * Cell_Size), int(self.pos.y * Cell_Size), Cell_Size, Cell_Num)
        pygame.draw.rect(screen, (153, 0, 76), Fruit_rectangle)

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
        self.fruit.Fruit_draw()
        self.snake.Snake_draw()

    def match_check(self):
        if self.fruit.pos == self.snake.body[0]:#this is to check is the snake position is equal to the snake head
            self.fruit.randomise()
            self.snake.inc_block() #this will increase the length of the snake once the fruit is eaten

    def fail_check(self): #this will somewhat check the end game states such as snake hits itself or the walls of the game
        if not 0 <= self.snake.body[0].x < Cell_Num or not 0 <= self.snake.body[0].y < Cell_Num:#this is to check if the R/L OR U/D for the walls are hit then game over
            self.Game_Over()

        for box in self.snake.body[1:]:#take all the elements that come after the head(1)
            if box == self.snake.body[0]:
                self.Game_Over()




    def Game_Over(self):
        pygame.quit()
        sys.exit()


pygame.init()
Cell_Size = 40
Cell_Num = 20
screen = pygame.display.set_mode((Cell_Num * Cell_Size, Cell_Num * Cell_Size)) #size of the window
speed_clock = pygame.time.Clock() #keeps the consistency of how fast the program runs on all computers

  

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
