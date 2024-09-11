import pygame
import random

# تهيئة Pygame
pygame.init()

# إعدادات الشاشة والألوان
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game")

ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# إعدادات الدبابة
TANK_WIDTH, TANK_HEIGHT = 60, 40
tank_x, tank_y = WIDTH // 2, HEIGHT - TANK_HEIGHT - 10
tank_speed = 5

# إعدادات الصواريخ
rockets = []
rocket_speed = 7

# إعدادات الأعداء (المنصات والصحون الفضائية)
enemy_platforms = [{'x': random.randint(0, WIDTH - 60), 'y': random.randint(0, HEIGHT // 2)} for _ in range(5)]
ufos = [{'x': random.randint(0, WIDTH - 60), 'y': random.randint(0, HEIGHT // 2)} for _ in range(3)]
enemy_platform_speed = 2
ufo_speed = 3

# دوال الرسم
def draw_tank(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, TANK_WIDTH, TANK_HEIGHT))  # جسم الدبابة
    pygame.draw.rect(screen, BLACK, (x + 10, y + TANK_HEIGHT - 20, 40, 20))  # المدفع

def draw_rocket(x, y):
    pygame.draw.rect(screen, RED, (x, y, 5, 20))  # جسم الصاروخ
    pygame.draw.polygon(screen, RED, [(x, y), (x - 5, y + 10), (x + 5, y + 10)])  # طرف الصاروخ

def draw_enemy_platform(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, 60, 20))  # جسم المنصة
    pygame.draw.polygon(screen, BLACK, [(x, y), (x + 30, y - 30), (x + 60, y)])  # شكل المنصة

def draw_ufo(x, y):
    pygame.draw.ellipse(screen, BLUE, (x, y, 60, 30))  # جسم الصحن الفضائي
    pygame.draw.ellipse(screen, WHITE, (x + 20, y + 10, 20, 10))  # ضوء الصحن

def draw_victory_message():
    font = pygame.font.SysFont(None, 75)
    text = font.render("Victory!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# دالة للتحقق من التصادم
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(rect2)

# حلقة اللعبة الرئيسية
running = True
victory = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rockets.append({'x': tank_x + TANK_WIDTH // 2 - 2, 'y': tank_y})

    # تحريك الدبابة
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank_x -= tank_speed
    if keys[pygame.K_RIGHT]:
        tank_x += tank_speed
    if keys[pygame.K_UP]:
        tank_y -= tank_speed
    if keys[pygame.K_DOWN]:
        tank_y += tank_speed

    # تحريك الأعداء
    for platform in enemy_platforms:
        platform['y'] += enemy_platform_speed
        if platform['y'] > HEIGHT:
            platform['y'] = random.randint(-100, -20)
            platform['x'] = random.randint(0, WIDTH - 60)

    for ufo in ufos:
        ufo['x'] += random.choice([-ufo_speed, ufo_speed])
        if ufo['x'] < 0 or ufo['x'] > WIDTH - 60:
            ufo['x'] = WIDTH // 2

    # تحديث مواقع الصواريخ والتحقق من التصادم
    for rocket in rockets[:]:
        rocket['y'] -= rocket_speed
        if rocket['y'] < 0:
            rockets.remove(rocket)
            continue

        rocket_rect = pygame.Rect(rocket['x'], rocket['y'], 5, 20)

        for platform in enemy_platforms[:]:
            platform_rect = pygame.Rect(platform['x'], platform['y'], 60, 20)
            if check_collision(rocket_rect, platform_rect):
                enemy_platforms.remove(platform)
                rockets.remove(rocket)
                break

        for ufo in ufos[:]:
            ufo_rect = pygame.Rect(ufo['x'], ufo['y'], 60, 30)
            if check_collision(rocket_rect, ufo_rect):
                ufos.remove(ufo)
                rockets.remove(rocket)
                break

    # تحقق من النصر
    if not enemy_platforms and not ufos:
        victory = True

    # تحديث الشاشة وعرض العناصر
    screen.fill(ORANGE)
    draw_tank(tank_x, tank_y)
    for rocket in rockets:
        draw_rocket(rocket['x'], rocket['y'])
    for platform in enemy_platforms:
        draw_enemy_platform(platform['x'], platform['y'])
    for ufo in ufos:
        draw_ufo(ufo['x'], ufo['y'])

    if victory:
        draw_victory_message()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
