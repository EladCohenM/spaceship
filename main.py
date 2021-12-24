import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

# VARIABLES
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
# WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 3, 0, 6, HEIGHT)
HEALTH_FONT = pygame.font.SysFont("sans-serif", 40)
WINNER_FONT = pygame.font.SysFont("sans-serif", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

FPS = 120
VEL = 10
MAX_BULLETS = 8
BULLET_VEL = 20

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotozoom(YELLOW_SPACESHIP_IMAGE, 90, 0.1)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotozoom(RED_SPACESHIP_IMAGE, 270, 0.1)
SPACE = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "space.png")), 0, 0.5)


# FUNCTIONS
def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}", 1, WHITE)
    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}", 1, WHITE)
    WIN.blit(yellow_health_text, (15, 15))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 15, 15))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def yellow_movement_handler(pressed_keys, player):
    if pressed_keys[pygame.K_a] and player.x >= 0 + VEL:  # LEFT
        player.x -= VEL
    if pressed_keys[pygame.K_d] and player.x < BORDER.x - player.width - VEL:  # RIGHT
        player.x += VEL
    if pressed_keys[pygame.K_w] and player.y > 0:  # UP
        player.y -= VEL
    if pressed_keys[pygame.K_s] and player.y < HEIGHT - player.height - VEL:  # DOWN
        player.y += VEL


def red_movement_handler(pressed_keys, player):
    if pressed_keys[pygame.K_LEFT] and player.x > BORDER.x + BORDER.width + VEL:  # LEFT
        player.x -= VEL
    if pressed_keys[pygame.K_RIGHT] and player.x < WIDTH - player.width - VEL:  # RIGHT
        player.x += VEL
    if pressed_keys[pygame.K_UP] and player.y > 0:  # UP
        player.y -= VEL
    if pressed_keys[pygame.K_DOWN] and player.y < HEIGHT - player.height - VEL:  # DOWN
        player.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (
        WIDTH//2 - draw_text.get_width()//2,
        HEIGHT//2 - draw_text.get_height()//2
    ))
    pygame.display.update()
    pygame.time.delay(5000)



# MAIN
def main():
    red = pygame.Rect(800, 250, RED_SPACESHIP.get_width(), RED_SPACESHIP.get_height())
    yellow = pygame.Rect(100, 250, YELLOW_SPACESHIP.get_width(), YELLOW_SPACESHIP.get_height())

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 12, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 12, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()


        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break



        pressed_keys = pygame.key.get_pressed()
        yellow_movement_handler(pressed_keys, yellow)
        red_movement_handler(pressed_keys, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
