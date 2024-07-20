import pygame
import time
import random
import os

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
pink = (255, 105, 180)
gray = (169, 169, 169)
light_blue = (173, 216, 230)
dark_green = (0, 100, 0)

# Dynamic backgrounds
background_colors = [blue, (70, 130, 180), (100, 149, 237), (135, 206, 235), light_blue, gray, dark_green]
current_background = 0

# Snake color
snake_color = black

# Set the initial snake speed
initial_speed = 15
snake_speed = initial_speed

# Set the snake block size
snake_block = 10

# Load sounds
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
level_up_sound = pygame.mixer.Sound("level_up.wav")
power_up_sound = pygame.mixer.Sound("power_up.wav")
button_click_sound = pygame.mixer.Sound("button_click.wav")
background_music = pygame.mixer.music.load("background_music.mp3")

# Set the font style and size
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 25)

# Function to display the score
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Function to draw the snake
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(screen, snake_color, [x[0], x[1], snake_block, snake_block])

# Function to display the message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

# Add a global variable for high score
high_score = 0

# Load high score from file
def load_high_score():
    global high_score
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())

# Save high score to file
def save_high_score():
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

# Function to update the high score
def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        save_high_score()

# Function to display the high score
def display_high_score():
    value = score_font.render("High Score: " + str(high_score), True, white)
    screen.blit(value, [screen_width - 200, 0])

# Function to reset the game
def reset_game():
    global Length_of_snake, snake_speed, start_time, current_background, controls
    update_high_score(Length_of_snake - 1)
    snake_speed = initial_speed
    start_time = time.time()
    current_background = 0
    controls = load_controls()
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

# Start screen function with instructions
def start_screen():
    screen.fill(background_colors[current_background])
    message("Welcome to Snake Game!", yellow)
    instructions = [
        "Press S to Start",
        "Use Arrow Keys to Move",
        "Press P to Pause",
        "Eat green food to grow",
        "Avoid purple obstacles",
        "Orange food changes speed",
        "Pink food for power-ups",
        "Press O for Options"
    ]
    y_offset = screen_height / 3 + 50
    for line in instructions:
        instr = score_font.render(line, True, white)
        screen.blit(instr, [screen_width / 6, y_offset])
        y_offset += 30
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
                elif event.key == pygame.K_o:
                    options_menu()

# Pause menu function
def pause_menu():
    paused = True
    menu_options = ["Resume (Press P)", "Restart (Press R)", "Quit (Press Q)"]
    screen.fill(background_colors[current_background])
    y_offset = screen_height / 3
    for option in menu_options:
        opt = score_font.render(option, True, yellow)
        screen.blit(opt, [screen_width / 6, y_offset])
        y_offset += 50
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Function to draw special food
def draw_special_food(x, y, color):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])

# Function to display timer
def display_timer(start_time):
    elapsed_time = int(time.time() - start_time)
    timer_text = score_font.render("Time: " + str(elapsed_time), True, white)
    screen.blit(timer_text, [screen_width - 200, 30])

# Function to display game over statistics
def game_over_screen(score, time_elapsed):
    screen.fill(background_colors[current_background])
    message("Game Over!", red)
    stats = [
        f"Score: {score}",
        f"Time: {time_elapsed} seconds",
        f"High Score: {high_score}"
    ]
    y_offset = screen_height / 3 + 50
    for stat in stats:
        stat_text = score_font.render(stat, True, white)
        screen.blit(stat_text, [screen_width / 6, y_offset])
        y_offset += 30
    menu_options = ["Restart (Press R)", "Quit (Press Q)"]
    for option in menu_options:
        opt = score_font.render(option, True, yellow)
        screen.blit(opt, [screen_width / 6, y_offset])
        y_offset += 50
    pygame.display.update()
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Function to change snake color
def change_snake_color():
    global snake_color
    colors = [black, red, green, yellow, blue, purple, orange, pink]
    snake_color = random.choice(colors)

# Function to load custom controls
def load_controls():
    default_controls = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "pause": pygame.K_p,
        "change_color": pygame.K_c
    }
    if os.path.exists("controls.txt"):
        with open("controls.txt", "r") as file:
            controls = eval(file.read())
    else:
        controls = default_controls
    return controls

# Function to save custom controls
def save_controls(controls):
    with open("controls.txt", "w") as file:
        file.write(str(controls))

# Function to handle control customization
def customize_controls():
    screen.fill(background_colors[current_background])
    message("Customize Controls", yellow)
    instructions = [
        "Press the key for each action",
        "Move Left (Press L)",
        "Move Right (Press R)",
        "Move Up (Press U)",
        "Move Down (Press D)",
        "Pause (Press P)",
        "Change Color (Press C)"
    ]
    y_offset = screen_height / 3 + 50
    for line in instructions:
        instr = score_font.render(line, True, white)
        screen.blit(instr, [screen_width / 6, y_offset])
        y_offset += 30
    pygame.display.update()

    controls = load_controls()
    key_map = {
        pygame.K_l: "left",
        pygame.K_r: "right",
        pygame.K_u: "up",
        pygame.K_d: "down",
        pygame.K_p: "pause",
        pygame.K_c: "change_color"
    }
    key_selected = None

    while key_selected is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for key, action in key_map.items():
                    if event.key == key:
                        key_selected = action
                        break
                if key_selected:
                    key_selected = None
                    for action in controls.keys():
                        if action != key_selected:
                            controls[action] = event.key
                            save_controls(controls)
                            break

# Function to draw power-ups
def draw_power_up(x, y, color):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])

# Function to create power-ups
def create_power_up():
    power_up_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    power_up_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
    return power_up_x, power_up_y

# Function to apply power-ups
def apply_power_up(effect, duration):
    global snake_speed, power_up_active, power_up_end_time
    if effect == "invincibility":
        snake_speed += 10  # Increase speed
    elif effect == "double_score":
        snake_speed += 5  # Increase speed
    power_up_active = effect
    power_up_end_time = time.time() + duration

# Function to reset power-up effects
def reset_power_up_effects():
    global snake_speed, power_up_active
    if power_up_active == "invincibility":
        snake_speed -= 10
    elif power_up_active == "double_score":
        snake_speed -= 5
    power_up_active = None

# Initialize power-up variables
power_up_x, power_up_y = create_power_up()
power_up_active = None
power_up_end_time = 0

# Main game loop
def gameLoop():
    global high_score, Length_of_snake, snake_speed, start_time, current_background, controls, power_up_x, power_up_y, power_up_active, power_up_end_time
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    special_food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    special_food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    obstacles = create_obstacles(5)
    level = 1
    start_time = time.time()
    controls = load_controls()

    while not game_over:

        while game_close == True:
            game_over_screen(Length_of_snake - 1, int(time.time() - start_time))
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == controls["left"]:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == controls["right"]:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == controls["up"]:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == controls["down"]:
                    x1_change = 0
                    y1_change = snake_block
                elif event.key == controls["pause"]:
                    pause_menu()
                elif event.key == controls["change_color"]:
                    change_snake_color()

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            pygame.mixer.Sound.play(game_over_sound)
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(background_colors[current_background])
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        draw_special_food(special_food_x, special_food_y, orange)
        draw_power_up(power_up_x, power_up_y, pink)
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
        display_timer(start_time)

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            # Increase the level and speed every 5 food items eaten
            if Length_of_snake % 5 == 0:
                level += 1
                pygame.mixer.Sound.play(level_up_sound)
                snake_speed += 5
                current_background = (current_background + 1) % len(background_colors)
                obstacles = create_obstacles(level + 4)

        if x1 == special_food_x and y1 == special_food_y:
            pygame.mixer.Sound.play(power_up_sound)
            special_food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            special_food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

            # Apply speed boost or slow down
            if random.choice([True, False]):
                snake_speed += 5
            else:
                snake_speed = max(10, snake_speed - 5)

        if x1 == power_up_x and y1 == power_up_y:
            pygame.mixer.Sound.play(power_up_sound)
            power_up_x, power_up_y = create_power_up()
            apply_power_up(random.choice(["invincibility", "double_score"]), 10)

        if power_up_active and time.time() > power_up_end_time:
            reset_power_up_effects()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Create a clock object
clock = pygame.time.Clock()

# Load high score
load_high_score()

# Show the start screen
start_screen()

# Run the game
gameLoop()
