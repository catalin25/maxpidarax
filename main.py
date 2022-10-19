import pygame
pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

bgcolor = (255,200,124)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('GAMEEE')

class Enemy():
    def __init__(self):
        pass


class Plat():
    def __init__(self, x, y):
        plat_img = pygame.image.load("assets/platform.jpg") 
        plat_inv = pygame.image.load("assets/platforminv.jpg")
        self.plat = plat_img
        self.platinv = plat_inv
        self.rect = self.plat.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = (self.rect.x, self.rect.y , 650, 130)


    def draw(self):
        screen.blit(self.plat,(self.rect.x, self.rect.y))
        self.hitbox = (self.rect.x, self.rect.y , 650, 130)
        # pygame.draw.rect(screen,(255,0,0), self.hitbox, 2)


    # def inv(self):
    #    screen.blit(self.platinv, (self.rect.x, self.rect.y))

class Soldier():
    def __init__(self, x, y, scale):
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'assets/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = (self.rect.x + 85, self.rect.y + 35, 70, 100)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.flip = False
        self.vel_y = 0
        self.jump = False
        self.hitu = False

    def move(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jump == False:
            self.vel_y = -15
            self.jump = True
        if key[pygame.K_SPACE] == False:
            self.jump = False
        if key[pygame.K_LEFT] and self.rect.x + 85 > 5:
            dx -= 5
            self.flip = True
        if key[pygame.K_RIGHT] and self.rect.x + 155 < 800:
            dx += 5
            self.flip = False

       

        #gravitate
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y


        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # if self.rect.bottom > 500:
        #     self.rect.bottom = 500
        #     dy = 0

    def hit(self):
        if self.hitu != True:
            print("Gata")


    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image on current frame
        self.image = self.animation_list[self.frame_index]
        # cat timp o trecut de la ultimul update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # restabilim ca nu mai avem imagini
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False ), self.rect)
        self.hitbox = (self.rect.x + 85, self.rect.y + 35, 70, 100)
        # pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

    def coliziune(self):
       if (self.hitbox[1] < platform.hitbox[1] + platform.hitbox[3]) and (self.hitbox[1] + self.hitbox[3] > platform.hitbox[1]):
        if (self.hitbox[0] + self.hitbox[2] > platform.hitbox[0]) and (self.hitbox[0] < platform.hitbox[0] + platform.hitbox[2]):
            self.rect.bottom = platform.rect.top - 7 # nu e potrivit cum trebuie
            

player = Soldier(100, 470, 2.5)
player2 = Soldier(300, 470, 2.5)
platform = Plat(0, 600)
platform2 = Plat(650,-30)

run = True
while run:

    

           
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False


    screen.fill(bgcolor)
    
    # platform2.inv()
    player.update_animation()
    player.draw()
    player2.draw()
    player.coliziune()
    platform.draw()
    

    player.move()
    pygame.display.flip()
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
