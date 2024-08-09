import pygame
import math
import time
import random

pygame.init()
pygame.mixer.init()

hit_sound= pygame.mixer.Sound("hit_sound.wav")
miss_sound= pygame.mixer.Sound("miss_sound.wav")

width,height= 800,600

window= pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Trainer") 

target_increament= 400
target_event= pygame.USEREVENT
 
target_padding= 30

Bg_colour= (46, 58, 89)

lives = 5
top_bar_height= 50

label_font= pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE= 30
    GROWTH_RATE= 0.2
    COLOUR= "red"
    SECOND_COLOUR= "white"

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.size= 0
        self.grow= True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow= False

        if self.grow:
            self.size+=self.GROWTH_RATE 
        else:
            self.size-=self.GROWTH_RATE

    def draw(self,win):
        pygame.draw.circle(win, self.COLOUR,(self.x,self.y),self.size)
        pygame.draw.circle(win, self.SECOND_COLOUR,(self.x,self.y),self.size * 0.8)
        pygame.draw.circle(win, self.COLOUR,(self.x,self.y),self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOUR,(self.x,self.y),self.size * 0.4)

    def collide(self,x,y):
        dis= math.sqrt((self.x - x)**2 + (self.y - y)**2)

        if dis <= self.size:
            return dis



def draw(win, targets):
    win.fill(Bg_colour)
    
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli= math.floor(int(secs * 1000 % 1000)/100)
    seconds= int(round(secs % 60, 1))
    minutes= int(secs / 60)

    return f"{minutes:02d}:{seconds:02d}:{milli}"

def end_display(win, elapsed_time, targets_pressed, clicks, score):
    win.fill(Bg_colour)

    time_label= label_font.render(f"Time : {format_time(elapsed_time)}",1, "white")

    speed= round(targets_pressed / elapsed_time, 1)
    speed_label= label_font.render(f"Speed: {speed} t/s",1,"white")

    hits_label= label_font.render(f"hits: {targets_pressed}",1,"white")

    accuracy= round(targets_pressed/clicks * 100,1)
    accuracy_label= label_font.render(f"Accuracy: {accuracy} %",1,"white")

    score_label = label_font.render(f"Score: {score}", 1, "white")

    win.blit(time_label, (get_middle(time_label),100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300)) 
    win.blit(accuracy_label, (get_middle(accuracy_label),400))
    win.blit(score_label, (get_middle(score_label), 500)) 

    pygame.display.update()

    state=True

    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return width/2 - surface.get_width()/2


def draw_top_bar(win, elapsed_time, targets_pressed, lives):
    pygame.draw.rect(win, "orange",(0,0,width,top_bar_height))

    time_label= label_font.render(f"Time : {format_time(elapsed_time)}",1, "black")

    speed= round(targets_pressed / elapsed_time, 1)
    speed_label= label_font.render(f"Speed: {speed} t/s",1,"black")

    lives_label= label_font.render(f"lives: {lives}",1,"black")

    hits_label= label_font.render(f"hits: {targets_pressed}",1,"black")


    win.blit(time_label, (5,5))
    win.blit(speed_label, (220,5))
    win.blit(hits_label, (480,5)) 
    win.blit(lives_label, (650,5)) 

def wait_for_quit():
    state = True
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_q, pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                state = False

def pause_menu(win):
    win.fill(Bg_colour)
    pause_label = label_font.render("Game Paused. Press R to resume or Q to quit.", 1, "white")
    win.blit(pause_label, (get_middle(pause_label), height / 2))
    pygame.display.update()
    wait_for_quit()

def draw_score(win, score):
    score_label = label_font.render(f"Score: {score}", 1, "white")
    win.blit(score_label, (10, height - 40))  

def hit_animation(win, x, y):
    
    colors = ["yellow", "orange", "red"]

    for i in range(30, 0, -1):  
        for color in colors:
            pygame.draw.circle(win, color, (x, y), i, 1)
        pygame.display.update()   


def main():
    global lives
    run=True
    targets=[]
    clock= pygame.time.Clock()

    target_pressed = 0
    clicks=0
    misses=0
    score=0
    start_time= time.time()

    pygame.time.set_timer(target_event, target_increament)

    while run:
        clock.tick(60)
        click= False
        mouse_pos= pygame.mouse.get_pos()
        elapsed_time= time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break
 
            if event.type == target_event:
                x= random.randint(target_padding, width-target_padding)
                y= random.randint(target_padding + top_bar_height, height-target_padding)
                target= Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click= True
                clicks += 1
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu(window)
                if event.key == pygame.K_q:
                    run = False

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
                miss_sound.play()

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1
                hit_sound.play()
                score+=10
                hit_animation(window, target.x, target.y)

        tar= target_pressed

        if misses >= lives:
            lives-=1
            misses=0

        if lives <= 0:
            end_display(window, elapsed_time, target_pressed, clicks, score)
            run = False
           
        draw(window, targets)
        draw_top_bar(window,elapsed_time,tar, lives)
        draw_score(window, score)
        pygame.display.update()

    
    pygame.quit()

if __name__ == "__main__":
    main()
        

 