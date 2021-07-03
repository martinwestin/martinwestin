import pygame
from pygame import key
pygame.font.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
SPACESHIP_DIMENSIONS = (55, 40)
VEL = 5
MAX_BULLETS = 5
BULLET_VEL = 10

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)

YELLOW_SPACESHIP_IMAGE = pygame.image.load("games/space_game/assets/spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS)
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP_IMAGE = pygame.image.load("games/space_game/assets/spaceship_red.png")
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, SPACESHIP_DIMENSIONS)
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE = pygame.transform.scale(pygame.image.load("games/space_game/assets/space.png"), (WIDTH, HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, win=None):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # blit is used when putting "surfaces" onto the screen, and images are surfaces
    if win is None:
        red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
        yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)

        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))
    
    else:
        win_text = HEALTH_FONT.render(f"{win} wins, press any key to start over", 1, WHITE)
        WIN.blit(win_text, (50, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0: # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # down
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0: # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # down
        red.y += VEL


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
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# main game loop
def main():
    red = pygame.Rect(700, 300, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])
    yellow = pygame.Rect(100, 300, SPACESHIP_DIMENSIONS[0], SPACESHIP_DIMENSIONS[1])
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    win = None
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if win is not None:
                    win = None
                    red_health = 10
                    yellow_health = 10
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        if red_health <= 0:
            win = "yellow"
        if yellow_health <= 0:
            win = "red"

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # input
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        if win is None:
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        else:
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, win=win)
    
    pygame.quit()

if __name__ == "__main__":
    main()
