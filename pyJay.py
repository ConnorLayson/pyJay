import pygame
import random
import json

pygame.font.init()
print('Thank you for installing the PyJay v.1.0 pygame engine! PyJay was made by Connor Layson.')

class map:
    def __init__(self,map_info,collider=False,map_x=0,map_y=0,extension='png'):
        with open(map_info,'r') as f:
            self.map_data = f.readlines()
        self.map_x = map_x
        self.map_y = map_y
        self.collider = collider
        self.ext = extension
        
        f = open(self.map_data[1].strip(),'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        self.game_map = []
        for row in data:
            self.game_map.append(list(row))

    def collide(self):
        if self.collider == False:
            print('This map isn\'t set up to be a collider.')
        else:
            rect_list = []
            img_size = int(self.map_data[2].strip())*int(self.map_data[3].strip())
            y = 0
            for row in self.game_map:
                x = 0
                for tile in row:
                    if tile == '0':
                        pass
                    else:
                        rect = pygame.rect.Rect((x*img_size)+self.map_x,(y*img_size)+self.map_y,img_size,img_size)
                        rect_list.append(rect)
                    x += 1
                y += 1
            return rect_list
    
    def display(self,screen,load_box):
        if self.collider:
            print('You can\'t display a collider map.')
        else:
            img_size = int(self.map_data[2].strip())*int(self.map_data[3].strip())
            y = 0
            for row in self.game_map:
                x = 0
                for tile in row:
                    if tile == '0':
                        pass
                    else:
                        hitbox = pygame.Rect((((x*img_size)+self.map_x),((y*img_size)+self.map_y)),(img_size,img_size))
                        if hitbox.colliderect(load_box):
                            img_name = self.map_data[0].strip()+tile+'.'+self.ext
                            img = pygame.image.load(img_name)
                            img = pygame.transform.scale(img,(img_size,img_size))
                            screen.blit(img,(((x*img_size)+self.map_x),((y*img_size)+self.map_y)))
                    x += 1
                y += 1
    
    def move(self,move_x,move_y):
        self.map_x += move_x
        self.map_y += move_y

class interactable(object):
    def __init__(self,file):
        self.file = file
        with open(self.file,"r") as f:
            self.data = json.load(f)
        
        self.map = self.data["map_data"]["file"]
        self.width = self.data["map_data"]["width"]
        self.height = self.data["map_data"]["height"]
        self.map_x = 0
        self.map_y = 0
        
        f = open(self.map,'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        self.game_map = []
        for row in data:
            self.game_map.append(list(row))
        
    def collide(self,plRect):
        y = 0
        self.rect_list = []
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '0':
                    pass
                else:
                    rect = pygame.Rect((x*self.width)+self.map_x,(y*self.height)+self.map_y,self.width,self.height)
                    rect_data = {
                        "rect": rect,
                        "key": tile
                    }
                    self.rect_list.append(rect_data)
                x += 1
            y += 1
        for data_point in self.rect_list:
            if plRect.colliderect(data_point["rect"]):
                for obj in self.data["objects"]:
                    if obj["key"] == data_point["key"]:
                        return obj["function"]
    
    def move(self,move_x,move_y):
        self.map_x += move_x
        self.map_y += move_y
    
    def display(self,screen):
        for tile in self.rect_list:
            pygame.draw.rect(screen,(255,255,0),tile["rect"],1)

class button (object):
    def __init__(self,x,y,text,font=pygame.font.Font(None,50)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_load = self.font.render(text, True, (159, 240, 101))
        self.text_rect = self.text_load.get_rect(center=(self.x,self.y))
        
    def display(self,screen):
        screen.blit(self.text_load, self.text_rect)

    def get_click(self,mosPos):
        if self.text_rect.collidepoint(mosPos):
            return True
        else:
            return False
        
class particle:
    def __init__(self,startX,startY,color,size,speed,lifetime=60):
        self.start_posX = startX
        self.start_posY = startY
        self.x = self.start_posX
        self.y = self.start_posY
        self.dirX = random.randint(-5,5)
        self.dirY = random.randint(-5,5)
        self.speed = speed
        self.size = size
        self.color = color
        self.lifetime = lifetime

    def move(self):
        self.x += self.dirX*self.speed
        self.y += self.dirY*self.speed

    def lifetime_check(self):
        self.lifetime -= 1
        if self.lifetime == 0:
            return True
        else:
            return False
                
    def display(self,screen):
        self.screen = screen
        self.star = pygame.draw.circle(self.screen,self.color,(self.x,self.y),self.size)

class animation:
    def __init__(self,folder,noOfFrames,speed=1,filetype='.png'):
        self.anim_folder = folder
        self.frames = noOfFrames
        self.speed = speed
        self.counter = speed
        self.filetype = filetype
        self.frame = 0

    def slide(self):
        self.counter -= 1
        if self.counter == 0:
            self.counter = self.speed
            self.frame += 1
            if self.frame > self.frames-1:
                self.frame = 0
        self.image = pygame.image.load(self.anim_folder+str(self.frame)+self.filetype)

    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))

class announcement:
    def __init__(self,text,img,color,font,screen):
        self.text = text
        self.img = img
        self.color = color
        self.screen = screen
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(300,100))
        self.font = font
        self.text_load = self.font.render(self.text, True, self.color)
        self.img_x = self.screen.get_width()+(self.img.get_width()/2)
        self.img_y = self.screen.get_height()/2
        self.text_x = 0-(self.img.get_width()/2)
        self.text_y = self.screen.get_height()/2

    def reset(self):
        self.img_x = self.screen.get_width()+(self.img.get_width()/2)
        self.img_y = self.screen.get_height()/2
        self.text_x = 0-(self.img.get_width()/2)
        self.text_y = self.screen.get_height()/2
    
    def display(self):
        self.img_rect = self.img.get_rect(center=(self.img_x,self.img_y))
        self.screen.blit(self.img,self.img_rect)
        
        self.text_rect = self.text_load.get_rect(center=(self.text_x,self.text_y))
        self.screen.blit(self.text_load,self.text_rect)
    
    def move(self):
        dif = abs(self.screen.get_width()/2 - self.text_x)
        if dif < 2:
            dif = 2
        self.text_x += dif/30
        
        imgdif = abs(self.screen.get_width()/2 - self.img_x)
        if imgdif < 2:
            imgdif = 2
        self.img_x -= imgdif/30

class data_management:
    def __init__(self,fileName):
        print('[CONSOLE] Save object created')
        self.name = fileName + '.json'

    def save(self,data):
        with open(self.name,'w') as save_file:
            json.dump(data,save_file,indent=4)
        print('[CONSOLE] Saved the game')

    def load(self):
        with open(self.name) as save_file:
            data = json.load(save_file)
            print('[CONSOLE] Loaded save data')
            return data
