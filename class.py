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

# Función para obtener el color de la barra según la vida
def get_health_color(health):
    if health > 60:
        return GREEN
    elif health > 30:
        return YELLOW
    else:
        return RED

# Clases
class Enemy:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        self.x = center_x + math.cos(angle) * 400
        self.y = center_y + math.sin(angle) * 400
        self.speed = random.uniform(1, 2)  # Velocidad inicial de los enemigos
        self.angle = math.atan2(center_y - self.y, center_x - self.x)
        self.life = 100  # Vida inicial del enemigo
        self.alive = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Aumenta la velocidad a medida que pasa el tiempo
        self.speed += 0.001
        
        if math.hypot(self.x - center_x, self.y - center_y) < 10:
            self.alive = False  # El enemigo ha alcanzado el centro
            return True  # Indicar que el enemigo tocó el centro

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)
        
        # Dibujar la barra de vida del enemigo
        health_color = get_health_color(self.life)
        pygame.draw.rect(screen, BLACK, (self.x - 10, self.y - 15, 20, 5))  # Barra base
        pygame.draw.rect(screen, health_color, (self.x - 10, self.y - 15, 20 * (self.life / 100), 5))  # Vida actual

    def take_damage(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.alive = False

class Bullet:
    def __init__(self, target_x, target_y):
        self.x, self.y = center_x, center_y
        self.speed = 5
        self.angle = math.atan2(target_y - self.y, target_x - self.x)
        self.alive = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT):
            self.alive = False

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 5)

# Variables de juego
enemies = []
bullets = []
round_num = 1
spawn_timer = 0
fire_rate = 30  # Dispara cada 30 frames
clock = pygame.time.Clock()
central_ball_life = 100  # Vida de la bola central

running = True
while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), 15)  # Bola central
    
    # Dibujar la vida de la bola central
    central_ball_color = get_health_color(central_ball_life)
    pygame.draw.rect(screen, BLACK, (center_x - 50, center_y - 30, 100, 10))  # Barra base
    pygame.draw.rect(screen, central_ball_color, (center_x - 50, center_y - 30, 100 * (central_ball_life / 100), 10))  # Vida actual

    # Generar enemigos por ronda
    if spawn_timer <= 0:
        for _ in range(round_num):
            enemies.append(Enemy())
        spawn_timer = 180  # Nueva ronda en 3 segundos
        round_num += 1  # Aumenta la dificultad
    spawn_timer -= 1

    # Disparo automático
    if len(enemies) > 0 and fire_rate <= 0:
        closest_enemy = min(enemies, key=lambda e: math.hypot(e.x - center_x, e.y - center_y))
        bullets.append(Bullet(closest_enemy.x, closest_enemy.y))
        fire_rate = 30  # Reinicia la velocidad de disparo
    fire_rate -= 1

    # Actualizar enemigos
    for enemy in enemies[:]:
        if enemy.move():
            central_ball_life -= 10  # La bola central pierde un 10% de su vida al tocarla
        enemy.draw()
        if not enemy.alive:
            enemies.remove(enemy)

    # Actualizar balas
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        for enemy in enemies[:]:
            if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < 10:
                enemy.take_damage(50)  # Enemigos reciben 50 de daño al ser alcanzados por la bala
                bullets.remove(bullet)
                break
        if not bullet.alive:
            bullets.remove(bullet)

    # Verificar si la bola central ha muerto
    if central_ball_life <= 0:
        print("¡La bola central ha sido destruida!")
        running = False

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
