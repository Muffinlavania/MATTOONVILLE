import pygame,time,sys,ctypes,math,os,threading
from threading import Thread
from pygame.locals import *

WINDOWS =  os.name == "nt"
if WINDOWS:
  from ctypes import POINTER, WINFUNCTYPE, windll
  from ctypes.wintypes import BOOL, HWND, RECT

def sin(deg):
  return math.sin(math.radians(deg))

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


music = True
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
#'' is if you clip out of bounds
objects = {'':[], "home": [], '2nd' : [], '2ndsec':[], '3rd':[],'4th':[],'3rd2':[],'award':[],'asecret':[],'death':[], 'menu':[]} #append all showable entities to me!!!!!!!
PLACE = 'home'
LOCERS = [0,1] #row col
maxtravel = [0,1]

MAPPINGs = [
 [''      ,'home',''    ,''       , 'death'],
 ['2ndsec','2nd' ,''    ,"asecret",      ""],
 [''      ,"3rd" ,"3rd2","award"  ,      ''],
 [''      ,"4th" ,''    ,''       ,      '']
]
#asecret - presidential office, sign saying "a very familiar place.... looks royal"? 



def che(x=0,y=0, use = False):
  return not MAPPINGs[x + (LOCERS[0] if not use else 0)][y + (LOCERS[1] if not use else 0)] == ''

def nextplace(dir):
  global LOCERS,PLACE,maxtravel
  p2 = PLACE
  if dir in ['up','down']:
    LOCERS[0] += -1 if dir=='up' and LOCERS[0] > 0 and che(-1) else 1 if dir=='down' and LOCERS[0]<len(MAPPINGs)-1 and che(1) else 0
  else:
    LOCERS[1] += -1 if dir=='left' and LOCERS[1] > 0 and che(0,-1) else 1 if dir=='right' and LOCERS[1]<len(MAPPINGs[LOCERS[0]])-1 and che(0,1) else 0
  PLACE = MAPPINGs[LOCERS[0]][LOCERS[1]]
  maxtravel = [max([LOCERS[0], maxtravel[0]]), max([LOCERS[1], maxtravel[1]])]
  upminimap()
  return p2 != PLACE

def obs():
  tI = sorted([i.pos.bottom for i in objects[PLACE]])
  Objects = [0]*len(tI)
  for i in objects[PLACE]:
    g = tI.index(i.pos.bottom)
    Objects.insert(g,i)
    Objects.pop(Objects.index(0,g))
  i=0
  hit3,hitM = False,False
  while i != len(Objects):
    I = Objects[i]
    if (hit3 and I.name == '1') or (hitM and I.name=='M'): break
    if I.name=='blek' or I.name in '13M':
      Objects.remove(I)
      Objects.append(I)
      if I.name=='blek': break
      hit3 = I.name=='3' or hit3
      hitM = I.name=='M' or hitM
      i-=1
    i+=1
  for i in Objects:
    show(i.image, i.pos)
    
def fill(color,default=screen): #can take RGB too?
  default.fill(color)

def up(thing=True):
  #"""Pass in either a pygame.Rect(x,y,width,height) or x,y,image"""
  if thing:
    show(backing if PLACE != "2ndsec" else MERICA,(0,0))
    obs()
  pygame.display.update()
  #pygame.display.update(thing if type(thing) == pygame.rect.Rect else pygame.Rect(thing[0],thing[1],thing[2].get_width(),thing[2].get_height()))

#------- img things -------

def scale(thing,coors):
  return pygame.transform.scale(thing,coors)

def img(name, size_cors = ""):
  x = pygame.image.load(file(name))
  return x if size_cors == '' else scale(x,size_cors)

MERICA = img("office.png", (1280,720))

def color(colo,wid=WIDTH,hei=HEIGHT):
  surf = pygame.Surface((wid,hei))
  surf.fill(colo)
  return surf


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
    if not music: return
    pygame.mixer.music.load(file(name))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops, 0, fadetime)
  
  @staticmethod
  def fadeout(time):
    pygame.mixer.music.fadeout(time)
    
  
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
    if not music: return
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

before = True #before = on main menu, cant move

class Player:
  def __init__(self, image, speed, starting_cords = (0,0), name = "def"):
    self.speed = speed
    self.touched = False
    entity.__init__(self,image,starting_cords) #yoinky sploinky entitoinky
  
  def move(self, up=False, down=False, left=False, right=False):
    if before: return
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
fliP = ''
you = Player(pimgs["down"], 8, (1280/2,300))
for i in objects:
  objects[i].append(you)


def PIMG(thing):
  global pCUR, fliP
  if pCUR == thing or thing == fliP: return
  if thing=='f':
    fliP = 'f'
    you.image = pimgs[pCUR+'f']
  else:
    fliP = ''
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
  elif type(thing) == str:
    if (i:=getme(thing)):
      objects[PLACE].remove(i)
  else:
    for i in thing:
      if i in objects[PLACE]: objects[PLACE].remove(i)

def getme(name:str):
  for i in objects[PLACE]:
    if i.name == name: return i
  return None

def change(name:str, img: pygame.Surface):
  """Change all objects with object.name == name to object.image = img"""
  global objects
  for i in objects[PLACE]:
    if i.name == name:
      i.image = img

def text(text:str, slep = 25, afterwait = 2000, delete = True, selet = '', voiceline = False): #max of 60
  if voiceline: Sound.play(file(voiceline, True))
  container = [entity(box((1000,300),(0,0,0)), (140,375), "1")]
  container[0].image.blit(box((980,280), (255,255,255)),(10,10))

  addme(container[0],PLACE)
  
  t2 = ""
  y = 340

  while len(text) > 0:
    t2 = ""
    if text[0]==' ': text = text[1:]
    curt = entity(BIGfont.render("", True, (0,0,0)), (160,(y:=y+50)), "3")
    container.append(curt)
    addme(curt, PLACE)
    while len(text) > 0 and (len(t2) < 55 or text[0]!=" ") and text[0] != '\n':
      t2 += text[0] if (selet == '' or not text[0].isdigit()) else "-> " if int(text[0])==selet else "   "
      text = text[1:]
      curt.image = BIGfont.render(t2, True, (0,0,0))
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

def text2(text, slep, afterwait, voiceline = False): #(620, 10)
  if voiceline: Sound.play(file(voiceline, True))
  
  container = []

  t2 = ""
  y = -5

  while len(text) > 0:
    t2 = ""
    if text[0]==' ': text = text[1:]
    curt = entity(font3.render("", True, (0,0,0)), (630,(y:=y+25)), "3")
    container.append(curt)
    addme(curt, PLACE)
    while len(text) > 0 and (len(t2) < 30 or text[0]!=" ") and text[0] != '\n':
      t2 += text[0]
      text = text[1:]
      curt.image = font3.render(t2, True, (0,0,0))
      if slep>0:
        time.sleep(slep/1000)
    if len(text) > 0 and text[0] == '\n':
      time.sleep(slep/1000*9)
      text = text[1:]
  
  time.sleep(afterwait/1000)
  for i in container: delme(i, PLACE)
  return 

def AWARD():#award cutscne
  global hasmilk
  text("its the award he was talking about!!!" if mission else "no way its a random shiny trophy")
  delme("award", PLACE)
  Sound.play("gotit.ogg")
  hasmilk = True
  text("going to need to bring this back..." if mission else "minus well take it i guess it couldnt hurt")

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
      Sound.play("sel.wav")
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


def fadeinto(nextscreen, fadetime = 2000, waittime = 1000, back = False, BOSS = False):
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
  if BOSS:
    fill((255,255,255),blek.image)
    Sound.play("sel.wav") #find sound, CHANGE TO boss.mp3
  objects[PLACE].append(blek)
  for i in range(255,-1,-5):
    blek.image.set_alpha(i)
    up()
    sleep(ti if not BOSS else ti/2)
  objects[PLACE].remove(blek)

mission, hasmilk,anoynum, anoy2 = False, False, 1, 1
annoy = ["can i have money","can i have a selfie","can i skip class pls","can i have kidneys pls"]

annoyresponses = [(("no are you just annoying or something",30,3000,False),("please scram",30,3000,False)),(("i know im cool but dont be bugging me", 30, 3000, False),("youre not so slowly getting on my nerves okay", 30, 3000, False)),(("dude at this rate you should i dont get paid enough to deal with you", 30, 3000, False), ("if you come back here one more time and ask for something stupid you won't like whats next.", 30, 4000, False), ("for your own sake, forget your annoying side.",30, 4000, False)),(("....", 30, 2000, False), ("your talking privilages have been revoked.", 30, 3000, False),("bring me back my award. just find it. do not come back unless you have it. if you do, I have warned you enough for you to deserve what is coming. now go.", 40, 4000, False))]
#each response is a list of text options in a list
#mat voice

def goodending():
  quit("GOOD ENDING!!!!!")
def badending():
  global objects
  sleep(1000)
  text("...")
  text("youre gone.")
  objects[PLACE] = []
  text("was this what you intended?", 50, 1000)
  quit("BAD ENDING")

def dia(type = 'start', step = 2):
  global objects
  mat,dia = getme("MAT"), getme("1")
  JI = range(1 if 's' in type else 255, 256 if 's' in type else -1, step if 's' in type else -1*step)
  for i in JI:
    mat.pos.left = 550 - 200 * sin(i/2.84)
    dia.image.set_alpha(i)
    time.sleep(.01)
  if 'e' in type: dia.image.set_alpha(0)
  



def THEFINALE(): #MATTOON BOSS FIGHT!!, IT WORKS, JUST DONT UPDATE SCREEN AND USE TIME.SLEEP!!!!!!!!
  global you,objects
  time.sleep(2)
  dia('start')
  text2("I aways knew what kind of person you were", 25, 1000)
  text2("a stealer of good, an embodiment of bad", 25, 1000)
  text2("an agreed upon outliner", 25, 1000)
  #weapons/health appear
  text2("someone with no place in this world", 25, 1000)
  dia('end')
  #attack 1, mattoon goes to a random spot above the box, changes image and drops a math symbol/coding symbol or something downwards?
  #maybe make the image a random 20x20 from like a 100x100 image of different things?

  #attack 2, out of bounds

  #attack 3, finale, mr mattoon like rushes at you, you need to get him his murray award or else you just die


  
firstime = False #testing

def DOOR(): #door cutscene, TALK WITH MATTOON?
  global objects,backing,cutsceneing,firstime,selector, mission,anoynum,PLACE,LOCERS,you,anoy2
  BOSS = True #testing
  Music.fadeout(500)
  cutsceneing = True
  DEATH = anoynum == 4 and not hasmilk
  g = objects[PLACE].copy()
  matt = entity(mimgs["stare"],(1280-500-400, 0))
  if DEATH:
    matt.image = selectfill(matt.image,-100,-100,-100)
  backing = color((145, 91, 55) if not DEATH else (25,0,0),WIDTH,HEIGHT)
  objects[PLACE] = []
  up()

  text("...",25,1000)
  
  if firstime:
    text("its an empty room?") #mat voice
    text("how exciting...") #mat voice
    text("suddenly you hear footsteps...") #mat voice
    sleep(500)
  
  if not DEATH:
    Music.play("musika.mp3", .3, -1, 10000 if not firstime else 5000)
    pass

  addme(matt)
  for i in range(1,256,2 if firstime else 6):
    matt.image.set_alpha(i)
    up()
    sleep(40 if firstime else 25)

  sleep(500 if firstime else 3000 if DEATH else 0)

  if firstime and hasmilk:
    text("wait dude") #mat voice
    text("is that my trophy?????") #mat voice
    text("im kidding i know it is") #mat voice
    text("may if you actually talked to me beforehand i would give you a choice") #mat voice
    text("but for now thats mine") #mat voice
    text("bye bye!") #mat voice
    goodending()

  if DEATH:
    text("...")
    text("does it make you happy?\nnot listening, not caring.", 30, 1000)#mat voice
    text("you know what youve done, I wont be bothered to repeat it.", 30, 1000)#mat voice
    text("good luck.") #mat voice
    LOCERS = [0,4]
    upminimap()
    you.pos.top = 600
    g = objects["death"]
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
      texters = text("whats good bro?\n[Z to select, Arrow Keys to move selection]\n1 nothin\n2 idk",0,150,False, selector)
    delme(texters)
    text("well thats cool but anyway") #mat voice
  selector = 1

  if not mission:
    for i in 'i':
      text("what do you want?", 30, 500) #mat voice
      texters = text("what do you want?\n1 nothing what do you want\n2 "+annoy[anoynum]+"\n3 leave",0,0,False, selector)
      while sel(3)!='enter':
        delme(texters)
        texters = text("what do you want?\n1 nothing what do you want\n2 "+annoy[anoynum]+"\n3 leave",0,150,False, selector)
      delme(texters)
      if selector == 3: continue
      if selector == 1:
        text("actually thanks for asking")#mat voice
        text("i won this award but the person who gave it to me just kinda wasnt there")#mat voice
        text("since you kind of look like him, can you get it for me? i think its somewhere south of here, youll probably be able to figure it out.")#mat voice
        text("that was rhetorical by the way thank you youre going to get it for me bye")#mat voice
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
      texters = text("hey did you get my award yet?\n1 yep\n2 nerp",0,150,False, selector)
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
        if anoy2 == 1:
          text("oh yeah that big yellow shiny thing you have is not my award alright you better say yes next time") #mat voice
        else:
          text("yeah youre done") #mat voice
          BOSS = True

        anoy2+=1
      else:
        text("ok")#mat voice


  Music.fadeout(2000)
  if BOSS:
    you.pos.top = 300
    g = [you,entity(img("MATLEAN.png",(200,200)), (550,0), "MAT"),entity(color((0,0,0), 420,180), (620, 10), "1"), entity(color((0,0,0), 1,1), (620, 10), "3")]

    #come here, blit the top onto entity[1]
    g[2].image.blit(color((255,255,255), 410,170),(5,5))
    g[2].image.set_alpha(0)

    #size, coords
    for i in [[(800,20), (220,200)], [(20,360), (220,220)], [(800,20), (220,580)],[(20,360),(1000,220)]]:
      g.append(entity(color((0,0,0),i[0][0],i[0][1]),i[1],"wall")) #TEST THIS
  fadeinto(g, 1000, 0, color(colour,WIDTH,HEIGHT),BOSS)
  Music.play("cyber.mp3" if not BOSS else "cyber.mp3", .75, -1, 2000) #find sound, CHANGE TO bosssong.mp3
  if BOSS:
    Thread(target = THEFINALE).start()
  up()

def SIGN2():
  Sound.play("eagle.mp3")
  text("seems like a pretty royal office.")
  text("an almost familiar sight...")
def SIGN3():
  text("have you gotten lost yet??",25,1000)

nerdi = False
def NERD():
  global nerdi
  if not nerdi:
    nerdi=True
    text("my friend said he was gonna show up soon...")
    text("statistically he never shows, but theres always the most improbable option that has to be considered, and therefore i must refrain from realizing ive never had any friends and i am in fact mentally insane", 25, 3000)
    text("let me sit here in peace please sir")
  else:
    text("one of these days", 25, 1000)

def TREE():
  text("an inconspicuous looking tree...")
  text("what a big word") 

def PHO():
  text("looks like a dropped photo...")
  text("looking sharp fr")

joe = False
def JOE():
  global joe
  if not joe:
    text("haters will say im hacking")
    text("oh yeah im not friends with that guy btw")
    text("never have been")
    joe = True
  else:
    text("(this dude is locked in)")
  
dcoun = 0
def NUB():
  global dcoun,you,pimgs
  dcoun+=1
  if dcoun == 1:
    text("hey you too huh?")
    text("theres really only one way out, you kinda did this to yourself")
    text("thats why im here")
  if dcoun == 2:
    text("its better to slowly fade away instead of like dying")
    text("feels better imo")
  if dcoun == 3:
    text("maybe next time listen to dan huh?")
    text("hes like kinda the ruler of this place")
  if dcoun == 4:
    text("well it was good knowing you for a bit i guess")
    text("one more time is all it takes")
  for i in pimgs:
    pimgs[i].set_alpha(pimgs[i].get_alpha() - 51)
  up()
  if you.image.get_alpha() < 10:
    badending()
def WHAT():
  text("why is there a place off the minimap???")
  text("seems like bad game design.")
maming = False
def MAM():
  global maming 
  if not maming:
    maming = True
    text("if you get bros trophy, dont lie to him and say you dont got it")
    text("that stuff pisses him off he might like become a boss  fight or something idk")
    text("brother will have you for lunch")
  else:
    text("just dont say no when he asks you if you have the trophy alright")
interactibles = {'sign':SIGN,'award':AWARD, 'door': DOOR, 'sign2': SIGN2, 'sign3':SIGN3, 'nerd':NERD, 'tree':TREE, 'matphoto':PHO, 'joe': JOE,'noob':NUB,'what':WHAT, 'mam':MAM} #find interactables
INT_ME = []
def interact(): #for interacting!!
  for i in INT_ME:
    if touching(you, i, 'pass') and i in objects[PLACE]:
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
  [img("door_closed.jpeg",(480,200)),(400,-2),(20, 20, 20), 'home', 'door'],
  [(480,183),(400,-3),(20, 20, 20), 'home', 'wall'],
  [(520,200),(0,-1),(224, 219, 215), 'home', 'wall'],
  [(520,200),(1280-520,-1),(224, 219, 215), 'home', 'wall'],
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
  
  [flip(img("tree.png",(350,350))),(700,300),(0, 0, 0), '2nd', 'tree'],
  
  [flip(img("sign.png",(100,100))),(392,408),(0, 0, 0), '2ndsec', 'sign2'],
  
  [],
  [img("sign.png",(100,100)),(1000,500),(0, 0, 0), '3rd', 'sign3'],
  [img("MATHANDSHAKE.jpg",(50,50)),(210,200),(0, 0, 0), '4th', 'matphoto'],
  [img("mam.png",(64,64)),(900,400),(0, 0, 0), '3rd2', 'mam'],
  [],
  [],
  [],
  [],
  
  [img("trophy.png",(200,200)), (1000,250), (66, 66, 66), 'award','award'],
  [img("nerd.png",(200,150)), (100,250), (66, 66, 66), 'asecret','nerd'],
  [img("joe.png",(150,100)), (1130,250), (66, 66, 66), 'asecret','joe'],
  [(100,100), (1150,30), (0, 0, 0), 'asecret','what'],
  [],
  [img("noob.png", (255,255)),(1280/2 - 125,0),(0,0,0), "death", 'noob'],
]
#MAPPINGs = [
# [''      ,'home',''    ,''       ], 'death'
# ['2ndsec','2nd' ,''    ,"asecret"],
# [''      ,"3rd" ,"3rd2","award"  ],
# [''      ,"4th" ,''    ,''       ]
#]
minimap = entity(color((0,0,0),100,100),(1150,30),'M')
def upminimap():
  global minimap 
  minimap.image = color((0,0,0),100,100)
  if LOCERS[1] == 4: return
  for row in range(len(MAPPINGs)):
    for col in range(len(MAPPINGs[0])):
      if ((row <= maxtravel[0] and 0 < col <= maxtravel[1]+1)\
      or (0 < row <= maxtravel[0]+1 and col <= maxtravel[1])) and che(row,col,True):
        minimap.image.blit(color((255,255,255) if row != LOCERS[0] or col != LOCERS[1] else (125,255,125),20,20), (10+20*col,10+20*row))
upminimap()

for i in toMAKE:
  if i!=[]:
    wall(i[0],i[1],i[2],i[3],i[4])

for i in objects:
  objects[i].append(you)
  objects[i].append(minimap)

clock = pygame.time.Clock()



#----------------------------------- MAIN GAMEEEEEEEEEE -----------------------------------
pygame.init()
BIGfont = pygame.font.Font(file('determination.ttf'), 40)
title("Mr Mattoonville")
font = pygame.font.Font(file('determination.ttf'), 80)
font2 = pygame.font.Font(file('determination.ttf'), 45)
font3 = pygame.font.Font(file('determination.ttf'), 30)
Mtexts = [[font.render("Welcome to Mattoonville!", True, (255,255,255)),[350,100]],[font2.render("Press 'z' to interact, Arrow keys/WASD to move, P to toggle sound!", True, (0,0,0)), [120,250]]\
          ,[font2.render("Talk to Dan Mattoon, and get him his prize!!",True,(0,0,0)),[300,350]],[font3.render("(or face consequences!!!)",True,(0,0,0)),[400,450]], [font.render("Space to continue!", True, (255,255,255)),[350,525]]]
#[text, start_pos],[...]...
#find main menu
backing = color((160,0,173))
snum = 0
startings = []
for ind,i in enumerate(Mtexts):
  Mtexts[ind][1][0] = 640 - i[0].get_width()/2
  startings.append(640 - i[0].get_width()/2)
  Mtexts[ind] = entity(i[0], i[1])
F = pygame.key.get_pressed()

copY = objects[PLACE].copy()
objects[PLACE] = []
for i in Mtexts:
  objects[PLACE].append(i)
while not F[pygame.K_SPACE]:
  snum+=1
  fill((160,200*sin(snum/4%180),173), backing)
  for ind,i in enumerate(Mtexts):
    i.pos.left = startings[ind] + (sin(snum)*20 if ind in [0, 4] else 0)
  check_events()
  up()
  F = pygame.key.get_pressed()
  clock.tick(fps)

fadeinto(copY,1000,0,color(colour))


Music.play("cyber.mp3", .75, -1, 1000)
before = False
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
  if k[pygame.K_p]:
    Music.fadeout(1000)
    music = False
  elif k[pygame.K_v]:
    print(you.pos)
    
  #if (k[pygame.K_o] or k[pygame.K_p]):
  #  HEIGHT+=3 if k[pygame.K_p] else -3
  #  WIDTH+=3 if k[pygame.K_p] else -3
  #  screensize(WIDTH,HEIGHT)
  
  
  check_events()
  
  up() #passing nothing = full screen update
  lag_time = clock.tick(fps) / 1000 #fps = time since last frame (1 = its fine, can be used in frame dependant animation?)

