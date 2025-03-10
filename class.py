import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defensa Circular")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Configuración del juego
center_x, center_y = WIDTH // 2, HEIGHT // 2
FPS = 60
font = pygame.font.SysFont(None, 36)

# Botón para iniciar la siguiente ronda
button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT - 80, 120, 50)
show_round_button = True

# Botón para mejorar el disparo
upgrade_button_rect = pygame.Rect(20, HEIGHT - 80, 180, 50)
shot_upgrade_cost = 50  # Costo de la mejora
shots_per_fire = 1  # Balas disparadas por vez

# Dinero y recompensa
money = 0
MONEY_REWARD = 10

def get_health_color(health):
    if health > 60:
        return GREEN
    elif health > 30:
        return YELLOW
    else:
        return RED

class Enemy:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        self.x = center_x + math.cos(angle) * 400
        self.y = center_y + math.sin(angle) * 400
        self.speed = random.uniform(1, 2)
        self.angle = math.atan2(center_y - self.y, center_x - self.x)
        self.life = 100
        self.alive = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed += 0.001
        if math.hypot(self.x - center_x, self.y - center_y) < 10:
            self.alive = False
            return True

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)
        health_color = get_health_color(self.life)
        pygame.draw.rect(screen, BLACK, (self.x - 10, self.y - 15, 20, 5))
        pygame.draw.rect(screen, health_color, (self.x - 10, self.y - 15, 20 * (self.life / 100), 5))

    def take_damage(self, damage):
        global money
        self.life -= damage
        if self.life <= 0:
            self.alive = False
            money += MONEY_REWARD

class Bullet:
    def __init__(self, angle):
        self.x, self.y = center_x, center_y
        self.speed = 5
        self.angle = angle
        self.alive = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT):
            self.alive = False

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 5)

def start_round():
    global enemies, show_round_button, fire_rate
    enemies = [Enemy() for _ in range(round_num)]
    show_round_button = False
    fire_rate = 30

def fire_bullets():
    if len(enemies) > 0:
        closest_enemy = min(enemies, key=lambda e: math.hypot(e.x - center_x, e.y - center_y))
        angle_to_enemy = math.atan2(closest_enemy.y - center_y, closest_enemy.x - center_x)
        
        delay_distance = 10  # Distancia entre cada bala en la misma trayectoria

        for i in range(shots_per_fire):
            bullet = Bullet(angle_to_enemy)
            bullet.x -= math.cos(angle_to_enemy) * delay_distance * i
            bullet.y -= math.sin(angle_to_enemy) * delay_distance * i
            bullets.append(bullet)



# Variables de juego
enemies = []
bullets = []
round_num = 1
central_ball_life = 100
fire_rate = 30  # Disparo cada 30 frames
running = True

while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (center_x, center_y), 15)
    
    central_ball_color = get_health_color(central_ball_life)
    pygame.draw.rect(screen, BLACK, (center_x - 50, center_y - 30, 100, 10))
    pygame.draw.rect(screen, central_ball_color, (center_x - 50, center_y - 30, 100 * (central_ball_life / 100), 10))

    if not enemies and not show_round_button:
        show_round_button = True
        round_num += 1

    for enemy in enemies[:]:
        if enemy.move():
            central_ball_life -= 10
        enemy.draw()
        if not enemy.alive:
            enemies.remove(enemy)

    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        for enemy in enemies[:]:
            if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < 10:
                enemy.take_damage(50)
                bullets.remove(bullet)
                break
        if not bullet.alive:
            bullets.remove(bullet)

    if len(enemies) > 0 and fire_rate <= 0:
        fire_bullets()
        fire_rate = 30
    fire_rate -= 1

    if show_round_button:
        pygame.draw.rect(screen, BLACK, button_rect)
        button_text = font.render("Siguiente Ronda", True, WHITE)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 15))
    
    pygame.draw.rect(screen, BLACK, upgrade_button_rect)
    upgrade_text = font.render("Mejorar Disparo (50$)", True, WHITE)
    screen.blit(upgrade_text, (upgrade_button_rect.x + 10, upgrade_button_rect.y + 15))

    money_text = font.render(f"Dinero: {money}", True, BLACK)
    screen.blit(money_text, (WIDTH - money_text.get_width() - 20, 50))

    shots_text = font.render(f"Balas por disparo: {shots_per_fire}", True, BLACK)
    screen.blit(shots_text, (20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_round_button and button_rect.collidepoint(event.pos):
                start_round()
            if upgrade_button_rect.collidepoint(event.pos) and money >= shot_upgrade_cost:
                money -= shot_upgrade_cost
                shots_per_fire += 1
    
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
