import random

import pygame

pygame.init()
pygame.mixer.init()


# main entrance
WIDTH = 880
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Monster Battle")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (150, 150, 150)




#font
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Menu playing images
background_menu = pygame.image.load("background.png")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))

logo_game = pygame.image.load("logo-removebg-preview.png")
logo_game = pygame.transform.scale(logo_game, (500, 250))
logo_rect = logo_game.get_rect(center=(WIDTH / 2, HEIGHT / 3))


# buttons play
img_button_play = pygame.image.load("play-removebg-preview.png")
img_button_exit = pygame.image.load("exit-removebg-preview.png")

img_button_play = pygame.transform.scale(img_button_play, (200, 80))
img_button_exit = pygame.transform.scale(img_button_exit, (200, 80))

play_button_rect = img_button_play.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
exit_button_rect = img_button_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

#game over images
img_gameover = pygame.image.load("game_over-removebg-preview.png").convert_alpha()
img_golden_border = pygame.image.load("bordersssssss-removebg-preview.png").convert_alpha()
background_menu_3 = pygame.image.load("background.png")

img_golden_border = pygame.transform.scale(img_golden_border , (WIDTH - 40, HEIGHT - 40))
marco_rect = img_golden_border .get_rect(center=(WIDTH // 2, HEIGHT // 2))

img_gameover = pygame.transform.scale(img_gameover, (450, 150))
gameover_rect = img_gameover.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140))

img_retry = pygame.image.load("retry-removebg-preview.png").convert_alpha()
img_retry = pygame.transform.scale(img_retry, (180, 50))
retry_rect = img_retry.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))



#player during game
player_img = pygame.image.load("cohete-removebg-preview.png").convert_alpha()
acid_eyes_img = pygame.image.load("eye_enemy-removebg-preview.png").convert_alpha()
background_menu_2 = pygame.image.load("background.png")

#define_new_dimentions
player_size = (80, 80)
acid_eyes_size = (60, 60)

player_img = pygame.transform.scale(player_img, player_size)
acid_eyes_img = pygame.transform.scale(acid_eyes_img, acid_eyes_size)


game_state = "MENU"

# player
player_width = 80
player_height = 80
player = pygame.Rect(WIDTH // 2 - player_width // 2,
                     HEIGHT - player_height - 10, player_width, player_height)

# EYES_enemy
acid_width = 25
acid_height = 25
acid_eyes = []

# score
score = 0

# clock for FPS
clock = pygame.time.Clock()

pygame.mixer.music.load("songs/nine_lives_at_mach_two.mp3")
pygame.mixer.music.play(-1)

# bucle for the game
running = True
while running:

    # main bucle for the game#
    if game_state == "MENU":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # player pressing menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = event.pos

                    if play_button_rect.collidepoint(mouse_position):
                        game_state = "PLAYING"

                    if exit_button_rect.collidepoint(mouse_position):
                        running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    running = False

        # design menu
        screen.blit(background_menu, (0, 0))
        screen.blit(logo_game, logo_rect)
        screen.blit(img_button_play, play_button_rect)
        screen.blit(img_button_exit, exit_button_rect)

    # state game playing
    elif game_state == "PLAYING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += 5

        # eye enemy
        if len(acid_eyes) < 9 and random.randint(1, 20) == 1:
            acid_eye = pygame.Rect(random.randint(0, WIDTH - acid_width),
                                   0, acid_width, acid_height)
            acid_eyes.append(acid_eye)

        # eye enemy_movements
        for acid_eye in acid_eyes[:]:
            acid_eye.y += 5
            if acid_eye.top > HEIGHT:
                acid_eyes.remove(acid_eye)
                score += 1

        # colition
        for acid_eye in acid_eyes:
            if player.colliderect(acid_eye):
                game_state = "GAME_OVER"
                break

        #active_game
        screen.fill(BLACK)
        screen.blit(background_menu_2, (0, 0))
        screen.blit(player_img, player)
        for acid_eye in acid_eyes:
            screen.blit(acid_eyes_img, acid_eye)


        #score!
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == "GAME_OVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_position = event.pos
                if play_button_rect.collidepoint(mouse_position):
                    acid_eyes.clear()
                    player.x = WIDTH // 2 - player_width // 2
                    player.y = HEIGHT - player_height - 10
                    score = 0
                    game_state = "PLAYING"
                if exit_button_rect.collidepoint(mouse_position):
                    running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                acid_eyes.clear()
                player.x = WIDTH // 2 - player_width // 2
                player.y = HEIGHT - player_height - 10
                score = 0
                game_state = "PLAYING"
            if event.key == pygame.K_ESCAPE:
                running = False

        play_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 40)
        exit_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 130)

        screen.blit(background_menu, (0, 0))
        screen.blit(img_golden_border, marco_rect)
        screen.blit(img_gameover, gameover_rect)

        screen.blit(img_retry, retry_rect)

        screen.blit(img_button_play, play_button_rect)
        screen.blit(img_button_exit, exit_button_rect)

        # score text
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()