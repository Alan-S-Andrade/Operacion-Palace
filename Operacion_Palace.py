import sys
import pygame
from time import sleep
from pygame.sprite import Sprite

class Stats:
    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
    def reset_stats(self):
        self.lulos_left = self.ai_settings.lulos_limit

class Willys():
    def __init__(self,ai_settings,screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('willys.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.y = 600
        self.ai_settings = ai_settings
        self.rect.x = 0
        self.center = float(self.rect.centerx)
    def blitme(self):
        self.screen.blit(self.image, self.rect)
class Titulo():
    def __init__(self,ai_settings,screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('palace2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.y = 0
        self.ai_settings = ai_settings
        self.rect.x = 100
        self.center = float(self.rect.centerx)
    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Canela(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('lulo.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        self.x += (self.ai_settings.canela_speed_factor *self.ai_settings.fleet_direction)
        self.rect.x = self.x
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
class Lulo():
    def __init__(self,ai_settings,screen):
        self.screen = screen
        self.image = pygame.image.load('elkin.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.ai_settings = ai_settings
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.center += self.ai_settings.lulo_speed_factor
        if self.moving_left and (self.rect.left > 0):
            self.center -= self.ai_settings.lulo_speed_factor
        self.rect.centerx = self.center
    def center_lulo(self):
        self.center = self.screen_rect.centerx

class Bullet(Sprite):
    def __init__(self,ai_settings,screen,lulo):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = lulo.rect.centerx
        self.rect.top = lulo.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Settings():
    def __init__(self):
        self.bullet_speed_factor = 5.1
        self.bullets_allowed = 7
        self.bullet_width = 6
        self.bullet_height = 15
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.bullet_color = 0, 0, 255
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.canela_speed_factor = 9
        self.lulo_speed_factor = 7
        self.lulos_limit = 3

def check_key_down(event,game_settings,screen,lulo,bullets):
    if event.key == pygame.K_RIGHT:
        lulo.moving_right = True
    elif event.key == pygame.K_LEFT:
        lulo.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, lulo, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_key_up(event,lulo):
    if event.key == pygame.K_RIGHT:
        lulo.moving_right = False
    elif event.key == pygame.K_LEFT:
        lulo.moving_left = False

def update_bullets(ai_settings,screen,lulo,canelas,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_canela_bullets_collisions(ai_settings,screen,lulo,canelas,bullets)
def check_canela_bullets_collisions(ai_settings,screen,lulo,canelas,bullets):
    collisions = pygame.sprite.groupcollide(bullets, canelas, True, True)
    if (len(canelas) == 0):
        bullets.empty()
        create_fleet(ai_settings,screen,lulo,canelas)


def fire_bullet(game_settings, screen, lulo, bullets):
    if (len(bullets) < game_settings.bullets_allowed):
        new_bullet = Bullet(game_settings,screen,lulo)
        bullets.add(new_bullet)

def check_events(game_settings, screen, lulo, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event,game_settings,screen,lulo,bullets)       
        elif event.type == pygame.KEYUP:
            check_key_up(event,lulo)

def update_screen(game_settings,screen,lulo,canelas,bullets,willys,titulo):
    screen.fill(game_settings.bg_color)
    lulo.blitme()
    willys.blitme()
    titulo.blitme()
    canelas.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()

def get_number_canelas_x(ai_settings,canela_width):
    available_space_x = ai_settings.screen_width - 2 * canela_width
    number_canelas_x = int(available_space_x / (2 * canela_width))
    return number_canelas_x

def get_number_rows(ai_settings,lulo_height,canela_height):
    available_space_y = (ai_settings.screen_height - (3 * canela_height) - lulo_height)
    number_rows = int(available_space_y / (2 * canela_height))
    return number_rows 

def check_fleet_edges(ai_settings,canelas):
    for canela in canelas.sprites():
        if canela.check_edges():
            change_fleet_direction(ai_settings, canelas)
            break
def change_fleet_direction(ai_settings,canelas):
    for canela in canelas.sprites():
        canela.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def create_fleet(ai_settings,screen,lulo,canelas):
    canela = Canela(ai_settings,screen)
    number_canelas_x = get_number_canelas_x(ai_settings, canela.rect.width)
    number_rows = get_number_rows(ai_settings,lulo.rect.height,canela.rect.height)
    for row_number in range(number_rows):
        for canela_number in range(number_canelas_x):
            create_canela(ai_settings,screen,canelas,canela_number,row_number)

def create_canela(ai_settings,screen,canelas,canela_number,row_number):
    caanela = Canela(ai_settings, screen)
    canela_width = caanela.rect.width
    caanela.x = canela_width + 2 * canela_width * canela_number
    caanela.rect.x = caanela.x
    caanela.rect.y = caanela.rect.height + 2 * caanela.rect.height * row_number
    canelas.add(caanela)

def check_canelas_bottom(ai_settings,stats,screen,lulo,canelas,bullets):
    screen_rect = screen.get_rect()
    for canela in canelas.sprites():
        if canela.rect.bottom >= screen_rect.bottom:
            # Lo mismo si le disparaon a lulo
            lulo_hit(ai_settings, stats, screen, lulo, canelas, bullets)
            break

def update_canelas(ai_settings,stats,screen,lulo,canelas,bullets):
    check_fleet_edges(ai_settings, canelas)
    canelas.update()
    if pygame.sprite.spritecollideany(lulo,canelas):
        lulo_hit(ai_settings, stats, screen, lulo, canelas, bullets)
    check_canelas_bottom(ai_settings, stats, screen, lulo, canelas, bullets)

def lulo_hit(ai_settings,stats,screen,lulo,canelas,bullets):
    if stats.lulos_left > 0:   
        stats.lulos_left -= 1
        canelas.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, lulo, canelas)
        lulo.center_lulo()
        sleep(0.5)
    else:
        stats.game_active = False

def run_game():
    pygame.init()
    pygame.display.set_caption("Operación Lulo")
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    lulo = Lulo(game_settings,screen)
    bullets = pygame.sprite.Group()
    stats = Stats(game_settings)
    willys = Willys(game_settings,screen)
    titulo = Titulo(game_settings,screen)
    canelas = pygame.sprite.Group()
    create_fleet(game_settings, screen,lulo, canelas)
    while True:
        check_events(game_settings,screen,lulo,bullets)
        if stats.game_active:
            lulo.update()
            update_bullets(game_settings,screen,lulo,canelas,bullets)
            update_canelas(game_settings,stats,screen,lulo,canelas,bullets)
        update_screen(game_settings,screen,lulo,canelas,bullets,willys,titulo)
run_game()
