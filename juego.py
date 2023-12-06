from contextlib import redirect_stdout
from telnetlib import LINEMODE
import pygame
import sys
import time
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galaxion")

# Configuración del personaje
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 5
orientation = 1

#Configuración del arma
balas = 300
hayAMMO = True

# Configuración del arma
bullet_speed = 28
bullets = []

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

#Inicialización de valores
puntos = 0
nivel = 1
dificultad = 7
alive = True
newRecord = False
record = 0
try:
    arch = open("max_score.txt","r")
    if (arch):
        for line in arch:
            record = int(line)
    arch.close()
except FileNotFoundError:
    print(f"El archivo no existe.")
except Exception as e:
    print(f"Ocurrió un error: {e}")


#Fuentes
font = pygame.font.Font(None, 31)
font2 = pygame.font.Font(None, 28)
fontPuntos = pygame.font.Font(None, 36)
fontGameOver = pygame.font.Font(None, 43)
fontTitle = pygame.font.Font(None, 55)

# Clase para representar los proyectiles
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 20)

    def moveUp(self):
        self.rect.y -= bullet_speed

    def moveDown(self):
        self.rect.y += bullet_speed
    
    def moveRight(self):
        self.rect.x += bullet_speed
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 20, 10)

    def moveLeft(self):
        self.rect.x -= bullet_speed
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 20, 10)

    def draw(self):
        pygame.draw.rect(screen, red, self.rect)

class BulletWhite:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 20)

    def move(self):
        self.rect.y -= bullet_speed

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self):
        pygame.draw.rect(screen, red, self.rect)

enemies = []
def generarEnemigos():
    cantEnemies = random.randint(1, 7)
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    for i in range (cantEnemies):
        xEnemie = random.randint(1, 1000)
        yEnemie = random.randint(1, 800)
        enemy = Enemy(xEnemie, yEnemie)
        if not player.colliderect(enemy.rect):
            enemies.append(enemy)

#Generación de enemigos inciales
generarEnemigos()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    text_surface = fontTitle.render(f'GALAXION', True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 - 10)
    screen.blit(text_surface, text_rect)

    text_surface = fontPuntos.render(f'Presiona espacio para jugar', True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 + 20)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        break



# Bucle principal del juego
while True:
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Mover al jugador
        if keys[pygame.K_a] and (player_x - player_speed) >= 0:
            orientation = 4
            player_x -= player_speed
        if keys[pygame.K_d] and (player_x + player_size + player_speed) <= width:
            orientation = 2
            player_x += player_speed
        if keys[pygame.K_w] and (player_y - player_speed) >= 0:
            orientation = 1
            player_y -= player_speed
        if keys[pygame.K_s] and (player_y + player_size + player_speed) <= height:
            orientation = 3
            player_y += player_speed

        if keys[pygame.K_LEFT] and (player_x - player_speed) >= 0:
            orientation = 4
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and (player_x + player_size + player_speed) <= width:
            orientation = 2
            player_x += player_speed
        if keys[pygame.K_UP] and (player_y - player_speed) >= 0:
            orientation = 1
            player_y -= player_speed
        if keys[pygame.K_DOWN] and (player_y + player_size + player_speed) <= height:
            orientation = 3
            player_y += player_speed

        # Crear un nuevo proyectil cuando se presiona la tecla espacio
        if keys[pygame.K_SPACE]:
            if balas > 0:
                new_bullet = Bullet(player_x + player_size // 2 - 2, player_y)
                for i in range (10):
                    new_bullet.draw()
                    if orientation == 1:
                        new_bullet.moveUp()
                    elif orientation == 2:
                        new_bullet.moveRight()
                    elif orientation == 3:
                        new_bullet.moveDown()
                    elif orientation == 4:
                        new_bullet.moveLeft()
                    pygame.display.flip()

                    for enemy in enemies:
                        if new_bullet.rect.colliderect(enemy.rect):
                            enemies.remove(enemy)
                            puntos += 50
                            if len(enemies) == 0:
                                generarEnemigos()
                                if  dificultad + 2 <= 25:
                                    dificultad += 2
                                nivel += 1
                
                #time.sleep(0.01)
                balas -= 1
            else:
                hayAMMO = False

        if keys[pygame.K_r]:
            hayAMMO = True
            balas = 300


        # Mostrar el número de balas restantes
            
        # Limpiar la pantalla
        screen.fill(black)

        #Mostrar textos
        text_surface = fontPuntos.render(f'Puntos: {puntos}', True, white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (width // 2, 10)
        screen.blit(text_surface, text_rect)


        level_text = font.render(f'Nivel {nivel}', True, white)
        screen.blit(level_text, (10, 35))


        level_text = font.render(f'Record: {record}', True, white)
        screen.blit(level_text, (10, 60))

        # Dibujar al jugador
        pygame.draw.rect(screen, white, [player_x, player_y, player_size, player_size])
        player = pygame.Rect(player_x, player_y, player_size, player_size)

        for enemy in enemies:
            if player.colliderect(enemy.rect):
                if puntos > record:
                    record = puntos
                    newRecord = True
                    arch = open("max_score.txt","w")
                    arch.write(str(record))
                    arch.close()
                alive = False
                

        if not hayAMMO:
            text_surface = font2.render("No AMMO", True, red)
            text_rect = text_surface.get_rect()
            text_rect.topright = (width - 10, 10)
            screen.blit(text_surface, text_rect)

        bullets_text = font.render(f'AMMO: {balas}', True, white)
        screen.blit(bullets_text, (10, 10))

        for enemy in enemies:
            direction = random.randint(1, 8)
            
            if direction == 1 and (enemy.rect.y - 1) >= 0:
                for i in range (dificultad):
                    enemy.rect.y -= 1
            elif direction == 2 and (enemy.rect.x + 1) <= width:
                for i in range (dificultad):
                    enemy.rect.x += 1
            elif direction == 3 and (enemy.rect.y + 1) <= height:
                for i in range (dificultad):
                    enemy.rect.y += 1
            elif direction == 4 and (enemy.rect.x - 1) >= 0:
                for i in range (dificultad):
                    enemy.rect.x -= 1
            elif direction == 5 and (enemy.rect.x + 1) <= width and (enemy.rect.y - 1) >= 0:
                for i in range (dificultad):
                    enemy.rect.x += 1
                    enemy.rect.y -= 1
            elif direction == 6 and (enemy.rect.x + 1) <= width and (enemy.rect.y + 1) <= height:
                for i in range (dificultad):
                    enemy.rect.x += 1
                    enemy.rect.y += 1
            elif direction == 7 and (enemy.rect.x - 1) >= 0 and (enemy.rect.y + 1) <= height:
                for i in range (dificultad):
                    enemy.rect.x -= 1
                    enemy.rect.y += 1
            elif direction == 8 and (enemy.rect.x - 1) >= 0 and (enemy.rect.y - 1) >= 0:
                for i in range (dificultad):
                    enemy.rect.x -= 1
                    enemy.rect.y -= 1
            
            enemy.draw()
                    
                

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del bucle
        pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if newRecord:
        text_surface = fontPuntos.render(f'Nuevo record!', True, red)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (width // 2, 35)
        screen.blit(text_surface, text_rect)

    text_surface = fontGameOver.render(f'GAME OVER', True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

        # Controlar la velocidad del bucle
    pygame.time.Clock().tick(60)


    keys = pygame.key.get_pressed()
    screen.blit(text_surface, text_rect)
    if keys[pygame.K_SPACE] and not alive:
        alive = True
        player_x = width // 2 - player_size // 2
        player_y = height // 2 - player_size // 2
        orientation = 1
        balas = 300
        hayAMMO = True
        newRecord = False
        enemies = []
        generarEnemigos()
        puntos = 0
        dificultad = 7
        nivel = 1
