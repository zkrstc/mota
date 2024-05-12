import pygame
import sys
import time
import os
import cv2
 
pygame.init()
size=(998,713)
screen=pygame.display.set_mode(size)
class Button(pygame.sprite.Sprite):#按钮类
    def __init__(self,text,fontpath,fontsize,position,color_select=(255,0,0),color_default=(255,255,255),):
        pygame.sprite.Sprite.__init__(self)
        self.text=text
        self.color_default=color_default
        self.color_select=color_select
        self.font=pygame.font.Font(fontpath,fontsize)
        self.font_render=self.font.render(text,True,color_default)
        self.rect=self.font_render.get_rect()
        self.rect.center=position
    def update(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.font_render=self.font.render(self.text,True,self.color_select)
        else:
            self.font_render=self.font.render(self.text,True,self.color_default)
    def draw(self,screen):
        screen.blit(self.font_render,self.rect)


class Config():#设置类
    FONTPATH_CN="font_cn.ttf"
    SCREENSIZE=(998,713)
    hero_dicts={
    'up':'images/player/up.png',
    'down':'images/player/down.png',
    'left':'images/player/left.png',
    'right':'images/player/right.png'
}
    map_dicts={
        '0':'0.lvl',
        '1':'1.lvl',
        '2':'2.lvl'
    }
    FPS=5
    size=(998,713)
    screen=pygame.display.set_mode(size)
    BLOCKSIZE=55
    offset=(336,55)

cfg=Config
class startgameinterface():#开始界面
    def __init__(self,cfg):
        self.cfg=cfg
        self.play_btn=Button('开始游戏',cfg.FONTPATH_CN,50,(cfg.SCREENSIZE[0]//2,cfg.SCREENSIZE[1]-400))
        self.intro_btn = Button('游戏说明', cfg.FONTPATH_CN, 50, (cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1] - 300))
        self.quit_btn = Button('离开游戏', cfg.FONTPATH_CN, 50, (cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1] - 200))
    def showgameintro(self,screen):
            font=pygame.font.Font(self.cfg.FONTPATH_CN,20)
            font_renders=[font.render('魔塔小游戏.',True,(255,255,255)),font.render('游戏素材来自:www.4399.com',True,(255,255,255))]
            rects=[fr.get_rect() for fr in font_renders]
            for idx,rect in enumerate(rects):
                rect.center=self.cfg.SCREENSIZE[0]//2,50*idx+100
            clock=pygame.time.Clock()
            while True:
                screen.fill((0,0,0))
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif event.type==pygame.MOUSEBUTTONDOWN:
                        if event.button==1:
                            mouse_pos=pygame.mouse.get_pos()
                            if self.play_btn.rect.collidepoint(mouse_pos):
                                return True
                            elif self.quit_btn.rect.collidepoint(mouse_pos):
                                pygame.quit()
                                sys.exit(0)
                            elif self.intro_btn.rect.collidepoint(mouse_pos):
                                return
                for btn in [self.intro_btn,self.play_btn,self.quit_btn]:
                    btn.update()
                    btn.draw(screen)
                '''screen.blit(font_render_cn,rect_cn)'''
                for fr,rect in zip(font_renders,rects):
                    screen.blit(fr,rect)
                pygame.display.update() 
                clock.tick(self.cfg.FPS)
    def run(self,screen):
        font=pygame.font.Font(self.cfg.FONTPATH_CN,80)
        
        font_render_cn=font.render('魔塔',True,(255,255,255))
        rect_cn=font_render_cn.get_rect()
        rect_cn.center=self.cfg.SCREENSIZE[0]//2,100
        
        font_render_en=font.render('magictower',True,(255,255,255))
        rect_en=font_render_en.get_rect()
        rect_en.center=self.cfg.SCREENSIZE[0]//2,150
        
        
        clock=pygame.time.Clock()
        flag=1
        while flag:
            screen.fill((0,0,0))
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        mouse_pos=pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            flag=0
                        elif self.quit_btn.rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit(0)
                        elif self.intro_btn.rect.collidepoint(mouse_pos):
                            self.showgameintro(screen)
            for btn in [self.intro_btn,self.play_btn,self.quit_btn]:
                btn.update()
                btn.draw(screen)
            for fr,rect in zip([font_render_cn,font_render_en],[rect_cn,rect_en]):
                screen.blit(fr,rect)
            pygame.display.update() 
            clock.tick(self.cfg.FPS)
        


class map:#解析地图
    def __init__(self,blocksize,filepath,element_images,offset):
        self.count=0
        self.blocksize=cfg.BLOCKSIZE
        self.element_images=element_images
        self.map_matrix=self.parse(filepath)
        self.offset=cfg.offset
        self.hero_x,self.hero_y=0,0
        self.level_pointer=0
        self.monsters_dict = {
    '40': ('绿头怪', 50, 20, 1,10),
    '41': ('红头怪', 70, 15, 2,20),
    '42': ('小蝙蝠', 100, 20, 0,10),
    '43': ('青头怪', 200, 35, 0,40),
    '44': ('骷髅人', 110, 25, 5,50),
    '45': ('骷髅士兵', 150, 40, 20,60),
    '46': ('兽面人', 300, 75, 45,70),
    '47': ('初级卫兵', 450, 150, 90,80),
    '48': ('大蝙蝠', 150, 65, 30,90),
    '49': ('红蝙蝠', 550, 160, 90,100),
    '50': ('白衣武士', 1300, 300, 150,110),
    '51': ('怪王', 700, 250, 125,110),
    '52': ('红衣法师', 500, 400, 260,110),
    '53': ('红衣魔王', 15000, 1000, 1000,110),
    '54': ('金甲卫士', 850, 350, 200,110),
    '55': ('金甲队长', 900, 750, 650,110),
    '56': ('骷髅队长', 400, 90, 50,110),
    '57': ('灵法师', 1500, 830, 730,110),
    '58': ('灵武士', 1200, 980, 900,110),
    '59': ('冥灵魔王', 30000, 1700, 1500,110),
    '60': ('麻衣法师', 250, 120, 70,110),
    '61': ('冥战士', 2000, 680, 590,110),
    '62': ('冥队长', 2500, 900, 850,110),
    '63': ('初级法师', 125, 50, 25,110),
    '64': ('高级法师', 100, 200, 110,110),
    '65': ('石头怪人', 500, 115, 65,110),
    '66': ('兽面战士', 900, 450, 330,110),
    '67': ('双手剑士', 1200, 620, 520,110),
    '68': ('冥卫兵', 1250, 500, 400,110),
    '69': ('高级卫兵', 1500, 560, 460,110),
    '70': ('影子战士', 3100, 1150, 1050,110),
    '188': ('血影', 99999, 5000, 4000,110),
    '198': ('魔龙', 99999, 9999, 5000,110),
}
    def parse(self,filepath):
        map_matrix=[]
        with open(filepath,'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                map_matrix.append([c.strip() for c in line.split(',')])
        return map_matrix#地图矩阵
    
    def draw0(self,screen):#画地图
        gamebg=pygame.transform.scale(pygame.image.load('images/gamebg.png'),size)
        screen.blit(gamebg,(0,0))
        screen.blit(pygame.transform.scale(pygame.image.load('images/blankbg.png'),(605,605)),(cfg.offset[0],cfg.offset[1]))
        FPS=5
        clock=pygame.time.Clock()
        images=[]#images/map0/40.png,images/map1/40.png
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx,elem in enumerate(row):
                position=col_idx*self.blocksize+self.offset[0],row_idx*self.blocksize+self.offset[1]
                if elem+'.png' in self.element_images:
                    for i in range(0, 2):  # 假设我们有4张图片，命名为1.png, 2.png, 3.png, 4.png  
                        imgload = pygame.image.load(f"images/map{i}/"+elem+".png").convert_alpha()  
                        img = pygame.transform.scale(imgload, (self.blocksize, self.blocksize))  # 缩放图片到合适的大小  
                        images.append(img)
                        current_image_index=0
                    screen.blit(images[0],position)
                images.clear()
    def draw1(self,screen):#画地图
        gamebg=pygame.transform.scale(pygame.image.load('images/gamebg.png'),size)
        screen.blit(gamebg,(0,0))
        screen.blit(pygame.transform.scale(pygame.image.load('images/blankbg.png'),(605,605)),(cfg.offset[0],cfg.offset[1]))
        FPS=5
        clock=pygame.time.Clock()
        images=[]#images/map0/40.png,images/map1/40.png
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx,elem in enumerate(row):
                position=col_idx*self.blocksize+self.offset[0],row_idx*self.blocksize+self.offset[1]
                if elem+'.png' in self.element_images:
                    for i in range(0, 2):  # 假设我们有4张图片，命名为1.png, 2.png, 3.png, 4.png  
                        imgload = pygame.image.load(f"images/map{i}/"+elem+".png").convert_alpha()  
                        img = pygame.transform.scale(imgload, (self.blocksize, self.blocksize))  # 缩放图片到合适的大小  
                        images.append(img)
                        current_image_index=0
                    screen.blit(images[1],position)
                images.clear()
        
        '''for row_idx, row in enumerate(self.map_matrix):
            for col_idx,elem in enumerate(row):
                position=col_idx*self.blocksize+self.offset[0],row_idx*self.blocksize+self.offset[1]
                if elem+'.png' in self.element_images:
                    imageload=pygame.image.load('images/'+'map'+'0/'+elem+'.png')
                    image=pygame.transform.scale(imageload,(self.blocksize,self.blocksize))
                    screen.blit(image,position)'''
                  

class Hero(pygame.sprite.Sprite):
    hero_x=5
    hero_y=9
    def __init__(self,imagepaths,blocksize,position,fontpath=None):
        pygame.sprite.Sprite.__init__(self)
        self.font=pygame.font.Font(fontpath,40)
        self.blocksize=blocksize
        self.images={}
        imagepaths=cfg.hero_dicts
        for key,value in imagepaths.items():
            self.images[key]=pygame.transform.scale(pygame.image.load(value),(blocksize,blocksize))
        self.image=self.images['down']#surface
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position   
        self.level=1
        self.life_value=1000
        self.attack_power=10
        self.defense_power=10
        self.experience=0
        self.num_yellow_keys=4
        self.num_purple_keys=0
        self.num_red_keys=0
        self.num_coins=0
        self.fontpath=fontpath
        self.lvl=0
        '''for row_idx, row in enumerate(map_matrix):
            for col_idx,elem in enumerate(row):
                if elem in ['hero']:
                    hero_y=row_idx
                    hero_x=col_idx#相对offset[0],offset[1]的坐标'''
    def draw(self,screen):
        font=pygame.font.Font(self.fontpath,32)
        font_renders=[font.render(str(self.level),True,(255,255,255)),
    font.render(str(self.life_value), True, (255, 255, 255)),
    font.render(str(self.attack_power), True, (255, 255, 255)),
    font.render(str(self.defense_power), True, (255, 255, 255)),
    font.render(str(self.num_coins), True, (255, 255, 255)),
    font.render(str(self.experience), True, (255, 255, 255)),
    font.render(str(self.num_yellow_keys), True, (255, 255, 255)),
    font.render(str(self.num_purple_keys), True, (255, 255, 255)),
    font.render(str(self.num_red_keys), True, (255, 255, 255)),
    font.render(str(self.lvl),True,(255,255,255))]
        rects=[fr.get_rect() for fr in font_renders]
        rects[0].topleft=(160,80)
        for idx in range(1,6):
            rects[idx].topleft=160,127+42*(idx-1)
        for idx in range(6,9):
            rects[idx].topleft=160,364+55*(idx-6)
        rects[9].topleft=(160,540)
        for fr,rect in zip(font_renders,rects):
            screen.blit(fr,rect)
        screen.blit(self.image,self.rect)
    def move(self, direction,map):
        
          # 只需要解析一次关卡
        FORBID = 0
        # 根据方向更新角色的坐标
        if direction == "up":
            
            new_x = Hero.hero_x
            new_y = Hero.hero_y - 1
            
        elif direction == "down":
            new_x = Hero.hero_x
            new_y = Hero.hero_y + 1
        elif direction == "right":
            new_x = Hero.hero_x + 1
            new_y = Hero.hero_y
        elif direction == "left":
            new_x = Hero.hero_x - 1
            new_y = Hero.hero_y
        else:
            new_x, new_y = Hero.hero_x, Hero.hero_y  # 如果方向无效，保持当前位置

        # 检查新位置是否为障碍物
        if new_x==11:
            new_x=10
            FORBID = 1
        elif new_x<0:
            new_x=0
            FORBID=1
        elif new_y==11:
            new_y=10
            FORBID=1
        elif new_y<0:
            new_y=0
            FORBID=1
        if map.map_matrix[new_y][new_x] != '0' and map.map_matrix[new_y][new_x]!='hero' and map.map_matrix[new_y][new_x]!='00' and map.map_matrix[new_y][new_x]!='01':
                FORBID = 1
        
        # 如果不是障碍物，则更新角色的矩形位置
        if FORBID == 0:
        
            if direction == "up":
                new_rect=self.rect.move(0, -self.blocksize)
            elif direction == "down":
                new_rect=self.rect.move(0, self.blocksize)
            elif direction == "right":
                new_rect=self.rect.move(self.blocksize, 0)
            elif direction == "left":
                new_rect=self.rect.move(-self.blocksize, 0)
            self.rect=new_rect
            Hero.hero_x=new_x
            Hero.hero_y=new_y
        # 打印新的矩形位置
        elif FORBID==1:
            if map.map_matrix[new_y][new_x] in ['24','2','3','4','6','7','8','9','10','11','12','13','14','40','41','42','43','44','45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69','71']:#[
                self.dealcollideevent(map.map_matrix[new_y][new_x],(new_y,new_x),map)
                FORBID=0
        self.image=self.images[direction]
        return self.rect
    def winmonster(self,monster):
        if self.attack_power<=monster[3]:return self.deadppt()
        if self.defense_power>=monster[2]:return True
        diff_our=self.attack_power-monster[3]#我打怪物
        diff_monster=monster[2]-self.defense_power#怪物打我
        if round(monster[1]/diff_our)<=round(self.life_value/diff_monster):
            ko=self.life_value-round(monster[1]/diff_our)*diff_our
            if ko<0:
                return self.deadppt()
            else:
                self.life_value=self.life_value-round(monster[1]/diff_our)*diff_our
                return True
        
        else: 
            return self.deadppt()
    def deadppt(self):
        screen.fill((255,255,255))
        imageload=pygame.image.load("images/cxkk.png").convert_alpha()
        img=pygame.transform.scale(imageload,size)
        screen.blit(img,(0,0))
        pygame.display.update()
        time.sleep(2)
        playgame()
            
            
    def dealcollideevent(self,elem,block_position,map_parser):
        if elem in ['2', '3', '4']:
            flag = False
            if elem == '2' and self.num_yellow_keys > 0:
                self.num_yellow_keys -= 1
                flag = True
            elif elem == '3' and self.num_purple_keys > 0:
                self.num_purple_keys -= 1
                flag = True
            elif elem == '4' and self.num_red_keys > 0:
                self.num_red_keys -= 1
                flag = True
            if flag: map_parser.map_matrix[block_position[0]][block_position[1]] = '0'
        elif elem in ['6', '7', '8']:
            if elem == '6': self.num_yellow_keys += 1
            elif elem == '7': self.num_purple_keys += 1
            elif elem == '8': self.num_red_keys += 1
            map_parser.map_matrix[block_position[0]][block_position[1]] = '0'
            return True
            # 捡到宝石
        elif elem in ['9', '10']:
            if elem == '9': self.defense_power += 3
            elif elem == '10': self.attack_power += 3
            map_parser.map_matrix[block_position[0]][block_position[1]] = '0'
            return True
            # 遇到仙女, 进行对话, 并左移一格
        elif elem in ['24']:
            map_parser.map_matrix[block_position[0]][block_position[1] - 1] = elem
            map_parser.map_matrix[block_position[0]][block_position[1]] = '0'#地图矩阵
            return False
        elif elem in ['11','12']:
            if elem =='11':self.life_value+=100
            elif elem=='12':self.life_value+=300
            map_parser.map_matrix[block_position[0]][block_position[1]]='0'
            return True
        elif elem in ['13', '14']:
            global mappointer
            if elem == '13':
                mappointer=mappointer+1#events=['upstairs']
                '''for row_idx, row in enumerate(self.map_matrix):
            for col_idx,elem in enumerate(row):
                position=col_idx*self.blocksize+self.offset[0],row_idx*self.blocksize+self.offset[1]
                if elem+'.png' in self.element_images:
                    imageload=pygame.image.load('image/'+elem+'.png')
                    image=pygame.transform.scale(imageload,(self.blocksize,self.blocksize))
                    screen.blit(image,position)'''
                for row_idx,row in enumerate(mapob[mappointer].map_matrix):
                    for col_idx,elem in enumerate(row):
                        if elem=='00':
                            Hero.hero_x=col_idx
                            Hero.hero_y=row_idx
                            self.lvl=self.lvl+1
                self.rect.left,self.rect.top=cfg.offset[0]+Hero.hero_x*cfg.BLOCKSIZE,cfg.offset[1]+Hero.hero_y*cfg.BLOCKSIZE
            elif elem == '14':
                mappointer=mappointer-1#events=['downstairs']
                for row_idx,row in enumerate(mapob[mappointer].map_matrix):
                    for col_idx,elem in enumerate(row):
                        if elem=='01':
                            Hero.hero_x=col_idx
                            Hero.hero_y=row_idx
                            self.lvl=self.lvl-1
                self.rect.left,self.rect.top=cfg.offset[0]+Hero.hero_x*cfg.BLOCKSIZE,cfg.offset[1]+Hero.hero_y*cfg.BLOCKSIZE
            return True
        elif elem in ['71']:
            self.attack_power+=10
            map_parser.map_matrix[block_position[0]][block_position[1]] = '0'
            return True
        else:
            flager=self.winmonster(map_parser.monsters_dict[elem])
            
            if flager:
                map_parser.map_matrix[block_position[0]][block_position[1]] = '0'
                self.num_coins+=map_parser.monsters_dict[elem][4]
            else:
                exit()
    def control_hero(self,event):
            if event.type == pygame.KEYDOWN:             
                if event.key == pygame.K_w or event.key == pygame.K_UP:  
                    self.move("up",mapob[mappointer])            
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:  
                    self.move("down",mapob[mappointer])
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:  
                    self.move("left",mapob[mappointer])
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:  
                    self.move("right",mapob[mappointer])
                if event.key == pygame.K_4:
                    self.life_value+=100
                if event.key == pygame.K_1:
                    self.num_yellow_keys+=1
                if event.key == pygame.K_2:
                    self.num_purple_keys+=1
                if event.key == pygame.K_3:
                    self.num_red_keys+=1
                if event.key == pygame.K_5:
                    self.attack_power+=1
                if event.key == pygame.K_6:
                    self.defense_power+=1
path = "image" #文件夹路径
def traverse(f):# 将文件名放入列表
    fs = os.listdir(f)
    fs.sort()
    return fs
def namechange(name_list):# 更换文件名后缀,以jpg换csv为例
    portion = os.path.splitext(name_list)
    if portion[1] == ".jpg":
        new_name = portion[0] + ".csv"
    return new_name
namelist = traverse(path)

a=map(cfg.BLOCKSIZE,'0.lvl',namelist,cfg.offset)

'''map_matrix=a.map_matrix
a.draw(screen)
'''
hero=Hero(cfg.hero_dicts,cfg.BLOCKSIZE,(cfg.offset[0]+Hero.hero_x*cfg.BLOCKSIZE,cfg.offset[1]+Hero.hero_y*cfg.BLOCKSIZE),'myfont.ttf')
#position=left,top
maprect=pygame.Rect(cfg.offset[0],cfg.offset[1],11*cfg.BLOCKSIZE,11*cfg.BLOCKSIZE)
pygame.display.update()

def loadmap():
    mapobjects=[]
    for value in ['-1.lvl','0.lvl','1.lvl','2.lvl','3.lvl','4.lvl','5.lvl','6.lvl','7.lvl','8.lvl']:
        a=map(cfg.BLOCKSIZE,value,namelist,cfg.offset)
        mapobjects.append(a)
        print(value)
    return mapobjects
mapob=loadmap()
mappointer=0

b=startgameinterface(cfg)
b.run(screen)        
FFPPSS=10
clock=pygame.time.Clock()
animation_state=0
def playgame():
    global animation_state
    pygame.key.stop_text_input()
    while True:
        clock.tick(FFPPSS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        hero.control_hero(event)

        if animation_state == 0:
            mapob[mappointer].draw0(screen)
            animation_state = 1
        else:
            mapob[mappointer].draw1(screen)
            animation_state = 0
        hero.draw(screen)
        pygame.display.update()    
playgame()