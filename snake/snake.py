import pygame, sys, random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (170, 200, 100)
DARK_GREEN = (40, 50, 25)
cell_size = 25
num_of_cells = 20

BOARDER_LEN = 75
screen = pygame.display.set_mode((cell_size * num_of_cells + 2 * BOARDER_LEN, cell_size * num_of_cells + 2 * BOARDER_LEN))

pygame.display.set_caption('RETRO SNAKE!')

clock = pygame.time.Clock()

#food class 
class Food:
    
    def __init__(self):
        self.position = self.rand_pos()

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size + BOARDER_LEN, self.position.y * cell_size + BOARDER_LEN, cell_size, cell_size)
        #pygame.draw.rect(screen, DARK_GREEN, food_rect)
        screen.blit(food_surface, food_rect)
        
    
    def rand_pos(self):
        x = random.randint(0, num_of_cells-1)
        y = random.randint(0, num_of_cells-1)
        position = Vector2(x, y)
        return position

#snake class
class Snake:
    
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)
        self.add_seg = False
        self.eat_s = pygame.mixer.Sound("snake/snake/eat.mp3")
        self.wall_s = pygame.mixer.Sound("snake/snake/wall.mp3")
    
    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(segment.x * cell_size + BOARDER_LEN, segment.y * cell_size + BOARDER_LEN, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0 , 7)  #7 for boarder radius of rectabgle
    
    def update(self):
        self.body.insert(0, self.body[0] + self.direction) #adds the new cell
        if self.add_seg ==  True:
            self.add_seg = False
        else:  
            self.body = self.body[:-1] #removes the last cell
    
    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)
     
 
class Game:
    
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.state = "Running"
        self.score = 0
    def draw(self):
        self.food.draw()
        self.snake.draw()
    
    def update(self):
        if self.state == "Running":
            self.snake.update()
            self.coll_with_food()
            self.coll_with_edge()
            self.coll_with_tail()
        
    def coll_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.rand_pos()
            self.snake.add_seg = True
            self.score = self.score + 1
            self.snake.eat_s.play()
    
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.rand_pos()
        self.state = "Stopped"
        self.score = 0
        self.snake.wall_s.play()
        
    def coll_with_edge(self):
        if self.snake.body[0].x == num_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == num_of_cells or self.snake.body[0].y == -1:
            self.game_over()
        
    
    def coll_with_tail(self):
        for seg in self.snake.body[1:]: #checks if the head hits the tail
            if seg == self.snake.body[0]:
                self.game_over()
    
#food = Food() before having Game class
food_surface = pygame.image.load("snake/snake/food.png") #returns a surface that contains the img

#snake = Snake() before having Game class
SNAKE_UPDATE = pygame.USEREVENT #creates an event
pygame.time.set_timer(SNAKE_UPDATE, 200)  #triggers the event every 200 ms

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE: 
            game.update() #position only gets updated when the event is triggered
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if game.state == "Stopped":  #restart by pressing any key
                game.state = "Running"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
    
    screen.fill(GREEN) #painting the background
    pygame.draw.rect(screen, DARK_GREEN, (BOARDER_LEN-5, BOARDER_LEN-5, cell_size *num_of_cells + 10, cell_size *num_of_cells + 10), 5)
    #drawing
   # food.draw()  #drawing the food by calling the draw method of the food obj
    #snake.draw() #drawing the snake
    game.draw()
    #title 
    title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
    screen.blit(title_surface, (BOARDER_LEN-5, 20))
    #score 
    score_surface = title_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(score_surface, (BOARDER_LEN+400, 20))
    pygame.display.update()
    clock.tick(60) #runs the loop 60 times per sec