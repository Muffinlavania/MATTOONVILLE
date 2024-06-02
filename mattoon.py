import pygame,time,sys,ctypes,math,os
from pygame.locals import *

WINDOWS =  os.name == "nt"
if WINDOWS:
  from ctypes import POINTER, WINFUNCTYPE, windll
  from ctypes.wintypes import BOOL, HWND, RECT


#HITBOXES WORK, SCREEN CHANGING WORKS!!!!
#MADE THE WALL AND DOOR, CAN INTERACT WITH SIGN
#TODO:
#TEXT BOX CUTSCENES, SIGN/DOOR CUTSCENE
#START ADDING OTHER SCREENS, MINIMAP????
  #START MAKING ENDINGS, WE NEED A BOSS


#WALLS:
  #just make them colors, maybe make a func to generate all the walls upon room change and use the limited screen.blit ????

#PUT MATTOON DOOR THING
  #add a sign that says "Mr Mattoon's room" and stuff, then mr mattoon pops out and says "thats me!"
    #PUT DOWN A LONG HALLWAY NOW
  #go into door to talk to mr mattoon
  #maybe the ending whetr you make him mad = screen starts filling with lava ?
#Add minimap?
#add small map with interactable things and finally award somewhere



#---------------------------- funcs ----------------------------

#------ main things ---------
def file(name, vc = False):
  return ("MATTOONVILLE/" if not vc else "MATVCS/")+name

def sleep(tim=1000):
  if tim==0: return
  tim = round(tim,-1)
  li = list(i for i in range(5,500,5) if tim/i < 50)[0] if tim>=50 else 1 #.01% chance this errors
  tim1 = time.time()
  for _ in range(round(li)):
    pygame.key.get_pressed() #so it doesnt say unresponsive lol
    check_events()
    pygame.time.delay(round(tim/li))
  
def check_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit()

def quit(prompt = " "):
  pygame.quit()
  if prompt!=" ":
    input(prompt+"\n[Enter to close]")
  sys.exit()
  
#------- window things ------- 
def title(thi):
  pygame.display.set_caption(thi)

def windowpos():
  if not WINDOWS: return
  prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
  paramflags = (1, "hwnd"), (2, "lprect")

  GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
  POS = GetWindowRect(pygame.display.get_wm_info()["window"]) #ehre
  return [POS.left,POS.top]

def screensize(size,size2):
  global screen
  screen = pygame.display.set_mode((size,size2))

def move_window(x, y):
  if not WINDOWS: return
  hwnd = pygame.display.get_wm_info()["window"]
  
  user32 = ctypes.windll.user32
  user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)  # 0x0001 is SWP_NOSIZE flag

screensize(1280,720) #find screensize, find size
HEIGHT = 720
WIDTH = 1280

#------- screen things -------
def show(thing,where=(0,0),thingnightingi=None):
  screen.blit(thing,where,thingnightingi) #3rd arg used for cutoffs


#-------------------------- MAKING THE MAP STUFF find map --------------------------------------
objects = {"home": [], '2nd' : []} #append all showable entities to me!!!!!!!
PLACE = 'home'
LOCERS = [0,0]

MAPPINGs = [
 ['home'],
 ['2nd']
]




def nextplace(dir):
  global LOCERS,PLACE
  p2 = PLACE
  if dir in ['up','down']:
    LOCERS[0] += -1 if dir=='up' and LOCERS[0] > 0 else 1 if dir=='down' and LOCERS[0]!=len(MAPPINGs)-1 else 0
  else:
    LOCERS[1] += -1 if dir=='left' and LOCERS[1] != 0 else 1 if dir=='right' and LOCERS[1]!=len(MAPPINGs[LOCERS[1]])-1 else 0
  PLACE = MAPPINGs[LOCERS[0]][LOCERS[1]]
  return p2 != PLACE

def obs():
  tI = sorted([i.pos.top for i in objects[PLACE]])
  Objects = [0]*len(tI)
  for i in objects[PLACE]:
    g = tI.index(i.pos.top)
    Objects.insert(g,i)
    Objects.pop(Objects.index(0,g))
    
  for i in Objects: 
    if i.name=='blek': 
      Objects.remove(i) 
      Objects.append(i)
      break
      
  for i in Objects:
    show(i.image, i.pos)
    
def fill(color,default=screen): #can take RGB too?
  default.fill(color)


def up(thing=False):
  """Pass in either a pygame.Rect(x,y,width,height) or x,y,image"""
  if not thing:
    show(backing,(0,0))
    obs()
    pygame.display.update()
  else:
    pygame.display.update(thing if type(thing) == pygame.rect.Rect else pygame.Rect(thing[0],thing[1],thing[2].get_width(),thing[2].get_height()))

#------- img things -------
def img(name, size_cors = ""):
  x = pygame.image.load(file(name))
  return x if size_cors == '' else scale(x,size_cors)

def color(colo,wid=WIDTH,hei=HEIGHT):
  surf = pygame.Surface((wid,hei))
  surf.fill(colo)
  return surf

def scale(thing,coors):
  return pygame.transform.scale(thing,coors)

def flip(thi,x_flip=True,y_flip=False):
  return pygame.transform.flip(thi,x_flip,y_flip)

def selectfill(img, r=0, g=0, b=0):
  #input numbers below 120 for best results (dont make them too extreme)
  for x in range(img.get_width()):
    for y in range(img.get_height()):
      a = img.get_at((x, y)) #r,g,b,a <- we get a
      img.set_at((x, y), pygame.Color(a[0] + r if 0<a[0] + r<255 else 255 if a[0]+r>=255 else 0, a[1] + g if 0<a[1] + g < 255 else 255 if a[1]+g>=255 else 0, a[2] + b if 0<a[2] + b < 255 else 255 if a[2]+b >= 255 else 0, a[3])) #set things
  return img

def grayscale(img):
  for x in range(img.get_width()):
    for y in range(img.get_height()):
      av2 = img.get_at((x,y))
      av = (av2[0]+av2[1]+av2[2])//3
      img.set_at((x,y),pygame.Color(av,av,av,av2[3]))
  return img

#used for animations, was used for FIRE and PETRONE
def anim(name,num,end='png'):
  return pygame.image.load(f"FILES/{name}/{name}-{num:05d}.{end}") #format num with 5 digits in total

def needed(AMO,start):
  q = AMO - round(round((time.time()-start)*1000),-1)
  return q if q>1 else 1

#--------------------- classes ----------------------------------
class Music:
  @staticmethod
  def play(name, volume = 1, loops = -1, fadetime =0):
    """Set loops to -1 for inf"""
    pygame.mixer.music.load(file(name))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops, 0, fadetime)
  
  @staticmethod
  def fadeout(time):
    pygame.mixer.fadeout(time)
    Music.stop()
    
  
  @staticmethod
  def stop():
    pygame.mixer.music.stop()
  
  @staticmethod
  def pause():
    pygame.mixer.music.pause()

  @staticmethod
  def unpause():
    pygame.mixer.music.unpause()

  @staticmethod
  def volume(vol):
    pygame.mixer.music.set_volume(vol)
  
class Sound:
  @staticmethod
  def play(name,volume = 1):
    s = pygame.mixer.Sound(file(name))
    if volume!=1: s.set_volume(volume)
    pygame.mixer.Sound.play(s)
  
class entity:
  def __init__(self, image, starting_cords = (0,0), name = 'def'):
    self.image = image
    self.height = self.image.get_height()
    self.pos = image.get_rect().move(starting_cords[0], starting_cords[1])
    self.width = self.image.get_width()
    self.name = name
  def changeimage(self,image):
    self.image = image
    self.height = self.image.get_height()
    self.width = self.image.get_width()
    self.pos = image.get_rect().move(self.pos.left,self.pos.top)

class Player:
  def __init__(self, image, speed, starting_cords = (0,0), name = "def"):
    self.speed = speed
    self.touched = False
    entity.__init__(self,image,starting_cords) #yoinky sploinky entitoinky
  
  def move(self, up=False, down=False, left=False, right=False):
    self.OLD = (self.pos.right,self.pos.top)

    if right: self.pos.right += self.speed
    elif left: self.pos.right -= self.speed
    if down: self.pos.top += self.speed
    elif up: self.pos.top -= self.speed
    
    #out of bounds
    t = False
    for i in objects[PLACE]:
      if i!=self and touching(self,i):
        t = True
        self.touched = True
        self.pos.right = self.OLD[0]
        self.pos.top = self.OLD[1]
    
    self.touched = t
    
    if self.pos.right > WIDTH:
        self.pos.right = WIDTH if not nextplace('right') else self.width
    if self.pos.right < self.width:
        self.pos.right = self.width if not nextplace('left') else WIDTH
    if self.pos.top > HEIGHT-self.height: #SWITCH THE SCREENS!!!!
        self.pos.top = HEIGHT-self.height if not nextplace('down') else 0
    if self.pos.top < 0:
        self.pos.top = 0 if not nextplace('up') else HEIGHT-self.height

def touching(MOVER:entity,WALL:entity,paddingtop=0,paddingsides=0): #both entites/players
  if WALL.name != 'wall' and paddingtop != 'pass': return

  if paddingtop == 'pass': paddingtop = 0

  T1 = WALL.pos
  T2 = MOVER.pos

  right = T2.right < T1.right-paddingsides and  T2.right > T1.left+paddingsides
  left = T2.left > T1.left+paddingsides and     T2.left < T1.right-paddingsides
  top = T2.top > T1.top+paddingtop and          T2.top < T1.bottom-paddingtop
  bottom = T2.bottom < T1.bottom-paddingtop and T2.bottom > T1.top + paddingtop

  for i in [right,left]:
    for j in [top,bottom]:
      if i and j: return (WALL.name)

  return False




#------------------------------------------------------------- start actual stuff -------------------------------------------------------------

colour=(160,132,173)
backing = color(colour,WIDTH,HEIGHT)
fps = 60
frame = 0

#PLAYER THINGS
BIGGER = img("players.png").convert_alpha()
pimgs = {"upf": pygame.Surface((256, 256)).convert_alpha(), "down": pygame.Surface((256, 256)).convert_alpha(),"up":pygame.Surface((256, 256)).convert_alpha(),"downf":pygame.Surface((256, 256)).convert_alpha()}

for i in pimgs: pimgs[i].fill((255,255,255)) #prep them, without this you just get black!!
  
for ind,i in enumerate(pimgs):
  if ind < 2:
    pimgs[i].blit(BIGGER, (0, 0), (0, ind*256, 256, 256), BLEND_RGBA_MULT)
    pimgs[i] = scale(pimgs[i], (64,64))
  else:
    pimgs[i].blit(BIGGER, (0, 0), (256, (ind-2)*256, 256, 256), BLEND_RGBA_MULT)
    pimgs[i] = scale(pimgs[i], (64,64))
    
pCUR = "down"
flip = ''
you = Player(pimgs["down"], 8, (1280/2,300))
for i in objects:
  objects[i].append(you)


def PIMG(thing):
  global pCUR, flip
  if pCUR == thing or thing == flip: return
  if thing=='f':
    flip = 'f'
    you.image = pimgs[pCUR+'f']
  else:
    flip = ''
    pCUR = thing if thing != '' else pCUR
    you.image = pimgs[pCUR]


#-- - - - -- - - - - - -- cutsceneing stuff --- -- - - - - - - - - - - - - - -

def addme(thing: entity, PLACE = PLACE):
  global objects
  objects[PLACE].append(thing)

def delme(thing, PLACE = PLACE):
  global objects
  if type(thing) == entity:
    if thing in objects[PLACE]:
      objects[PLACE].remove(thing)
  else:
    for i in thing:
      if i in objects[PLACE]: objects[PLACE].remove(i)

def change(name:str, img: pygame.Surface):
  """Change all objects with object.name == name to object.image = img"""
  global objects
  for i in objects[PLACE]:
    if i.name == name:
      i.image = img

def text(text:str, slep = 30, afterwait = 2000, delete = True, selet = '', voiceline = False): #max of 60
  if voiceline: Sound.play(file(voiceline, True))
  container = [entity(box((1000,300),(0,0,0)), (140,375), "txt"), entity(box((980,280), (255,255,255)), (150,385), "txt2")]

  for i in container: addme(i,PLACE)
  
  font = pygame.font.Font(file('determination.ttf'), 40)

  t2 = ""
  y = 340

  while len(text) > 0:
    t2 = ""
    curt = entity(font.render("", True, (0,0,0)), (160,(y:=y+50)), "txt3")
    container.append(curt)
    addme(curt, PLACE)
    while len(text) > 0 and (len(t2) < 55 or text[0]==" ") and text[0] != '\n':
      t2 += text[0] if (selet == '' or not text[0].isdigit()) else "-> " if int(text[0])==selet else "   "
      text = text[1:]
      curt.image = font.render(t2, True, (0,0,0))
      if slep>0:
        up()
        sleep(slep)
    if len(text) > 0 and text[0] == '\n':
      sleep(slep*9)
      text = text[1:]
  up()
  sleep(afterwait)
  
  if delete:
    for i in container: delme(i, PLACE)
    up()
  else:
    return container


def AWARD():#award cutscne
  pass

def SIGN(): #sign cutscene
  text("the sign reads:\nMATTOONS HOUSE", 25, 1000)
  met = entity(pygame.transform.rotate(img("MATSUP.png",(250,250)),-5),(500,10))
  addme(met)
  change("door",img("door_open.jpg", (480,202)))
  up()
  sleep(1000)
  text("THATS ME!", 30, 2000, True, '', False) #mat voice
  Sound.play("doorslam.mp3")
  delme(met)
  change("door",img("door_closed.jpeg", (480,202)))
  up()
  sleep(500)

selector = 1
def sel(max):
  '''Returns a number for next position based on max of selector, or "enter" if you select'''
  global selector
  
  while True:
    k = pygame.key.get_pressed()
    check_events()

    if k[pygame.K_z]:
      return "enter"
    if k[pygame.K_w] or k[pygame.K_UP]:
      selector = selector-1 if selector > 1 else max
      return 
    if k[pygame.K_s] or k[pygame.K_DOWN]:
      selector = selector+1 if selector<max else 1
      return 
    clock.tick(fps)


mimgs = {"lean":img("MATLEAN.png", (500,500)), "pfp":img("MATPFP.jpg", (500,500)), "stare":img("MATSTARE.png", (500,500)), "sup":img("MATSUP.png", (500,500))}
cutsceneing = False
firstime = True


def fadeinto(nextscreen, fadetime = 2000, waittime = 1000, back = False):
  global objects,backing
  '''Fades the entire screen into the next one'''
  blek = entity(box((1300,800), (0,0,0)),(-1,-10),"blek")
  objects[PLACE].append(blek)
  ti = round(fadetime/51)-5 
  for i in range(0,256,5):
    blek.image.set_alpha(i)
    up()
    sleep(ti)
  sleep(waittime)
  if back: backing = back
  objects[PLACE] = nextscreen
  objects[PLACE].append(blek)
  for i in range(255,-1,-5):
    blek.image.set_alpha(i)
    up()
    sleep(ti)
  objects[PLACE].remove(blek)

mission, hasmilk,anoynum = False, False, 1
annoy = ["can i have money","can i have a selfie","can i skip class pls","can i have kidneys pls"]

annoyresponses = [(("no are you just annoying or something",30,3000,False),("please scram",30,3000,False)),(("i know im cool but stop bugging me", 30, 3000, False),("youre not so slowly getting on my nerves okay", 30, 3000, False)),(("dude at this rate you should i dont get paid enough to deal with you", 30, 3000, False), ("if you come back here one more time and ask for something stupid you won't like whats next.", 30, 5000, False), ("for your own sake, forget your annoying side.",30, 4000, False)),(("....", 30, 2000, False), ("your talking privilages have been revoked.", 30, 3000, False),("bring me back my award. just find it. do not come back unless you have it. if you do, I have warned you enough for you to deserve what is coming. now go.", 40, 4000, False))]
#each response is a list of text options in a list
#mat voice
def goodending():
  pass

def DOOR(): #door cutscene, TALK WITH MATTOON?
  global objects,backing,cutsceneing,firstime,selector, mission,anoynum
  cutsceneing = True
  DEATH = anoynum == 4 and not hasmilk
  g = objects[PLACE].copy()
  matt = entity(mimgs["stare"],(1280-500-400, 0))
  if DEATH:
    matt.image = selectfill(matt.image,-100,-100,-100)
  backing = color((145, 91, 55) if not DEATH else (90,26,0),WIDTH,HEIGHT)
  objects[PLACE] = []
  up()

  if firstime:
    sleep(500)
    text("...")
    text("its an empty room?")
    text("how exciting...")
    text("suddenly you hear footsteps...")
    sleep(500)
  if not DEATH:
    #Music.play("musika.mp3", .3, -1, 10000)
    pass

  addme(matt)
  for i in range(1,256,2 if firstime else 6):
    matt.image.set_alpha(i)
    up()
    sleep(40 if firstime else 25)

  sleep(500 if firstime else 3000 if DEATH else 0)

  if DEATH:
    text("...")
    text("does it make you happy?\nnot listening, not caring.", 30, 1000)#mat voice
    text("you know what youve done, I wont be bothered to repeat it.", 30, 1000)#mat voice
    text("good luck.") #mat voice
    fadeinto(g, 1000, 500, color((0,0,0),WIDTH,HEIGHT))
    up()
    return
  elif anoynum == 4:
    text("woah you actually got it") #mat voice
    text("you were an inch away from death but now that i have my award its ok")#mat voice
    goodending()

  selector = 1
  texters = []
  
  if firstime:
    firstime = False

    text("whats good bro?",30,500) #mat voice
    texters = text("whats good bro?\n[Z to select, Arrow Keys to move selection]\n1 nothin\n2 idk",0,0,False, selector)
    while sel(2)!='enter':
      delme(texters)
      texters = text("whats good bro?\n[Z to select, Arrow Keys to move selection]\n1 nothin\n2 idk",0,100,False, selector)
    delme(texters)
    text("well thats cool but anyway") #mat voice
  selector = 1

  if not mission:
    for i in 'i':
      text("what do you want?", 30, 500) #mat voice
      texters = text("what do you want?\n1 nothing what do you want\n2 "+annoy[anoynum]+"\n3 leave",0,0,False, selector)
      while sel(3)!='enter':
        delme(texters)
        texters = text("what do you want?\n1 nothing what do you want\n2 "+annoy[anoynum]+"\n3 leave",0,100,False, selector)
      delme(texters)
      if selector == 3: continue
      if selector == 1:
        text("actually thanks for asking")#mat voice
        text("i won this award but the person who gave it to me just kinda wasnt there")#mat voice
        text("since you kind of look like him, can you get it for me? i think its somewhere south of here, youll probably be able to figure it out.")#mat voice
        text("that was rhetorical by the way thank you youre going to get it for me bye")
        mission = True
      if selector == 2:
        if anoynum == 3:
          Music.fadeout(1000)
          sleep(1000)
        
        for i in annoyresponses[anoynum]:
          if 'for your own sake' in i[0]: Music.pause()
          text(i[0],i[1],i[2],True,"",i[3])
          Music.unpause()
        anoynum += 1
  else:
    text("hey did you get my award yet?", 30, 500) #mat voice
    texters = text("hey did you get my award yet?\n1 yep\n2 nerp",0,0,False, selector)
    while sel(2)!='enter':
      delme(texters)
      texters = text("hey did you get my award yet?\n1 yep\n2 nerp",0,100,False, selector)
    delme(texters)
    if selector == 1:
      if hasmilk:
        text("no way bro it looks so shiny thank you") #mat voice
        text("i wont forget this but ill never tell anyone about this for some reason") #mat voice
        goodending()
      else:
        text("im not even annoyed just disappointed") #mat voice
    else:
      if hasmilk:
        text("oh yeah that big yellow shiny thing you have is not my award alright tell me when you get it") #mat voice
      else:
        text("ok")#mat voice

    




  
  Music.fadeout(2000)
  fadeinto(g, 1000, 0, color(colour,WIDTH,HEIGHT))
  up()


interactibles = {'sign':SIGN,'award':AWARD, 'door': DOOR}
INT_ME = []
def interact(): #for interacting!!
  for i in INT_ME:
    if touching(you, i, 'pass'):
      interactibles[i.name]()

def box(size, color):
  e = pygame.Surface(size)
  e.fill(color)
  return e

def wall(size, coord = (0,0), colo = (0,0,0), PLACE = PLACE, name = 'wall'):
  global INT_ME
  NEW = entity(box(size, colo) if type(size) != pygame.Surface else size,coord,name)
  addme(NEW, PLACE)
  if any(i==name for i in interactibles):
    INT_ME.append(NEW)
  return NEW


#MAKING WALLS, find walls

toMAKE = [ #size (can be img), coords, color (unused if size is img), place, name (wall = hitbox, NA = no hitbox [decor])
  [img("door_closed.jpeg",(480,202)),(400,-2),(20, 20, 20), 'home', 'door'],
  [(480,183),(400,-3),(20, 20, 20), 'home', 'wall'],
  [(520,201),(0,-1),(224, 219, 215), 'home', 'wall'],
  [(520,201),(1280-520,-1),(224, 219, 215), 'home', 'wall'],
  [(60,200),(120,0),(214, 209, 205), 'home', 'NA'],
  [(60,200),(1280-180,0),(214, 209, 205), 'home', 'NA'],
  [(60,200),(180,0),(200, 196, 191), 'home', 'NA'],
  [(60,200),(1280-240,0),(200, 196, 191), 'home', 'NA'],
  [(60,200),(240,0),(185, 181, 176), 'home', 'NA'],
  [(60,200),(1280-300,0),(185, 181, 176), 'home', 'NA'],
  [(60,200),(300,0),(200, 196, 191), 'home', 'NA'],
  [(60,200),(1280-360,0),(200, 196, 191), 'home', 'NA'],
  [(60,200),(360,0),(214, 209, 205), 'home', 'NA'],
  [(60,200),(1280-420,0),(214, 209, 205), 'home', 'NA'],
  [img("sign.png",(100,100)),(1280-520,220),(214, 209, 205), 'home', 'sign'],
  [(320, 180), (500,500), (96, 199, 28), '2nd',' wall'],
  [],
  [],
  [],
  [],
]

for i in toMAKE:
  if i!=[]:
    wall(i[0],i[1],i[2],i[3],i[4])


clock = pygame.time.Clock()




#----------------------------------- MAIN GAMEEEEEEEEEE -----------------------------------
title("Mr Mattoonville")
pygame.init()
while True:

  k = pygame.key.get_pressed()

  if k[pygame.K_UP] or k[pygame.K_w]:
    you.move(up=True)
    PIMG("up")
  elif k[pygame.K_RIGHT] or k[pygame.K_d]:
    you.move(right=True)
    PIMG("")
  elif k[pygame.K_DOWN] or k[pygame.K_s]:
    you.move(down=True)
    PIMG("down")
  elif k[pygame.K_LEFT] or k[pygame.K_a]:
    you.move(left=True)
    PIMG("f")
  
  if k[pygame.K_z]:
    interact()
  elif k[pygame.K_v]:
    text("hello hows it going you doing wel muffin man wading wow huh i did do i need a break yes i do need a breka and now herfen this wshould work ")
    
  #if (k[pygame.K_o] or k[pygame.K_p]):
  #  HEIGHT+=3 if k[pygame.K_p] else -3
  #  WIDTH+=3 if k[pygame.K_p] else -3
  #  screensize(WIDTH,HEIGHT)
  
  
  check_events()
  
  up() #passing nothing = full screen update
  lag_time = clock.tick(fps) / 1000 #fps = time since last frame (1 = its fine, can be used in frame dependant animation?)
