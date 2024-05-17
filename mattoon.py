import pygame,time,sys,ctypes,math,os
from pygame.locals import *

WINDOWS =  os.name == "nt"
if WINDOWS:
  from ctypes import POINTER, WINFUNCTYPE, windll
  from ctypes.wintypes import BOOL, HWND, RECT


#TODO:
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
def file(name):
  return "MATTOONVILLE/"+name

def sleep(tim=1000):
  tim = round(tim,-1)
  li = list(i for i in range(5,500,5) if tim/i < 50)[0] #.01% chance this errors
  tim1 = time.time()
  for _ in range(round(li)):
    key = pygame.key.get_pressed() #so it doesnt say unresponsive lol
    if key[pygame.K_v]:
      print(time.time()-tim1)
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

screensize(1280,720)
HEIGHT = 720
WIDTH = 1280

#------- screen things -------
def show(thing,where=(0,0),thingnightingi=None):
  screen.blit(thing,where,thingnightingi) #3rd arg used for cutoffs

objects = {"home": [], '2nd' : []} #append all showable entities to me!!!!!!!
PLACE = 'home'

def obs():
  for i in objects[PLACE]:
    show(i.image, i.pos)
    
def fill(color,default=screen): #can take RGB too?
  default.fill(color)

def up(thing=False):
  """Pass in either a pygame.Rect(x,y,width,height) or x,y,image"""
  if not thing:
    pygame.display.update()
  else:
    pygame.display.update(thing if type(thing) == pygame.rect.Rect else pygame.Rect(thing[0],thing[1],thing[2].get_width(),thing[2].get_height()))

#------- img things -------
def img(name):
  return pygame.image.load(file(name))

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
      img.set_at((x, y), pygame.Color(a[0] + r if a[0] + r<255 else 255, a[1] + g if a[1] + g < 255 else 255, a[2] + b if a[2] + b < 255 else 255, a[3])) #set things
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
  def play(name, volume = 1, loops = 0):
    """Set loops to -1 for inf"""
    pygame.mixer.music.load(file(name))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops)
  
  @staticmethod
  def stop():
    pygame.mixer.music.stop()
  
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
  def __init__(self, image, starting_cords = (0,0)):
    self.image = image
    self.height = self.image.get_height()
    self.pos = image.get_rect().move(starting_cords[0], starting_cords[1])
    self.width = self.image.get_width()
    
disable_time = 0 #set this to a second value or something and update every tick, to disable movement!!!

class Player:
  def __init__(self, image, speed):
    self.speed = speed
    entity.__init__(self,image) #yoinky sploinky entity
  
  def move(self, up=False, down=False, left=False, right=False):
    if disable_time<=0:
      if right: self.pos.right += self.speed
      elif left: self.pos.right -= self.speed
      if down: self.pos.top += self.speed
      elif up: self.pos.top -= self.speed
      
      if self.pos.right > WIDTH:
          self.pos.right = WIDTH
      if self.pos.right < self.width:
          self.pos.right = self.width
      if self.pos.top > HEIGHT-self.height:
          self.pos.top = HEIGHT-self.height
      if self.pos.top < 0:
          self.pos.top = 0

def touching(thing1:entity,thing2:entity,paddingtop=0,paddingsides=0): #both entites/players
  right = thing2.pos.right<thing1.pos.right-paddingsides and thing2.pos.right>thing1.pos.right-thing1.width+paddingsides
  left = thing2.pos.left>thing1.pos.left+paddingsides and thing2.pos.left<thing1.pos.left+thing1.width-paddingsides
  top = thing2.pos.top>thing1.pos.top+paddingtop and thing2.pos.top<thing1.pos.top+thing1.height-paddingtop
  bottom = thing2.pos.bottom<thing1.pos.bottom and thing2.pos.bottom>thing1.pos.bottom-thing1.height+paddingtop
  return  (right or left) and (top or bottom)




#------------------------------------------------------------- start actual stuff -------------------------------------------------------------

colour=(160,132,173)
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
you = Player(pimgs["down"], 8)
for i in objects:
  objects[i].append(you)

#MATTOON IMAGES
mimgs = {"lean":img("MATLEAN.png"), "pfp":img("MATPFP.jpg"), "stare":img("MATSTARE.png"), "sup":img("MATSUP.png")}
mattoon = entity(mimgs["lean"])
curmat = 0

objects[PLACE].append(mattoon)

def changemattoon():
  global curmat,mattoon
  curmat = 0 if curmat == 3 else curmat+1
  mattoon.image = mimgs[list(mimgs.keys())[curmat]]

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

def wall(size, coord = (0,0), colo = (0,0,0)):
  global objects
  NEW = entity(pygame.Surface(size),coord)
  NEW.image.fill(colo)
  objects[PLACE].append(NEW)

for SIZE,COR in zip([(100,200),(300,300)] , [(0,0),(1280-300,0)]):
  wall(SIZE,COR)


clock = pygame.time.Clock()




#----------------------------------- MAIN GAMEEEEEEEEEE -----------------------------------

while True:
  frame+=1
  
  #background
  backing = color(colour,WIDTH,HEIGHT)
  show(backing,(0,0))
  obs()
  
  #text = pygame.font.Font('FILES/determination.ttf', 32).render(f'R\T to drink petroleum, O\P to control the world [fps:{lagS}]', True, (0,255,0))
  
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
  elif k[pygame.K_0]:
    changemattoon()
    
  if (k[pygame.K_o] or k[pygame.K_p]):
    HEIGHT+=3 if k[pygame.K_p] else -3
    WIDTH+=3 if k[pygame.K_p] else -3
    screensize(WIDTH,HEIGHT)
  
  
  check_events()
  
  up() #passing nothing = full screen update
  lag_time = clock.tick(fps) / 1000 #fps = time since last frame (1 = its fine, can be used in frame dependant animation?)
  
  disable_time -= .5
