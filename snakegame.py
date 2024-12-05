# Final Project - Snake Game 
import pygame
import time 
import random 

print("hello")
# initialize pygame
pygame.init()

# define colors using RGB format 
white = (255,255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# define display size
display_width = 800
display_height = 800

# create display board for the game window
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# define clock and snake parameters
clock = pygame.time.Clock()
snake_block = 40  # snake is 10x10 
snake_speed = 6

# define fonts for score and messages 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# function to display the score
def display_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    game_display.blit(value, [0, 0])
    
# Load Images 
# Image of snake head 
snake_head_img = pygame.image.load('snakehead.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
# Image of obstacle 
obstacle_img = pygame.image.load('obstacle.png').convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (snake_block, snake_block))
# Image of apple 
apple_img = pygame.image.load('apple.jpeg').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

game_display.blit(snake_head_img,(50, 50)) 

# function to draw the snake on the screen 
def draw_snake(snake_block, snake_list):
    print(snake_list)
    # Draw the head with the loaded image
    game_display.blit(snake_head_img, (snake_list[-1][0], snake_list[-1][1])) # Draw head 
    # Draw the body segments as green rectangles 
    for x in snake_list[:-1]:
        pygame.draw.ellipse(game_display, green, [x[0], x[1], snake_block, snake_block])

# function to display messages on the screen 
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [display_width / 6, display_height / 3])

# function to update the snake's position 
def update(my_list, x, y, length):
    # create snake head with current x , y 
    snake_head = []
    snake_head.append(x)
    snake_head.append(y)
    # add snake head to list 
    my_list.append(snake_head)
    # my_list = snake_head.append(my_list)
    # remove last segment if snake length exceeds current length 
    if len(my_list) > length:
        del my_list[0]

def detect_collision():
    pass 

# funcation to generate random coordinates for food and obstacles 
def generate_coord():
    x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    return (x,y)

# Function to draw obstacles with an image 
def draw_obstacle(x, y):
    # print("draw obstacle", x, y)
    game_display.blit(obstacle_img, (x, y))

# main game loop 
def game_loop():
    game_over = False # main game state
    # game_close = False
    
    #initialize snake starting position 
    x1 = display_width / 2 
    y1 = display_height / 2
    
    #initialize movement direction 
    x1_change = 0
    y1_change = 0 
    
    snake_list = [] # list to store snake segments 
    length_of_snake = 1 #initial length of the snake 
    
    # generate random placement for food 
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    
    # initial obstacle list with one obstacle 
    obstacle_list = []
    # static coordinates for obstacles
    obstacle_list.append(generate_coord())
    while not game_over:
        
        # handle keypresses for snake movement 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit game if window is closed 
                game_over = True 
            if event.type == pygame.KEYDOWN: # use arrow keys for direction 
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0 
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0 
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0 
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0 
        
        # check for boundary collision 
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            break
        # update snake position 
        x1 += x1_change
        y1 += y1_change
        game_display.fill(black) # clear screen
        
        # draw the food on the screen 
        # pygame.draw.rect(game_display, blue, [foodx, foody, snake_block, snake_block])
        game_display.blit(apple_img, (foodx, foody)) # Draw head 
        
        # draw obstacles
        for pair in obstacle_list:
            ox = pair[0]
            oy = pair[1]
            draw_obstacle(ox, oy)
        
        # update the snake position and check for collisions 
        snake_head = []
        update(snake_list, x1, y1, length_of_snake)
        
        # check for collisions with the snake's own body
        for x in snake_list[:-1]:
            if x == snake_head:
                break
                
        over = False
        #  check if snake collides w obstacle
        for each_pair in obstacle_list:
            x = each_pair[0]
            y = each_pair[1]     
            if x1 == x and y1 == y:
                over = True
        if over == True:
            break
        
        # draw snake and display score       
        draw_snake(snake_block, snake_list)
        display_score(length_of_snake -1)
        
        # upgrade display
        pygame.display.update()
        print()
        # check if snake eats food
        if x1 == foodx and y1 == foody:
            # generate new food position and increase snake length 
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1 
        
       
        # if the length of the snake is evenly divisible by 3:
        if length_of_snake % 3 == 0: # the snake has eaten 3 foods 
            if len(obstacle_list) <= length_of_snake//3: # ensuring the length of snake to obstacles is 3:1 
                obstacle_list.append(generate_coord())
            # pass
        
            # add to obstacle list
            
            # call draw obstacle on new coordinate
        
        clock.tick(snake_speed)
    
    # display game over message and score when the game is lost 
    game_display.fill(blue)
    display_message("You lost! Press Q-Quit or C-Play Again", red)
    display_score(length_of_snake - 1)
    pygame.display.update()
    # handle user input after the game is over 
    while True:
        for event in pygame.event.get():
            # print("dsfghjkl;")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # restart game 
                    game_over = False
                    game_loop()
                elif event.key == pygame.K_q: # quit game 
                    pygame.quit()
                    quit()


draw_obstacle(0,0)
# start the game
game_loop()
# quit()
