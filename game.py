import pygame
import random
import sys

from pygame import *



LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600


class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("ressources/vaisseau.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)
                tous_sprites.add(missile)
                le_missile.add(missile)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN


class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("ressources/missile.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = center_missile
        )

    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()


class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super(Ennemi, self).__init__()
        self.surf = pygame.image.load("ressources/ennemi.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 50,
                random.randint(0, HAUTEUR_ECRAN),
            )
        )

        self.speed = random.randint(5, 20)

    def update(self):
       self.rect.move_ip(-self.speed, 0)
       if self.rect.right < 0:
           self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        self._compteur = 10
        self.surf = pygame.image.load("ressources/explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = center_vaisseau
        )

    def update(self):
        self._compteur = self._compteur - 1

        if self._compteur == 0:
            self.kill()



pygame.init()


pygame.display.set_caption("The Shoot'em up 1.1 !")

AJOUTE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(AJOUTE_ENEMY, 500)

ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])



clock = pygame.time.Clock()


tous_sprites = pygame.sprite.Group()
le_missile = pygame.sprite.Group()
les_ennemis = pygame.sprite.Group()
les_explosions = pygame.sprite.Group()


vaisseau = Vaisseau()
tous_sprites.add(vaisseau)



continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        
        elif event.type == AJOUTE_ENEMY:
            nouvel_ennemi = Ennemi()
            les_ennemis.add(nouvel_ennemi)
            tous_sprites.add(nouvel_ennemi)

    
    ecran.fill((0, 0, 0))

    if pygame.sprite.spritecollideany(vaisseau, les_ennemis):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        continuer = False

    for missile in le_missile:
        liste_ennemis_touches = pygame.sprite.spritecollide(
            missile, les_ennemis, True)
        if len(liste_ennemis_touches) > 0:
            missile.kill()
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)

    touche_appuyee = pygame.key.get_pressed()

    vaisseau.update(touche_appuyee)
    le_missile.update()
    les_ennemis.update()
    les_explosions.update()

    for mon_sprite in tous_sprites:
        ecran.blit(mon_sprite.surf, mon_sprite.rect)

    ecran.blit(vaisseau.surf, vaisseau.rect)

    pygame.display.flip()

    clock.tick(30)


pygame.quit()
sys.exit()