


import pygame.gfxdraw


def main():

    
    import time
    import pygame
    import math
    import sys
    import random
    from icecream import ic

    # # Main settings # #
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    pygame.display.set_caption("Circle Shooter")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    # # Musik and SoundFX (inf loop) # #
    pygame.mixer.init()
    pygame.mixer.music.load('sfx/DragAndDreadTheme.wav')
    pygame.mixer_music.set_volume(0.0)
    pygame.mixer.music.play(-1)

    # Draw Background
    BG_image = pygame.image.load('textures/bg_space.png')

    # IC Debugger
    ic.enable
    

    ###########################
    ### Define classes here ###
    ###########################

    # TODO Fetch Controller input
    class Controlls:
        pass

    class Player(pygame.sprite.Sprite):
        def __init__(self, groups):
            super().__init__(groups)
            self.image = pygame.image.load('textures/body_01.png').convert_alpha()
            self.rect = self.image.get_frect()
            # Spawn position on obj. construction
            self.rect.centerx = (SCREEN_WIDTH / 2)
            self.rect.centery = (SCREEN_HEIGHT / 2)
            self.move_x = 0
            self.move_y = 0
            self.move_speed = 1
            self.angle = 0.0
            # List of Weapons Attribute List
            self.turrets = []
            # Call input and trigger shoot
            self.shoot = False
 
        def controlls(self):  
            self.move_x, self.move_y = 0, 0
            keys = pygame.key.get_pressed() 
            self.move_x = int(keys[pygame.K_d] - int(keys[pygame.K_a]))
            self.move_y = int(keys[pygame.K_s] - int(keys[pygame.K_w]))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.shoot = True
                    print(player.shoot)
                if event.type == pygame.MOUSEBUTTONUP:
                    player.shoot = False
                    ic(player.shoot)

        def move(self):
            self.controlls()
            self.rect.centerx += self.move_x * self.move_speed
            self.rect.centery += self.move_y * self.move_speed

        # atan2 vector degree calculation
        def vectorCalculation(self):
            # Mouse pos x, y
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # ATAN2 Vector -> angle calculation
            vector_x = player.rect.centerx - mouse_x
            vector_y = player.rect.centery - mouse_y
            angle_rad = math.atan2(vector_x, vector_y)
            self.angle = math.degrees(angle_rad)
            # Draw line between ship and cursor
            # pygame.draw.line(screen, (255,0,0), (player.rect.centerx, player.rect.centery), (mouse_x, mouse_y), 2)
         
        def rotate_player(self):
            self.vectorCalculation()
            self.rotate_image = pygame.transform.rotate(player.image, self.angle)
            self.rotate_rect = self.rotate_image.get_rect(center=self.rect.center)

        def update(self):
            # update player surface
            self.move()
            self.rotate_player()
            screen.blit(self.rotate_image, self.rotate_rect.topleft)
            # update turret list AND shoot if requierments met
            ic(player)
            for turret in self.turrets:
                # player shoot true if lmb pressed
                if self.shoot:
                    turret.shoot(self.rect.x, self.rect.y, self.angle)
                # update turrents draw on (-,-)
                turret.update(self, screen, player, self.rotate_rect.x, self.rotate_rect.y, self.angle)
                


    class weapon:
        def __init__(self):
            self.weap_surf = pygame.image.load('textures/turret_01_mk1.png')
            self.weap_rect = self.weap_surf.get_frect()
            self.weap_sfx = pygame.mixer.Sound('sfx/shoot.wav')
            self.weap_rate_of_fire = 500
            self.pre = 0
            self.post = pygame.time.get_ticks()
            self.weap_dmg = 1
            self.weap_proj_list = []
            self.weap_shoot = False

        def calc_fire_rate(self):
            self.pre = pygame.time.get_ticks()
            if  self.pre - self.post > self.weap_rate_of_fire:
                self.weap_shoot = True
                self.post = pygame.time.get_ticks()       
            
        def shoot(self, x, y, angle):
            # validate time between shoots
            self.calc_fire_rate()
            # validate if LMB pressed, create proj and add to weap Proj list
            if self.weap_shoot:
                self.weap_shoot = False
                self.weap_sfx.play()
            
        # TODO fix turrent rotation on mouse x,y and shipcontrol key press only
        def update(self, screen, player, x, y, angle):
            rotation = pygame.transform.rotate(self.weap_surf, angle)
            screen.blit(rotation, (x,y))
            self.weap_rect = rotation.get_frect(center=(player.rect.centerx, player.rect.centery))
            ic(self.weap_rect)
            for projectile in self.weap_proj_list[:]:
                projectile.update(screen)
                if projectile.proj_duration <= 0:
                    pass


    class Projectile:
        def __init__(self, x, y, angle):
            self.proj_surf = pygame.image.load('textures/turret_01_bullet_01.png')
            self.proj_rect = self.proj_surf.get_frect(center=(x, y))
            self.proj_sfx = 0
            self.x = x
            self.y = y
            self.proj_speed = 2
            self.proj_duration = 240
            self.proj_size = 1
            self.angle = angle
            self.calc_xy_velocity()

        def calc_xy_velocity(self):
            angle_radians = math.radians(self.angle)
            self.proj_x_velo = -self.proj_speed * math.sin(angle_radians)
            self.proj_y_velo = -self.proj_speed * math.cos(angle_radians)
          
        def update(self, screen):
            self.proj_rect.centerx += self.proj_x_velo
            self.proj_rect.centery += self.proj_y_velo
            pygame.draw.line(screen, (0,255,0), (self.proj_rect.centerx, self.proj_rect.centery), (self.x, self.y), 2)
            self.proj_duration -= 1
            if self.proj_duration > 0:
                screen.blit(self.proj_surf, self.proj_rect.topleft)

    # TODO Automate encounter and events logic
    class Spawner:
        def __init__(self):
            pass

        def offscreen_spawn_calc():
            pass

        def atan2_traj_calc():
            pass

    # Encounter main class 
    # TODO: Subclasses Asteroid, Enemys with random size and speed range. Different target system.    
    class Encounter:
        def __init__(self, x, y, angle):
            self.type_path = self.type_path
            self.surf = pygame.image.load(self.type_path, (x,y))
            self.rect = self.surf.get_rect()
            self.angle = angle
            self.rotate_surf = pygame.transform.rotate(self.surf, self.angle)

    # TODO Item class to boost player attributes
    class Item:
        pass

    

        


            
    # Clocktick tracking  in milliseconds
    clock = pygame.time.Clock()
    running = True

    # create objects
    main_sprites = pygame.sprite.Group()
    player = Player(main_sprites)
    player.turrets.append(weapon)
  
    

    # Mainloop for game logic
    while running:
        
        # Exit and Mouse button event chk
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     player.shoot = True
            # if event.type == pygame.MOUSEBUTTONUP:
            #     player.shoot = False

        # Draw background
        screen.blit(BG_image)

        # Draw player and sub classes and call their objects incl. methods
        main_sprites.update()

        # Buttom settings and clean up screen
        pygame.display.flip()
        screen.fill("black")
        clock.tick(60)

    # Quit if loop finishes
    pygame.quit()

# convention to run main file
if __name__ == '__main__':
    main()