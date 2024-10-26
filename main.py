import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=100):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def update(self, keys=None):
        if keys:
            if keys[pygame.K_UP]:
                self.move_up()
            if keys[pygame.K_DOWN]:
                self.move_down()

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 5
        self.speed_y = 5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней границ
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1

player = Paddle(WIDTH - 20, HEIGHT // 2)
computer = Paddle(20, HEIGHT // 2)
ball = Ball(WIDTH // 2, HEIGHT // 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(computer)
all_sprites.add(ball)

player_score = 0
computer_score = 0
font = pygame.font.SysFont(None, 36)

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    player.update(keys)

    # Управление компьютером (простая ИИ)
    if computer.rect.centery < ball.rect.centery:
        computer.move_down()
    elif computer.rect.centery > ball.rect.centery:
        computer.move_up()

    # Обновление мяча
    ball.update()

    # Проверка столкновений с ракетками
    if pygame.sprite.collide_rect(ball, player) or pygame.sprite.collide_rect(ball, computer):
        ball.speed_x *= -1

    # Проверка, если мяч вышел за пределы экрана
    if ball.rect.left <= 0:
        player_score += 1
        ball.reset()
    if ball.rect.right >= WIDTH:
        computer_score += 1
        ball.reset()

    # Отрисовка
    WINDOW.fill(BLACK)
    all_sprites.draw(WINDOW)

    # Отображение счёта
    score_text = font.render(f"{computer_score} : {player_score}", True, WHITE)
    WINDOW.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
