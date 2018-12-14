# -*- coding: utf-8 -*-

import pygame
from math import * 
from pylab import *
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
#BALL_SIZE = 25 

#Random olarak yaratilan toplarin alabilecegi en buyuk ve en kucuk kutle degeri(kg)
MAX_MASS=50
MIN_MASS=20

#Her topun kendine ozgu bir id'si olmasi icin. Ayrica sahnedeki toplam top sayisini tutar
ballIndex=0

class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.mass=0
        self.id=0
        self.radius=0
        self.size=0
        self.color=WHITE
        #mass diam color coefficient can be added here
 
 
def make_ball(_ballIndex):
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
#    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
#    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
    ball.x = 100
    ball.y = 100
    # Speed and direction of rectangle
    ball.change_x = random.randrange(-2, 5)
    ball.change_y = random.randrange(-2, 5)
 
    ball.mass=random.randrange(MIN_MASS,MAX_MASS)

    
#   Top agirligi ve buyuklugu arasindaki iliski:
    ball.size=ball.mass*2.5
    ball.radius=ball.size/2
    
#   hafif top mavi, agir top kirmizi olsun
    ballColor= 255*(1-(MAX_MASS-ball.mass)/(MAX_MASS-MIN_MASS))
    ball.color=(ballColor,0,255-ballColor)
    ball.id=_ballIndex
    return ball
 
#   Iki top arasindaki uzakligi doner.
def distance(ball1,ball2):
    return hypot((ball1.x-ball2.x),(ball1.y-ball2.y))

#   Carpismadan sonraki hizlari doner. Aksi belirtilmedikce e 0.9 olarak hesaplanir
def calculateCollision(ball1,ball2,theta,e=0.9):

    v1pre = matrix([[ball1.change_x],
                    [ball1.change_y]])
    v2pre = matrix([[ball2.change_x],
                    [ball2.change_y]])
    
    R1 = matrix([[cos(theta), sin(theta)],
                 [-sin(theta), cos(theta)]])
    
    R2 = matrix([[cos(theta), -sin(theta)],
                 [sin(theta), cos(theta)]])
    
    v1p, v1n = R1*v1pre
    v2p, v2n = R1*v2pre
    
    v1pt, v2pt = multiply((1.0/(ball1.mass+ball2.mass)), matrix([[(ball1.mass-e*ball2.mass), ball2.mass*(1+e)],[ball1.mass*(1+e), (ball2.mass-e*ball1.mass)]])*vstack((v1p, v2p)))
    
    v1post = R2*vstack((v1pt, v1n))
    v2post = R2*vstack((v2pt, v2n))        
    return v1post,v2post
 
def main():
    """
    This is our main program.
    """
    pygame.init()
    
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Primitive Physics Engine")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    ball_list = []
    ballIndex=0
    ball = make_ball(ballIndex)
    
    ball_list.append(ball)
    

 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ballIndex+=1
                    ball = make_ball(ballIndex)
                    ball_list.append(ball)
 
        # --- Logic
        for ball in ball_list:
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y
 
            # Bounce the ball if needed
            if ball.y > SCREEN_HEIGHT - ball.radius or ball.y < ball.radius:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - ball.radius or ball.x < ball.radius:
                ball.change_x *= -1

        for i in range(ballIndex):
            for j in range(i+1,ballIndex+1):
                distanceBetweenBalls=distance(ball_list[i],ball_list[j])
                if distanceBetweenBalls<(ball_list[i].radius+ball_list[j].radius):
#                    Carpisma oldu
                    angleOfLineOfAction= atan2((ball_list[i].y-ball_list[j].y),(ball_list[i].x-ball_list[j].x))
#                   Eger genis aciysa tumleyenini al
                    if degrees(angleOfLineOfAction)<0:
                        angleOfLineOfAction=radians(180+degrees(angleOfLineOfAction))
#                   Toplarin ic ice ne kadar girdigini hesaplar
                    error=ball_list[i].radius+ball_list[j].radius-distanceBetweenBalls
                    
                    if error>0:
#                       ic ice giren toplarin konumlarini duzeltir
#                        print("rad",ball_list[i].radius+ball_list[j].radius," error ", error," distance ",distanceBetweenBalls," angle of action ",degrees(angleOfLineOfAction))
                        debug="1st ball is at "
                        if ball_list[i].x>ball_list[j].x:
                            debug+="right "
                            ball_list[i].x+=(error/2)*cos(angleOfLineOfAction)
                            ball_list[j].x-=(error/2)*cos(angleOfLineOfAction)
                            
                        else:
                            debug+="left "
                            ball_list[i].x-=(error/2)*cos(angleOfLineOfAction)
                            ball_list[j].x+=(error/2)*cos(angleOfLineOfAction)
                            
                        if ball_list[i].y>ball_list[j].y:
                            debug+="down"
                            ball_list[i].y+=(error/2)*sin(angleOfLineOfAction)
                            ball_list[j].y-=(error/2)*sin(angleOfLineOfAction)
                            
                        else: 
                            debug+="up"
                            ball_list[i].y-=(error/2)*sin(angleOfLineOfAction)
                            ball_list[j].y+=(error/2)*sin(angleOfLineOfAction)
                        
#                    print(debug)
                    v1post,v2post=calculateCollision(ball_list[i],ball_list[j],angleOfLineOfAction)
                    
#                   Carpisma sonrasi kutlelere gore hesaplanan hizlari atama:
                    ball_list[i].change_x= v1post.item(0)
                    ball_list[i].change_y=v1post.item(1)
                    ball_list[j].change_x=v2post.item(0)
                    ball_list[j].change_y=v2post.item(1)

                
        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)
 
        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, [int(ball.x), int(ball.y)], int(ball.radius))
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(100)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()