import pygame 
from settings import * 
from wall import * 
from block import * 
from player import * 
from ghost import *

# Je charge límage de mon pacman 
PacmanIcon = pygame.image.load("images/pacman.png")  
pygame.display.set_icon(PacmanIcon) 

#Jájoute la musique de fond et je la fais jou 
pygame.mixer.init() 
pygame.mixer.music.load("pacman.mp3") 
pygame.mixer.music.play(-1, 0.0) 


# on recupere la taille de chaque tableau de directions de nos fantomes
pl = len(Pinky_directions) - 1 
bl = len(Blinky_directions) - 1 
il = len(Inky_directions) - 1 
cl = len(Clyde_directions) - 1 


# Initialisation 
pygame.init() 
screen = pygame.display.set_mode([606, 606]) 
pygame.display.set_caption("Pacman") 

background = pygame.Surface(screen.get_size()) 
background = background.convert() 
background.fill(black) 

clock = pygame.time.Clock() 
pygame.font.init() 
font = pygame.font.Font("freesansbold.ttf", 24) # Changer la police 

# On defini les positions par defaut de pacman et des fantomes 
w = 303-16 # Width 
p_h = (7 * 60) + 19 # Position de Pacman 
m_h = (4 * 60 ) + 19 # Position de Monster 
b_h = (3 * 60) + 19 # Position de Binky 
i_w = 303 - 16 - 32 # Position de Inky 
c_w = 303 + (32 - 16) # Position de Clyde 


def startGame():

    # Definition des surface et chargement du premier niveau 
    all_sprites_list = pygame.sprite.RenderPlain() 
    block_list = pygame.sprite.RenderPlain() 
    monsta_list = pygame.sprite.RenderPlain() 
    pacman_collide = pygame.sprite.RenderPlain() 
    wall_list = setupRoomOne(all_sprites_list) 
    gate = setupGate(all_sprites_list) 


    # etat de pacman et des fantomes
    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_turn = 0
    c_steps = 0


    # Creation des pnj et de leurs surfaces de collisions
    Pacman = Player( w, p_h, "images/pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky=Ghost( w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky=Ghost( w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky=Ghost( i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde=Ghost( c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)
    

    # Dessinons la grille
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue 
            else:
                block = Block(yellow, 4, 4)

                # Definir un emplacement aleatoire pour le bloc
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26
                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue 
                elif p_collide:
                    continue 
                else:
                    # on ajoute le bloc la liste des objets du jeu
                    block_list.add(block)
                    all_sprites_list.add(block)
    
    bll = len(block_list)
    score = 0
    i = 0

    done = False 
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30,0) 
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30,0) 
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0,-30) 
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0,30) 
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30,0) 
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30,0) 
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0,30) 
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0,-30) 


        # Mis a jour de la position de pacman
        Pacman.update(wall_list,gate)


        # automatisation et mis a jour des fantomes 
        returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl) 
        p_turn = returned[0] 
        p_steps = returned[1] 
        Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl) 
        Pinky.update(wall_list,False) 

        returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl) 
        b_turn = returned[0] 
        b_steps = returned[1] 
        Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl) 
        Blinky.update(wall_list,False) 

        returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il) 
        i_turn = returned[0] 
        i_steps = returned[1] 
        Inky.changespeed(Inky_directions,False,i_turn,i_steps,il) 
        Inky.update(wall_list,False) 

        returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl) 
        c_turn = returned[0] 
        c_steps = returned[1] 
        Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl) 
        Clyde.update(wall_list,False) 


        # On verifie si le bloc de pacman est entre en collision avec un autre
        blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
           
        # On verifie la liste des collisions
        if len(blocks_hit_list) > 0:
            score +=len(blocks_hit_list)

        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)


        text = font.render("Score: "+str(score)+"/"+str(bll), True, red) 
        screen.blit(text, [10, 10]) 
        # On verifie si le joueur a fait mange toutes les balles a pacman 
        if score == bll: # si oui il a gagne 
            doNext("Congratulations, you won!",145,all_sprites_list,block_list, 
                       monsta_list,pacman_collide,wall_list,gate) 
            

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False) 
        if monsta_hit_list: # si il entre en collision avec un fantome il perd 
            doNext("Game Over",235,all_sprites_list,block_list,
                   monsta_list,pacman_collide,wall_list,gate)
        
        
        
        pygame.display.flip()

        clock.tick(10) 


# Gere la reinitialisation du jeu et la fenetre
def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
    while True:
        # On gere les venements de la fenetre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                if event.key == pygame.K_RETURN:
                    del all_sprites_list 
                    del block_list 
                    del monsta_list 
                    del pacman_collide 
                    del wall_list 
                    del gate 
                    startGame() 
        
        w = pygame.Surface((400,200))  # on dessine une surface dínformations 
        w.set_alpha(10)    # on defini sa transparence 
        w.fill((128,128,128))     # on defini sa couleur (gris) 
        screen.blit(w, (100,200))    # on positionne la surface 

        # En cas de victoire ou déchec
        text1 = font.render(message, True, white) 
        screen.blit(text1, [left, 233])  

        text2 = font.render("To play again, press ENTER.", True, white) 
        screen.blit(text2, [135, 303]) 
        text3 = font.render("To quit, press ESCAPE.", True, white) 
        screen.blit(text3, [165, 333]) 

        pygame.display.flip() 
        clock.tick(10) 


startGame()
pygame.quit()
