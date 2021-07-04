import pygame
import random
pygame.font.init()



WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
FONT = pygame.font.SysFont("comicsans", 40)
GROUND = pygame.Rect(0, 490, WIDTH, 10)
BACKGROUND = pygame.transform.scale(pygame.image.load("games/flappy_bird/assets/background.png"), (WIDTH, HEIGHT))
COLLIDED = pygame.USEREVENT + 1
SCORE = pygame.USEREVENT + 2

class Bird(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.graivty = 0

    def wingbeat(self):
        self.graivty = -3

class TopPillar(pygame.Rect):
    def __init__(self, height, starting_x):
        super().__init__(starting_x, 0, 30, height)

class BottomPillar(pygame.Rect):
    def __init__(self, height, starting_x):
        super().__init__(starting_x, HEIGHT - height, 30, height)

top_pillar1 = TopPillar(random.randint(150, 200), 400)
bottom_pillar1 = BottomPillar(random.randint(150, 200), 400)
top_pillar2 = TopPillar(random.randint(150, 200), 900)
bottom_pillar2 = BottomPillar(random.randint(150, 200), 900)
pillars = [[top_pillar1, bottom_pillar1], [top_pillar2, bottom_pillar2]]

bird = Bird(100, 100, 30, 30)


def draw_window(score=None, lost=False):
    WIN.blit(BACKGROUND, (0, 0))
    if lost:
        game_over_text = FONT.render("You lost", 1, BLACK)
        WIN.blit(game_over_text, (10, 10))

    else:
        bird.y += bird.graivty
        score_text = FONT.render(f"Score: {score}", 1, BLACK)
        WIN.blit(score_text, (10, 10))

    for pillar in pillars:
        # check if player has collided
        if pillar[0].colliderect(bird) or pillar[1].colliderect(bird):
            pygame.event.post(pygame.event.Event(COLLIDED))
        if bird.x > pillar[0].x:
            if bird.x - pillar[0].x <= 3:
                pygame.event.post(pygame.event.Event(SCORE))

        pillar[0].x -= 3
        pygame.draw.rect(WIN, BLACK, pillar[0])
        pillar[1].x -= 3
        pygame.draw.rect(WIN, BLACK, pillar[1])
        if pillar[0].x < 0:
            top_height = random.randint(50, HEIGHT - 100)
            bottom_height = HEIGHT - 100 - top_height
            pillar[0].__init__(top_height, 900)
            pillar[1].__init__(bottom_height, 900)

    if GROUND.colliderect(bird):
        pygame.event.post(pygame.event.Event(COLLIDED))

    pygame.draw.rect(WIN, GREEN, GROUND)
    pygame.draw.rect(WIN, RED, bird)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    lost = False
    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # check if the player has pressed space bar
            if event.type == pygame.KEYDOWN:
                if lost:
                    bird.graivty = 0
                    bird.y = 200
                    score = 0
                    lost = False

                if event.key == pygame.K_SPACE:
                    bird.wingbeat()
            
            if event.type == COLLIDED:
                lost = True
            
            elif event.type == SCORE:
                score += 1

        if lost:
            draw_window(lost=True)
        else:
            draw_window(score=score)
            bird.graivty += 0.25

if __name__ == "__main__":
    main()
