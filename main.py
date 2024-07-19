import pygame
import time
import random

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Set the width and height of the screen (window)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
orange = (255, 165, 0)

# Set the initial snake speed
initial_speed = 15
snake_speed = initial_speed

# Set the snake block size
snake_block = 10

# Load sounds
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Set the font style and size
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Function to display the score
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Function to draw the snake
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Function to display the message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

# Add a global variable for high score
high_score = 0

# Function to update the high score
def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score

# Function to display the high score
def display_high_score():
    value = score_font.render("High Score: " + str(high_score), True, white)
    screen.blit(value, [screen_width - 200, 0])

# Function to reset the game
def reset_game():
    global Length_of_snake, snake_speed
    update_high_score(Length_of_snake - 1)
    snake_speed = initial_speed
    gameLoop()

# Function to draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, purple, [obstacle[0], obstacle[1], snake_block, snake_block])

# Function to create obstacles
def create_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        obstacle_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
        obstacle_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
        obstacles.append([obstacle_x, obstacle_y])
    return obstacles

# Start screen function
def start_screen():
    screen.fill(blue)
    message("Welcome to Snake Game! Press S to Start", yellow)
    pygame.display.update()
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start = True

# Pause function
def pause_game():
    paused = True
    message("Paused. Press P to Resume", yellow)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# Function to draw special food
def draw_special_food(x, y, color):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])

# Main function with added functionality
def gameLoop():
    global Length_of_snake, snake_speed
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Create food at random position
    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    # Create special food at random position
    special_food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    special_food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    # Create obstacles
    obstacles = create_obstacles(5)

    # Set initial level
    level = 1

    while not game_over:

        while game_close == True:
            screen.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            Your_score(Length_of_snake - 1)
            display_high_score()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_p:
                    pause_game()

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            pygame.mixer.Sound.play(game_over_sound)
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        draw_special_food(special_food_x, special_food_y, orange)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        for obstacle in obstacles:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        our_snake(snake_block, snake_List)
        draw_obstacles(obstacles)
        Your_score(Length_of_snake - 1)
        display_high_score()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            # Increase the level and speed every 5 food items eaten
            if Length_of_snake % 5 == 0:
                level += 1
                snake_speed += 5
                obstacles = create_obstacles(level + 4)

        if x1 == special_food_x and y1 == special_food_y:
            pygame.mixer.Sound.play(eat_sound)
            special_food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            special_food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

            # Apply speed boost or slow down
            if random.choice([True, False]):
                snake_speed += 5
            else:
                snake_speed = max(10, snake_speed - 5)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Create a clock object
clock = pygame.time.Clock()

# Show the start screen
start_screen()

# Run the game
gameLoop()
