import pygame, sys, os
pygame.font.init()
background_colour = (51,102,0) # bcg color
(width, height) = (1200, 600) # Screen size
screen = pygame.display.set_mode((width, height)) #Setting Screen
pygame.display.set_caption('Żużel by mgld') #Window Name
screen.fill(background_colour)#Fills white to screen
clock = pygame.time.Clock()

class Track:
    def __init__(self):
        self.dim=[160,90,24,1]
        self.scale=5
        self.weight=self.scale*self.dim[0]
        self.height=self.scale*self.dim[1]
        self.t=self.scale*self.dim[2]
        self.offset=self.scale*self.dim[3]
        self.cent=(width/2,height/2)
        self.radm=(self.weight-self.height)/2
        self.r=self.scale*self.dim[1]/2

        self.cent_1=(self.cent[0]-self.radm,self.cent[1])
        self.cent_2=(self.cent_1[0]+2*self.radm,self.cent_1[1])

        self.tcol=(102,51,0)
        self.ocol=(204,204,255)
        self.gcol=(51,102,0)

        self.rect_1=(self.cent[0]-(self.weight-self.height)/2,self.cent[1]-self.height/2,self.weight-self.height,self.height)
        self.rect_2=(self.rect_1[0],self.rect_1[1]+self.offset,self.rect_1[2],self.rect_1[3]-2*self.offset)
        self.rect_3=(self.rect_2[0],self.rect_2[1]+self.t,self.rect_2[2],self.rect_2[3]-2*self.t)
        self.rect_4=(self.rect_3[0],self.rect_3[1]+self.offset,self.rect_3[2],self.rect_3[3]-2*self.offset)

        self.rect_start=pygame.Rect(self.cent[0]-self.scale*1, self.cent[1]-self.height/2, self.scale*1, self.t+2*self.offset)

    def draw(self):
        pygame.draw.circle(screen, self.ocol, self.cent_1, self.r)
        pygame.draw.circle(screen, self.tcol, self.cent_1, self.r-self.offset)
        pygame.draw.circle(screen, self.ocol, self.cent_1, self.r-self.offset-self.t)
        pygame.draw.circle(screen, self.gcol, self.cent_1, self.r-2*self.offset-self.t)

        pygame.draw.circle(screen, self.ocol, self.cent_2, self.r)
        pygame.draw.circle(screen, self.tcol, self.cent_2, self.r-self.offset)
        pygame.draw.circle(screen, self.ocol, self.cent_2, self.r-self.offset-self.t)
        pygame.draw.circle(screen, self.gcol, self.cent_2, self.r-2*self.offset-self.t)

        pygame.draw.rect(screen,self.ocol,self.rect_1)
        pygame.draw.rect(screen,self.tcol,self.rect_2)
        pygame.draw.rect(screen,self.ocol,self.rect_3)
        pygame.draw.rect(screen,self.gcol,self.rect_4)

        pygame.draw.rect(screen, (0,0,0), self.rect_start)

    def resize(self):
        self.t=self.dim[2]*self.scale
        self.r=self.scale*self.dim[1]/2
        self.offset=self.scale*self.dim[3]
        self.rect_1=(self.cent[0]-(self.weight-self.height)/2,self.cent[1]-self.height/2,self.weight-self.height,self.height)
        self.rect_2=(self.rect_1[0],self.rect_1[1]+self.offset,self.rect_1[2],self.rect_1[3]-2*self.offset)
        self.rect_3=(self.rect_2[0],self.rect_2[1]+self.t,self.rect_2[2],self.rect_2[3]-2*self.t)
        self.rect_4=(self.rect_3[0],self.rect_3[1]+self.offset,self.rect_3[2],self.rect_3[3]-2*self.offset)

        self.rect_start=pygame.Rect(self.cent[0]-self.scale*1, self.cent[1]-self.height/2, self.scale*1, self.t+2*self.offset)

class Runner:
    def __init__(self):
        self.number=1
        self.pos=pygame.Vector2(track.cent[0],track.cent[1]-track.height/2+track.offset+track.t/3*self.number)
        self.startpos=pygame.Vector2(track.cent[0],track.cent[1]-track.height/2+track.offset+track.t/3*self.number)
        self.col=(255,0,0)
        self.tailcol=(200,30,0)

        self.dir=pygame.Vector2(-1,0)
        self.speed=1
        self.velosity=0.1

        self.tail=[]

        self.lapstogo=3
        self.halflaps=0

        self.startlap=0
        self.lapstime=[]
        # self.endtime=0
        self.bestlap=1000
        self.bestrun=1000
        self.won=False

        # self.end=False

    def update(self):
        global run
        self.pos+=self.dir*self.speed
        self.tail.append(self.pos[:])
        if len(self.tail)>100:self.tail=self.tail[-100:]
        self.speed-=self.velosity/2
        self.speed=max(1,self.speed)
        
        if not isintrack(self.pos, track):
            self.restart()

        if self.halflaps==0 and self.pos.x>width/2:
            self.halflaps=0.5
        if self.halflaps==0.5 and self.pos.x<width/2:
            self.halflaps=0
            self.lapstogo-=1
            temp=(pygame.time.get_ticks()-self.startlap)/1000
            if temp<self.bestlap:self.bestlap=temp
            self.startlap=pygame.time.get_ticks()
        
        if self.lapstogo<=0:
            temp=(pygame.time.get_ticks()-start_time)/1000
            if temp<self.bestrun:self.bestrun=temp
            self.restart()
            self.lapstogo=3
            run=False
            self.won=True

    def draw(self):
        for i in range(len(self.tail)-1):
            pygame.draw.line(screen, self.tailcol, self.tail[i], self.tail[i+1],2)

        pygame.draw.circle(screen, self.col, self.pos, 5)
        if self.won and gamemode:
            text(screen, height/2,width/2-50, "Winner: {}".format(self.number),30, (0,0,0))
    
    def restart(self):
        self.pos=pygame.Vector2(track.cent[0],track.cent[1]-track.height/2+track.offset+track.t/3*self.number)
        self.dir=pygame.Vector2(-1,0)
        self.speed=1
        self.velosity=0.1
        self.tail=[]
        self.halflaps=0
        self.won=False

def isintrack(pos,track):
    x=pos.x
    y=pos.y

    x_c1=track.cent_1[0]
    y_c1=track.cent_1[1]
    r_c1=track.r

    x_c2=track.cent_2[0]
    y_c2=track.cent_2[1]
    r_c2=track.r

    xr=track.rect_1[0]
    yr=track.rect_1[1]
    w=track.rect_1[2]
    h=track.rect_1[3]
    
    track_we=track.t+2*track.offset
    
    a=isincir(x, y, x_c1, y_c1, r_c1) or isincir(x, y, x_c2, y_c2, r_c2) or isinrec(x, y, xr, yr, w, h)
    b=isincir(x, y, x_c1, y_c1, r_c1-track_we) or isincir(x, y, x_c2, y_c2, r_c2-track_we) or isinrec(x, y, xr, yr+track_we, w, h-2*track_we)

    return a and not b
    
def isincir(x,y,xc,yc,r):
    return (x-xc)**2 + (y-yc)**2 <= r**2

def isinrec(x,y,xr,yr,w,h):
    return xr<x<xr+w and yr<y<yr+h

def text(surface, y, x, text,h,col):
    font = pygame.font.SysFont(None, h)
    text = font.render(text, 1, col)
    surface.blit(text, (x, y))

def reset():
    global running,helppanel,gamemode,track,runner1,runner2,run
    running = True
    helppanel=False
    gamemode=True
    track=Track()
    runner1=Runner()
    runner2=Runner()
    runner2.number=2
    runner2.col=(0,255,0)
    runner2.tailcol=(30,200,0)
    runner2.restart()
    run=False

reset()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_EQUALS:
                track.dim[2]+=5
                if track.dim[2]>39:track.dim[2]=39
                track.resize()
            if event.key==pygame.K_MINUS:
                track.dim[2]-=5
                if track.dim[2]<4:track.dim[2]=4
                track.resize()            
            if event.key==pygame.K_h:
                helppanel=not helppanel
            if event.key==pygame.K_g:
                gamemode=not gamemode
            if event.key==pygame.K_r:
                reset()

    keys=pygame.key.get_pressed()
     

    if keys[pygame.K_SPACE]:
        run=True
        start_time=pygame.time.get_ticks()
        runner1.startlap=pygame.time.get_ticks()
    if keys[pygame.K_RETURN]:
            runner1.restart()
            runner1.lapstogo=3
            runner2.restart()
            runner2.lapstogo=3
            run=False
    if run==True:
        if keys[pygame.K_z]:
            runner1.speed+=runner1.velosity
        if keys[pygame.K_x]:
            runner1.dir.rotate_ip_rad(-0.03)
        runner1.update()

        if keys[pygame.K_KP2]:
            runner2.speed+=runner1.velosity       
        if keys[pygame.K_KP3]:
            runner2.dir.rotate_ip_rad(-0.03)
        runner2.update()

    if run:
        text(screen, 20,width/2-20, "{:.1f}".format((pygame.time.get_ticks()-start_time)/1000),40, (0,0,0))

    text(screen, 20,20, "laps to go: {}".format(runner1.lapstogo),40, (0,0,0))
    text(screen, 80,20, "best:",40, (0,0,0))
    text(screen, 140,30, "-lap: {:.1f}".format(runner1.bestlap if runner1.bestlap!=1000 else 0),30, (0,0,0))
    text(screen, 200,30, "-run: {:.1f}".format(runner1.bestrun if runner1.bestrun!=1000 else 0),30, (0,0,0))
    track.draw()
    runner1.draw()

    if gamemode:
        de=200
        text(screen, 20,width-de, "laps to go: {}".format(runner2.lapstogo),40, (0,0,0))
        text(screen, 80,width-de, "best:",40, (0,0,0))
        text(screen, 140,width-de-10, "-lap: {:.1f}".format(runner2.bestlap if runner2.bestlap!=1000 else 0),30, (0,0,0))
        text(screen, 200,width-de-10, "-run: {:.1f}".format(runner2.bestrun if runner2.bestrun!=1000 else 0),30, (0,0,0))
        runner2.draw()

    if helppanel:
        run=False
        txt=["Controls: Z/X ; 2/3","Track resize: +/-","Restart: Enter","Reset: R","Start: Space","Gamemode: G"]
        for i in txt:
            text(screen, height/2+txt.index(i)*30-80,width/2-30, i,30, (0,0,0))

    pygame.display.flip()        
    pygame.display.update()
    pygame.time.wait(5)
    screen.fill(background_colour)
