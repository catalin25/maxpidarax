def main():
    from xml.etree.ElementInclude import FatalIncludeError
    import pygame
    import os
    from pygame import mixer
    pygame.init()
    mixer.init()
    

    FPS = 60
    fpsClock = pygame.time.Clock()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    SCROLL_THRESH = 80 #DISTANTA PANA LA CAT PLAYERUL VEDE
    red= (255,0,0)
    gray = (80,80,80)
    bgcolor = (2, 48, 32)
    screen_scroll = 0
    bg_scroll = 0
    # pygame.mixer.music.load('assets/death.mp3')
    fall = pygame.mixer.Sound('assets/death.mp3')


    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('GAMEEE')
    bgpic = pygame.image.load("assets/bgpic.jpg")

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Press Q to exit', True, red, gray)
    textRect = text.get_rect()
    textRect = (0,0)


    def drawbg():
        screen.fill(bgcolor)
        for x in range(6):
            screen.blit(bgpic,((x * bgpic.get_width()) - bg_scroll *  0.2, bgpic.get_height() - 500))



    class Plat():
        def __init__(self, x, y):
            plat_img = pygame.image.load("assets/platform.jpg") 
            self.plat = plat_img
            self.rect = self.plat.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.hitbox = (self.rect.x, self.rect.y , 650, 130)


        def draw(self):
            self.rect.x += screen_scroll
            screen.blit(self.plat,(self.rect.x, self.rect.y))
            self.hitbox = (self.rect.x, self.rect.y , 650, 130)


    class Soldier():
        def __init__(self, x, y, char_type, scale):
            self.char_type = char_type
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

            animation_types = ['Idle', 'Run', 'Jump']
            for animation in animation_types:
                temp_list = []
                num_of_frames = len(os.listdir(f'assets/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'assets/{self.char_type}/{animation}/{i}.png')
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.alive = True
            self.hitbox = (self.rect.x + 80, self.rect.y + 35, 70, 100)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.flip = False
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.moving = False
            

        def move(self):
            dx = 0
            dy = 0
            screen_scroll = 0

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.in_air == False:
                self.jump = True
                self.vel_y = -17
                self.in_air = True
                
            if key[pygame.K_LEFT] :#and self.rect.x + 85 > 5:
                dx -= 5
                self.flip = True
                self.moving = True
            if key[pygame.K_RIGHT]: # and self.rect.x + 155 < 800:
                dx += 5
                self.flip = False
                self.moving = True
            
            
            
            #gravitate
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # # game over
            # if self.rect.y > 750:
            #     screen.fill(red)

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy



            # update scroll 
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

            return screen_scroll


        def update_animation(self):
            # update animation
            ANIMATION_COOLDOWN = 100
            # update image on current frame
            self.image = self.animation_list[self.action][self.frame_index]
            # cat timp o trecut de la ultimul update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            # restabilim ca nu mai avem imagini
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            
        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action

                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()


        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False ), self.rect)
            self.hitbox = (self.rect.x + 80, self.rect.y + 35, 70, 100)
        
        

        def coliziune(self, platform, platform2,platform3):
            if (self.hitbox[1] < platform.hitbox[1] + platform.hitbox[3]) and (self.hitbox[1] + self.hitbox[3] > platform.hitbox[1]):
                if (self.hitbox[0] + self.hitbox[2] > platform.hitbox[0]) and (self.hitbox[0] < platform.hitbox[0] + platform.hitbox[2]):
                    self.rect.bottom = platform.rect.top - 7 # nu e potrivit cum trebuie
                    self.in_air = False
                    # if (self.hitbox[0] + self.hitbox[2] > platform.hitbox[1]) :
                    #     self.rect.x = platform.hitbox[1]
            if (self.hitbox[1] < platform2.hitbox[1] + platform2.hitbox[3]) and (self.hitbox[1] + self.hitbox[3] > platform2.hitbox[1]):
                if (self.hitbox[0] + self.hitbox[2] > platform2.hitbox[0]) and (self.hitbox[0] < platform2.hitbox[0] + platform2.hitbox[2]):
                    self.rect.bottom = platform2.rect.top - 7 # nu e potrivit cum trebuie
                    self.in_air = False
            if (self.hitbox[1] < platform3.hitbox[1] + platform3.hitbox[3]) and (self.hitbox[1] + self.hitbox[3] > platform3.hitbox[1]):
                if (self.hitbox[0] + self.hitbox[2] > platform3.hitbox[0]) and (self.hitbox[0] < platform3.hitbox[0] + platform3.hitbox[2]):
                        self.rect.bottom = platform3.rect.top - 7 # nu e potrivit cum trebuie
                        self.in_air = False   
                    
            
    player = Soldier(100, 470,'player', 2.5)
    platform = Plat(0, 600)
    platform2 = Plat(780,480)
    platform3 = Plat(1600, 600)

    run = True
    while run:
        

        screen_scroll = player.move()
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                elif event.key == pygame.K_r:
                    player.alive = True
                    main()

                

                

        drawbg()
        player.update_animation()
        player.draw()
        # player2.draw()
        player.coliziune(platform, platform2, platform3)
        platform.draw()
        platform2.draw()
        platform3.draw()
        screen.blit(text,textRect)

        if player.in_air:
            player.update_action(2)#2: jump
        elif player.moving:
            player.update_action(1)#1: run
            player.moving = False
        else:
            player.update_action(0)#0: idle
            
        
        if player.rect.y > 750:
            player.alive = False
            fall.play()

        if player.alive == False:
                    screen.fill((136, 8, 8))
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    textDead = font.render('You Died! Press R to restart', True, (255, 255, 255))
                    textRectDead = textDead.get_rect()
                    textRectDead = ((SCREEN_WIDTH//2) + 140, SCREEN_HEIGHT//2)
                    screen.blit(textDead,textRectDead)
    
        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()

main()