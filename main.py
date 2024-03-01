import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
FPS = 60
WIDTH = 800
HEIGHT = 600
font = pygame.font.SysFont("Arial", 48)
input_font = pygame.font.SysFont("Stengazeta Regular", 36)
guess_font = pygame.font.SysFont("Stengazeta Regular", 36)
alert_font = pygame.font.SysFont("Stengazeta Regular", 28)
lives_font = pygame.font.SysFont("Stengazeta Regular", 36)
restart_font = pygame.font.SysFont("Stengazeta Regular", 40)
backtomenu_font = pygame.font.SysFont("Stengazeta Regular", 40)

lose_sound = pygame.mixer.Sound('lose.mp3')

pygame.display.set_caption('Guess The Number')
pygame.display.set_icon(pygame.image.load('logo.jpg'))

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_image = pygame.image.load("bg.png")
guessing_scene_image = pygame.image.load("game.png")

heart_image = pygame.image.load("heart.png")
heart_image_width, heart_image_height = heart_image.get_size()
desired_heart_width = 21
desired_heart_height = 21
scaled_heart_image = pygame.transform.scale(heart_image, (desired_heart_width, desired_heart_height))

location = "MAIN_MENU"
mouse_loc = (0, 0)
left_click = False
right_click = False

play_btn_rect = pygame.Rect(349, 316, 102, 50)
back_btn_rect = pygame.Rect(349, 316, 102, 50)

MINIMUM_NUMBER = 1 # Enter minimum number
MAXIMUM_NUMBER = 2 # Enter maximum number
max_attempts = 20 # Enter amount of lives
num_lives = max_attempts
max_hearts_per_row = 20

game_over = False

user_input = ""
feedback_message = ""


def draw_text(surface, text, font, color, pos):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (WIDTH - text_surface.get_width() / 2 - WIDTH / 2 + pos[0], pos[1]))


def draw_hearts(surface, num_lives, pos):
    rows = num_lives // max_hearts_per_row + 1
    row_height = heart_image_height + 5

    for row in range(rows):
        x_offset = WIDTH - (WIDTH / 2) - (num_lives * (desired_heart_width + 2)) / 2 - desired_heart_height
        y_offset = pos[1] + row * row_height

        for i in range(min(max_hearts_per_row, num_lives)):
            x_offset += desired_heart_width + 2
            if x_offset < WIDTH:
                surface.blit(scaled_heart_image, (x_offset, y_offset))
                num_lives -= 1


restart_btn_rect = pygame.Rect(340, 480, 200, 50)
back_to_menu_btn_rect = pygame.Rect(340, 540, 200, 50)


def draw_restart_buttons():
    draw_text(screen, "Restart", restart_font, (0, 0, 0), (0, 480))
    draw_text(screen, "Back to Main Menu", backtomenu_font, (0, 0, 0), (0, 540))


def run_guessing_game():
    global user_input, feedback_message, location, num_lives, game_over
    num_lives = max_attempts
    game_over = False
    feedback_message = ""
    secret_number = random.randint(MINIMUM_NUMBER, MAXIMUM_NUMBER)
    pygame.mixer.music.load('suspense.mp3')
    pygame.mixer.music.play(-1)
    print("Welcome to the Guess the Number game!")
    print(f"You have {max_attempts} attempts to guess the secret number.")
    guess_text_rect = pygame.Rect(20, 20, WIDTH - 40, 30)
    user_input_surface = input_font.render("", True, (255, 255, 255))
    input_box_rect = pygame.Rect(205, 260, 400, 40)
    message_color = (0, 0, 0)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.TEXTINPUT:
                user_input += f"{event.text}"
                user_input_surface = input_font.render(user_input, True, (0, 0, 0))
                pygame.display.flip()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    user_input_surface = input_font.render(user_input, True, (0, 0, 0))
                    pygame.display.flip()

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                print(user_input)
                try:
                    user_guess = int(user_input)
                    if MINIMUM_NUMBER <= user_guess <= MAXIMUM_NUMBER:
                        if user_guess == secret_number:
                            if num_lives == max_attempts:
                                show_fireworks()
                            feedback_message = f"Congratulations! You guessed the number ({secret_number}) correctly!"
                            message_color = (0, 0, 0)
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("win.mp3")
                            pygame.mixer.music.play(fade_ms=1000)
                            draw_restart_buttons()
                            game_over = True
                        elif user_guess < secret_number:
                            feedback_message = "Too low! Try a higher number."
                            message_color = (0, 0, 255)
                            num_lives -= 1
                        else:
                            feedback_message = "Too high! Try a lower number."
                            message_color = (255, 0, 0)
                            num_lives -= 1
                            draw_text(screen, feedback_message, alert_font, (255, 255, 255), (295, 360))
                    else:
                        feedback_message = ("Invalid input or number out of range.")
                        num_lives -= 1
                except ValueError:
                    feedback_message = "Invalid input. Please enter a valid number."
                    num_lives -= 1
                user_input = ""

        if num_lives <= 0:
            game_over = True
            pygame.mixer.music.stop()
            lose_sound.play()  # Playing the losing sound
            feedback_message = "You're lost! Out of guesses! The secret number was " + str(secret_number)

        screen.fill((239, 12, 233))
        screen.blit(guessing_scene_image, (0, 0))
        draw_hearts(screen, num_lives, (600, 10))
        draw_text(screen, f"Guess the number between {MINIMUM_NUMBER} and {MAXIMUM_NUMBER}:", guess_font, (0, 0, 0),
                  (0, 195))
        pygame.draw.rect(screen, (0, 0, 0), input_box_rect, 2)
        screen.blit(user_input_surface, (input_box_rect.x + 10, input_box_rect.y + 7))
        draw_text(screen, feedback_message, alert_font, message_color, (0, 360))

        if (num_lives <= 0) or game_over:
            draw_restart_buttons()

        pygame.display.flip()

    return game_over


def show_fireworks():
    pygame.mixer.music.stop()
    num_particles = 1000
    particle_size = 1
    explosion_centers = [
        (0, 0),
        (WIDTH, 0),
        (0, HEIGHT),
        (WIDTH, HEIGHT)
    ]

    particles = []

    winning_sound = pygame.mixer.Sound('win.mp3')
    fireworks_sound = pygame.mixer.Sound('fireworks.mp3')

    for center in explosion_centers:
        for _ in range(int(num_particles / 4)):
            particle = {
                "x": center[0],
                "y": center[1],
                "dx": random.uniform(-5, 5),
                "dy": random.uniform(-5, 5),
                "color": (random.randint(200, 255), random.randint(0, 255), random.randint(0, 255))
            }
            particles.append(particle)

    # Animation loop
    running = True
    animation_duration = 7
    start_time = pygame.time.get_ticks()
    winning_sound_played = False
    fireworks_sound_played = False

    while running and (pygame.time.get_ticks() - start_time) / 1000 < animation_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for particle in particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]

            # Gravity simulation
            particle["dy"] += 0.1

            if particle["y"] > HEIGHT or particle["x"] < 0 or particle["x"] > WIDTH:
                particles.remove(particle)

        if not winning_sound_played:
            pygame.mixer.stop()
            winning_sound.play()
            winning_sound_played = True

        if not fireworks_sound_played:
            pygame.mixer.stop()
            fireworks_sound.play()
            fireworks_sound_played = True
        # Clearing the screen and draw the particles
        for particle in particles:
            pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), particle_size)

        pygame.display.flip()
        clock.tick(60)


restart_btn_rect = pygame.Rect(340, 480, 200, 50)
back_to_menu_btn_rect = pygame.Rect(340, 540, 200, 50)

while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_over = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if restart_btn_rect.collidepoint(event.pos):
                game_over = False
                run_guessing_game()
        elif back_to_menu_btn_rect.collidepoint(event.pos):
            game_over = True
            location = "MAIN_MENU"

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_loc = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True
                if game_over:
                    if restart_btn_rect.collidepoint(mouse_loc):
                        game_over = run_guessing_game()
                    elif back_to_menu_btn_rect.collidepoint(mouse_loc):
                        game_over = False
                        location = "MAIN_MENU"
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_click = False
                if location == "MAIN_MENU":
                    if play_btn_rect.collidepoint(mouse_loc):
                        location = "GAME"
                        game_over = run_guessing_game()

    if location == "MAIN_MENU":
        screen.blit(background_image, (0, 0))

    pygame.display.flip()

pygame.quit()
