import pygame
import time
import random
import os
import json

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
    while paused:
        screen.fill(black)
        message("Paused", white, -100, size="large")
        message("Press C to Continue", white, -50)
        message("Press Q to Quit", white, 0)
        message("Press S for Save/Load", white, 50)
        message("Press L to View Leaderboard", white, 100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_s:
                    save_load_menu()
                elif event.key == pygame.K_l:
                    display_leaderboard()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Function to draw special food
def draw_special_food(x, y, color):
    pygame.draw.rect(screen, color, [x, y, snake_block, snake_block])

# Function to load achievements
def load_achievements():
    try:
        with open("achievements.json", "r") as achievements_file:
            achievements = json.load(achievements_file)
    except FileNotFoundError:
        achievements = {
            "First Food": False,
            "10 Foods": False,
            "20 Foods": False,
            "First Special Food": False,
            "Speed Boost": False,
            "Invincibility": False
        }
    return achievements

# Function to save achievements
def save_achievements(achievements):
    with open("achievements.json", "w") as achievements_file:
        json.dump(achievements, achievements_file)

# Function to check and unlock achievements
def check_achievements(score, achievements, snake_speed):
    if score >= 1 and not achievements["First Food"]:
        achievements["First Food"] = True
        display_achievement("First Food")
    if score >= 10 and not achievements["10 Foods"]:
        achievements["10 Foods"] = True
        display_achievement("10 Foods")
    if score >= 20 and not achievements["20 Foods"]:
        achievements["20 Foods"] = True
        display_achievement("20 Foods")
    if snake_speed > 15 and not achievements["Speed Boost"]:
        achievements["Speed Boost"] = True
        display_achievement("Speed Boost")
    if power_up_active and not achievements["Invincibility"]:
        achievements["Invincibility"] = True
        display_achievement("Invincibility")

# Function to display achievement notifications
def display_achievement(achievement):
    screen.fill(black)
    message(f"Achievement Unlocked: {achievement}", yellow, 0, size="large")
    pygame.display.update()
    pygame.time.delay(2000)

# Function to display timer
def display_timer(start_time):
    elapsed_time = int(time.time() - start_time)
    timer_text = score_font.render("Time: " + str(elapsed_time), True, white)
    screen.blit(timer_text, [screen_width - 200, 30])

# Function to display game over statistics
def game_over_screen(score, duration):
    screen.fill(black)
    message("Game Over", red, -50, size="large")
    message(f"Score: {score}", white, 0)
    message(f"Time: {duration} seconds", white, 50)
    message("Press Q to Quit", white, 100)
    message("Press R to Restart", white, 150)
    message("Press L to View Leaderboard", white, 200)
    pygame.display.update()

    # Update leaderboard
    player_name = "Player"  # Replace with actual player name if available
    update_leaderboard({"name": player_name, "score": score})

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    gameLoop()
                elif event.key == pygame.K_l:
                    display_leaderboard()
            if event.type == pygame.QUIT:
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

# Function to save the game state
def save_game():
    game_state = {
        "x1": x1,
        "y1": y1,
        "x1_change": x1_change,
        "y1_change": y1_change,
        "snake_List": snake_List,
        "Length_of_snake": Length_of_snake,
        "foodx": foodx,
        "foody": foody,
        "special_food_x": special_food_x,
        "special_food_y": special_food_y,
        "obstacles": obstacles,
        "level": level,
        "snake_speed": snake_speed,
        "start_time": start_time,
        "current_background": current_background,
        "power_up_x": power_up_x,
        "power_up_y": power_up_y,
        "power_up_active": power_up_active,
        "power_up_end_time": power_up_end_time,
        "high_score": high_score,
        "controls": controls
    }
    with open("save_game.json", "w") as save_file:
        json.dump(game_state, save_file)

# Function to load the game state
def load_game():
    global x1, y1, x1_change, y1_change, snake_List, Length_of_snake, foodx, foody, special_food_x, special_food_y
    global obstacles, level, snake_speed, start_time, current_background, power_up_x, power_up_y, power_up_active, power_up_end_time
    global high_score, controls
    
    try:
        with open("save_game.json", "r") as save_file:
            game_state = json.load(save_file)
            x1 = game_state["x1"]
            y1 = game_state["y1"]
            x1_change = game_state["x1_change"]
            y1_change = game_state["y1_change"]
            snake_List = game_state["snake_List"]
            Length_of_snake = game_state["Length_of_snake"]
            foodx = game_state["foodx"]
            foody = game_state["foody"]
            special_food_x = game_state["special_food_x"]
            special_food_y = game_state["special_food_y"]
            obstacles = game_state["obstacles"]
            level = game_state["level"]
            snake_speed = game_state["snake_speed"]
            start_time = game_state["start_time"]
            current_background = game_state["current_background"]
            power_up_x = game_state["power_up_x"]
            power_up_y = game_state["power_up_y"]
            power_up_active = game_state["power_up_active"]
            power_up_end_time = game_state["power_up_end_time"]
            high_score = game_state["high_score"]
            controls = game_state["controls"]
    except FileNotFoundError:
        print("No saved game found!")

# Function to display the save/load menu
def save_load_menu():
    menu = True
    while menu:
        screen.fill(black)
        message("Save/Load Game", white, -50, size="large")
        message("S - Save Game", white, 0)
        message("L - Load Game", white, 50)
        message("B - Back to Game", white, 100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_game()
                    menu = False
                elif event.key == pygame.K_l:
                    load_game()
                    menu = False
                elif event.key == pygame.K_b:
                    menu = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Function to load the leaderboard
def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as leaderboard_file:
            leaderboard = json.load(leaderboard_file)
    except FileNotFoundError:
        leaderboard = []
    return leaderboard

# Function to save the leaderboard
def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as leaderboard_file:
        json.dump(leaderboard, leaderboard_file)

# Function to update the leaderboard
def update_leaderboard(new_score):
    leaderboard = load_leaderboard()
    leaderboard.append(new_score)
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_leaderboard(leaderboard)

# Function to display the leaderboard
def display_leaderboard():
    leaderboard = load_leaderboard()
    screen.fill(black)
    message("Leaderboard", white, -100, size="large")
    y_offset = -50
    for index, entry in enumerate(leaderboard):
        message(f"{index + 1}. {entry['name']} - {entry['score']}", white, y_offset)
        y_offset += 30
    message("Press B to go back", white, y_offset + 50)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Function to display the settings menu
def settings_menu():
    settings_running = True
    selected_option = 0
    options = ["Change Snake Color", "Change Background Color", "Toggle Sound", "Back to Main Menu"]
    colors = [white, yellow, red, blue, green, orange, purple, pink]
    backgrounds = [black, gray, dark_gray, navy, olive, maroon]

    while settings_running:
        screen.fill(black)
        for i, option in enumerate(options):
            color = yellow if i == selected_option else white
            message(option, color, i - 2, size="medium")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Change Snake Color":
                        change_snake_color_menu(colors)
                    elif options[selected_option] == "Change Background Color":
                        change_background_color_menu(backgrounds)
                    elif options[selected_option] == "Toggle Sound":
                        toggle_sound()
                    elif options[selected_option] == "Back to Main Menu":
                        settings_running = False

# Function to display and handle the snake color change menu
def change_snake_color_menu(colors):
    color_menu_running = True
    selected_color = 0

    while color_menu_running:
        screen.fill(black)
        for i, color in enumerate(colors):
            rect_color = color
            text_color = white if i != selected_color else yellow
            pygame.draw.rect(screen, rect_color, [screen_width // 2 - 50, screen_height // 2 + (i * 30) - 100, 100, 30])
            message(f"Color {i + 1}", text_color, i - 3, size="medium")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_color = (selected_color - 1) % len(colors)
                elif event.key == pygame.K_DOWN:
                    selected_color = (selected_color + 1) % len(colors)
                elif event.key == pygame.K_RETURN:
                    snake_color = colors[selected_color]
                    color_menu_running = False

# Function to display and handle the background color change menu
def change_background_color_menu(backgrounds):
    background_menu_running = True
    selected_background = 0

    while background_menu_running:
        screen.fill(black)
        for i, background in enumerate(backgrounds):
            rect_color = background
            text_color = white if i != selected_background else yellow
            pygame.draw.rect(screen, rect_color, [screen_width // 2 - 50, screen_height // 2 + (i * 30) - 100, 100, 30])
            message(f"Background {i + 1}", text_color, i - 3, size="medium")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_background = (selected_background - 1) % len(backgrounds)
                elif event.key == pygame.K_DOWN:
                    selected_background = (selected_background + 1) % len(backgrounds)
                elif event.key == pygame.K_RETURN:
                    current_background = backgrounds[selected_background]
                    background_menu_running = False

def main_menu():
    menu_running = True
    selected_option = 0
    options = ["Start Game", "Settings", "Leaderboard", "Quit"]

    while menu_running:
        screen.fill(black)
        for i, option in enumerate(options):
            color = yellow if i == selected_option else white
            message(option, color, i - 2, size="medium")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_option] == "Start Game":
                        gameLoop()
                    elif options[selected_option] == "Settings":
                        settings_menu()
                    elif options[selected_option] == "Leaderboard":
                        display_leaderboard()
                    elif options[selected_option] == "Quit":
                        pygame.quit()
                        quit()

# Function to toggle sound on and off
def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

# Function to load levels
def load_levels():
    try:
        with open("levels.json", "r") as levels_file:
            levels = json.load(levels_file)
    except FileNotFoundError:
        levels = [
            {
                "obstacles": [],
                "food_speed": 10,
                "snake_speed": 15
            },
            {
                "obstacles": [(100, 100), (200, 200), (300, 300)],
                "food_speed": 10,
                "snake_speed": 20
            },
            {
                "obstacles": [(150, 150), (250, 250), (350, 350), (450, 450)],
                "food_speed": 8,
                "snake_speed": 25
            }
        ]
    return levels

# Function to display level transition
def display_level_transition(level):
    screen.fill(black)
    message(f"Level {level + 1}", white, 0, size="large")
    pygame.display.update()
    pygame.time.delay(3000)

# Function to start the next level
def start_next_level(level, levels):
    global obstacles, snake_speed, food_speed

    obstacles = levels[level]["obstacles"]
    snake_speed = levels[level]["snake_speed"]
    food_speed = levels[level]["food_speed"]
    display_level_transition(level)

# Main loop
def gameLoop():
    global high_score, Length_of_snake, snake_speed, start_time, current_background, controls, power_up_x, power_up_y, power_up_active, power_up_end_time
    global x1, y1, x1_change, y1_change, snake_List, foodx, foody, special_food_x, special_food_y, obstacles, level, food_speed

    game_over = False
    game_close = False

    levels = load_levels()
    level = 0
    start_next_level(level, levels)

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

    start_time = time.time()
    controls = load_controls()
    achievements = load_achievements()

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
                if level < len(levels):
                    start_next_level(level, levels)
                else:
                    # Game completed
                    screen.fill(black)
                    message("Congratulations! You completed all levels!", yellow, 0, size="large")
                    pygame.display.update()
                    pygame.time.delay(5000)
                    game_over = True

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

        check_achievements(Length_of_snake - 1, achievements, snake_speed)
        save_achievements(achievements)
        
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
