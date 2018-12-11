#Bellen, Enrique III M. 2018-01015
#Khong Hun, Angelica 2018-04502
#Miranda, Jerimiah 2018-01845
import pygame, time, datetime, pickle, inspect
#player
class player():
    def __init__(self, stats = 0, willpower = 0, persuasion = 0, courage = 0, endurance = 0, optimism = 0):
        self.stats = stats
        self.willpower = willpower
        self.courage = courage
        self.persuasion = persuasion
        self.endurance = endurance
        self.optimism = optimism

#images
class picture(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file) #loads the image file
        self.rect = self.image.get_rect() #get rectangle of image

class background(picture):
    def __init__(self, image_file): 
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.rect.left, self.rect.top = [0,0] #location of background image

class character(picture):
    def __init__(self, image_file):
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.43), int(self.image.get_height()*0.43))) #scale down the character images
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        self.rect.center = [500,300] #location of character in screen

class character_decision(picture):
    def __init__(self, image_file):
        picture.__init__(self, "assets/" + image_file) #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.43), int(self.image.get_height()*0.43))) #scale down the character images
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        self.rect.center = [700,300] #location of character in screen

class textbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/textbox.png") #call picture initializer
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.90), int(self.image.get_height()*0.90))) #scale down the textbox image
        self.rect = self.image.get_rect() #get rectangle of image after scaling down
        #text
        font = pygame.font.SysFont('Arial', 20, bold, italic) #text format
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words
        space = font.size(' ')[0]  # the width of a space
        max_width, max_height = self.image.get_size() #get dimensions of image
        max_width -= 85 #right margin
        pos = [self.rect.left + 100 ,self.rect.top + 60] #left margin, top margin
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  #reset the x
                    y += word_height  # start on new row
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  #reset the x
            y += word_height  #start on new row
        self.rect.center = [500,500]

class namebox(picture):
    def __init__(self,message):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.70), int(self.image.get_height()*0.90)))
        self.rect = self.image.get_rect()
        self.rect.right,self.rect.top = [950,350]
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("ChopinScript", 35)
        self.textSurf = self.font.render(message, 1, pygame.Color('black'))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [image_width/2, image_height/2 + 10]
        self.image.blit(self.textSurf, self.textRect)

class decisionbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/decisionbox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.80), int(self.image.get_height()*0.80)))
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont('Arial', 20, bold, italic)
        #text
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        max_width -= 10
        pos = [self.rect.left + 45, self.rect.top + 100]
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        self.rect.left, self.rect.top = [20,10]

class button(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/button.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*1.75), int(self.image.get_height()*1.75)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("NORMAL", 10)
        self.textSurf = self.font.render(message, 1, (208, 113 ,4))
        text_width = self.textSurf.get_width()
        text_height = self.textSurf.get_height()
        self.image.blit(self.textSurf, [image_width/2 - text_width/2, image_height/2 - text_height/2])

class button_hover(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/button-hover.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*1.75), int(self.image.get_height()*1.75)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("NORMAL", 10)
        self.textSurf = self.font.render(message, 1, pygame.Color('white'))
        text_width = self.textSurf.get_width()
        text_height = self.textSurf.get_height()
        self.image.blit(self.textSurf, [image_width/2 - text_width/2, image_height/2 - text_height/2])

class load_button(picture):
    def __init__(self, location):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.93), int(self.image.get_height()*0.93)))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location

class shopbox(picture):
    def __init__(self, message, italic = False, bold = True):
        picture.__init__(self, "assets/images/boxes/decisionbox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.80), int(self.image.get_height()*0.80)))
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont('ChopinScript', 35)
        word_surface = font.render("Welcome to the Shop!", 0, pygame.Color('black'))
        pos = [self.rect.left + 45, self.rect.top + 100]
        x, y = pos
        self.image.blit(word_surface, (x, y))
        #text
        font = pygame.font.SysFont('Arial', 20, bold, italic) 
        words = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.image.get_size()
        max_width -= 30
        pos = [self.rect.left + 45, self.rect.top + 150]
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, pygame.Color('black'))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        self.rect.right, self.rect.top = [980,10]

class shop_button(picture):
    def __init__(self, image, location):
        picture.__init__(self, image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.5), int(self.image.get_height()*0.5)))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class shop_button_caption(picture):
    def __init__(self, message, location):
        picture.__init__(self, "assets/images/boxes/namebox.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.93), int(self.image.get_height()*0.93)))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = location
        image_width = self.rect.size[0]
        image_height = self.rect.size[1]        
        self.font = pygame.font.SysFont("ChopinScript", 35)
        self.textSurf = self.font.render(message, 1, pygame.Color('black'))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = [image_width/2, image_height/2 + 10]
        self.image.blit(self.textSurf, self.textRect)

class transparent_black():
    def __init__(self, width, height, location, alpha):
        self.surf = pygame.Surface((width,height))  #the size of your rect
        self.surf.set_alpha(alpha) # alpha level
        self.surf.fill((0,0,0)) #this fills the entire surface
        self.rect = location

#text
class text(pygame.sprite.Sprite):
    def __init__(self, message, font, size, color, bold, italic):
        self.font = pygame.font.SysFont(font, size, bold, italic)
        self.textSurf = self.font.render(message, 1, color)
        self.rect = self.textSurf.get_rect()
        
class main_button(text):
    def __init__(self, message, location, width, height):
        text.__init__(self, message, "Normal", 15, pygame.Color('white'), False, False)
        self.rect.right, self.rect.top = [location[0] + width - 15, location[1] + 10]

class decision_button(text):
    def __init__(self, message, location, width, height):
        text.__init__(self, message, "Arial", 20, pygame.Color('black'), True, False)
        self.rect.center = [location[0] + width/2, location[1] + height/2]

class load_text(text):
    def __init__(self, message, color, location, width, height):
        text.__init__(self, message, "ChopinScript", 27, color, False, False)
        self.rect.center = [location[0] + width/2, location[1] + height/2 + 10]

#music & sounds
class music():
    def __init__(self, music, loop):
        self.music = pygame.mixer.music.load("assets/" + music)
        self.play = pygame.mixer.music.play(loop)

class sound():
    def __init__(self, sound, loop = 0):
        self.sound = pygame.mixer.Sound("assets/" + sound)
        self.play = pygame.mixer.Sound.play(self.sound, loop)

#main game
class window(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode((1000,650))
        self.screen.fill((255,255,255))
        self.clock = pygame.time.Clock()
        pygame.display.update()
        logo = pygame.image.load('assets/images/logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption('World Only I Know')
        pygame.display.update()

    def button_menu(self, message, location, action = None, background = None, scene = None, player = None):
        button_down = button(message, location)
        button_down_hover = button_hover(message, location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + button_down.rect.size[0] > mouse[0] > location[0] and location[1] + button_down.rect.size[1] > mouse[1] > location[1]:
            self.screen.blit(button_down_hover.image, button_down_hover.rect)
            if click[0] == 1 and action != None:
                if action == self.load_game:
                    action(background)
                elif action == self.save_game:
                    action(background, scene)
                elif action == self.shop:
                    action(background, player)
                elif action == "back":
                    return 0
                else:
                    action()

        else:
            self.screen.blit(button_down.image, button_down.rect)

    def main_menu(self, message, location, action = None, background = None, player = None):
        width = 200
        height = 40
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            main_holder = transparent_black(width, height, location, 128)
            self.screen.blit(main_holder.surf, main_holder.rect)
            if click[0] == 1 and action != None:
                if action == self.load_game:
                    action(background)
                elif action == self.scene1:
                    action(0,player)
                else:
                    action()
        main_button_right = main_button(message, location, width, height)
        self.screen.blit(main_button_right.textSurf, main_button_right.rect)

    def decision_menu(self, message, location, action = None, count = None, player = None):
        width = 365
        height = 40
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            main_holder = transparent_black(width, height, location, 50)
            self.screen.blit(main_holder.surf, main_holder.rect)
            if click[0] == 1 and action != None:
                action(count, player)
             
        decision_center = decision_button(message, location, width, height)
        self.screen.blit(decision_center.textSurf, decision_center.rect)

    def load_menu(self, count, location):
        load = load_button(location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        width = load.rect.size[0]
        height = load.rect.size[1]

        try:
            fh = open('assets/save_files/timestamps.txt','r')
        except:
            pass
        try:
            all_timestamp = fh.readlines()
            message = all_timestamp[count]
            message= message.strip()
            fh.close()
        except:
            message = ""

        self.screen.blit(load.image, load.rect)
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            timestamp = load_text(message, (46, 63, 83), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)
            if click[0] == 1:
                if message == "":
                    pass
                else:
                    self.load_scene(count)
        else:     
            timestamp = load_text(message, pygame.Color('black'), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)

    def overwrite_menu(self, count, location, new_timestamp, scene):
        load = load_button(location)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        width = load.rect.size[0]
        height = load.rect.size[1]

        fh = open('assets/save_files/timestamps.txt','r')
        all_timestamp = fh.readlines()
        message = all_timestamp[count]
        message= message.strip()
        fh.close()
        self.screen.blit(load.image, load.rect)
        if location[0] + width > mouse[0] > location[0] and location[1] + height > mouse[1] > location[1]:
            timestamp = load_text(message, (46, 63, 83), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)
            if click[0] == 1:
                return self.overwrite(count,new_timestamp, scene)
        else:     
            timestamp = load_text(message, pygame.Color('black'), location, width, height)
            self.screen.blit(timestamp.textSurf, timestamp.rect)       

    def overwrite(self, count, new_timestamp, scene):
        fh = open('assets/save_files/timestamps.txt','r')
        all_timestamp = fh.readlines()
        all_timestamp[count] = new_timestamp + "\n"
        fh = open('assets/save_files/timestamps.txt', 'w')
        fh.writelines(all_timestamp)
        fh.close()
        data = {"scene" : scene[0], "scene count": scene[1], "player": scene[2]}
        with open(("assets/save_files/save" + str(count) + ".txt"),'wb') as fh:
            pickle.dump(data,fh)
        return 0

    def load_scene(self, count):
        with open("assets/save_files/save" + str(count) + ".txt",'rb') as fh:
            data = pickle.load(fh)
        scene = "".join(("self.",data["scene"],"(",str(data['scene count']),",player(",str(data['player'].stats),",", str(data['player'].willpower),",", str(data['player'].persuasion),",", str(data['player'].courage),",", str(data['player'].endurance), ",", str(data['player'].optimism),"))"))
        eval(scene)

    def exit_game(self):
        pygame.quit()
        quit()

    def load_game(self, background):
        load_game = True

        while load_game:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))

            self.load_menu(0, [70,60])
            self.load_menu(1, [508,60])
            self.load_menu(2, [70,124])
            self.load_menu(3, [508,124])
            self.load_menu(4, [70,188])
            self.load_menu(5, [508,188])
            self.load_menu(6, [70,252])
            self.load_menu(7, [508,252])
            self.load_menu(8, [70,316])
            self.load_menu(9, [508,316])
            back = self.button_menu("BACK", [400,500], "back")
            if back == 0:
                load_game = False
            pygame.display.update()
            self.clock.tick(60)

    def save_game(self, background, scene = None, save_game = True):
        new_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        try:
            fh = open("assets/save_files/timestamps.txt", "r")
        except:
            fh = open("assets/save_files/timestamps.txt", "w")
            fh.close()
            fh = open("assets/save_files/timestamps.txt", "r")
        try:
            for i, l in enumerate(fh):
                pass
            i += 1
        except:
            i = 0
        while save_game:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))
            if i <= 9:
                fh = open("assets/save_files/timestamps.txt", "a")
                fh.write(new_timestamp + "\n")
                fh.close()
                data = {"scene" : scene[0], "scene count": scene[1], "player": scene[2]}
                with open(("assets/save_files/save" + str(i) + ".txt"),'wb') as fh:
                    pickle.dump(data,fh)
                save_game = False
            else:
                l1 = self.overwrite_menu(0, [70,60], new_timestamp, scene)
                l2 = self.overwrite_menu(1, [508,60],new_timestamp, scene)
                l3 = self.overwrite_menu(2, [70,124],new_timestamp, scene)
                l4 = self.overwrite_menu(3, [508,124],new_timestamp, scene)
                l5 = self.overwrite_menu(4, [70,188],new_timestamp, scene)
                l6 = self.overwrite_menu(5, [508,188],new_timestamp, scene)
                l7 = self.overwrite_menu(6, [70,252],new_timestamp, scene)
                l8 = self.overwrite_menu(7, [508,252],new_timestamp, scene)
                l9 = self.overwrite_menu(8, [70,316],new_timestamp, scene)
                l10 = self.overwrite_menu(9, [508,316],new_timestamp, scene)
                instructions = textbox("Click on the timestamps above to overwrite.")
                self.screen.blit(instructions.image, instructions.rect)
                if 0 in [l1,l2,l3,l4,l5,l6,l7,l8,l9,l10]:
                    save_game = False
            pygame.display.update()
            self.clock.tick(60)


    def shop(self, background, player, shop = True):
        while shop:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if player.stats > 0:
                        if event.key == pygame.K_w:
                            player.willpower += 1
                            player.stats -= 1
                        if event.key == pygame.K_p:
                            player.persuasion += 1
                            player.stats -= 1
                        if event.key == pygame.K_c:
                            player.courage += 1
                            player.stats -= 1
                        if event.key == pygame.K_e:
                            player.endurance += 1
                            player.stats -= 1
                        if event.key == pygame.K_o:
                            player.optimism += 1
                            player.stats -= 1
                        
            if background:
                self.screen.blit(background.image,background.rect)
            else:
                self.screen.fill((0,0,0))
            shop = shopbox("Increase your skills by spending your stat points. These skills will be valuable to the story. One stat point will be spent for one key press.\n\nW = Willpower\nP = Persuasion\nC = Courage\nE = Endurance\nO = Optimism\n\nCurrent Stat Points:" + str(player.stats))
            willpower = shop_button("assets/images/shop/willpower.png",[50,50])
            persuasion = shop_button("assets/images/shop/persuasion.png",[50,151])
            courage = shop_button("assets/images/shop/courage.png",[50,252])
            endurance = shop_button("assets/images/shop/endurance.png",[50,353])
            optimism = shop_button("assets/images/shop/optimism.png",[50,454])
            w_cap = shop_button_caption("Willpower: " + str(player.willpower), [170,50])
            p_cap = shop_button_caption("Persuasion: " + str(player.persuasion), [170,151])
            c_cap = shop_button_caption("Courage: " + str(player.courage), [170,252])
            e_cap = shop_button_caption("Endurance: " + str(player.endurance), [170,353])
            o_cap = shop_button_caption("Optimism: " + str(player.optimism), [170,454])
            self.screen.blit(willpower.image, willpower.rect)
            self.screen.blit(w_cap.image, w_cap.rect)
            self.screen.blit(persuasion.image, persuasion.rect)
            self.screen.blit(p_cap.image, p_cap.rect)
            self.screen.blit(courage.image, courage.rect)
            self.screen.blit(c_cap.image, c_cap.rect)
            self.screen.blit(endurance.image, endurance.rect)
            self.screen.blit(e_cap.image, e_cap.rect)
            self.screen.blit(optimism.image, optimism.rect)
            self.screen.blit(o_cap.image, o_cap.rect)
            self.screen.blit(shop.image, shop.rect)
            
            back = self.button_menu("BACK", [750,500], "back")
            if back == 0:
                return player
            pygame.display.update()
            self.clock.tick(60)

    def main_screen(self):
        pygame.mixer.music.stop()
        bg_music = music("assets/music/background_music/Dream Culture.mp3", 1)
        bg  = background('assets/images/backgrounds/main.png')
        main_screen = True

        while main_screen:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
            self.screen.fill((255,255,255))
            self.screen.blit(bg.image, bg.rect)
            self.main_menu("NEW GAME", [750,400], self.scene1, None, player(10,0,0,0,0,0))
            self.main_menu("LOAD GAME", [750,440], self.load_game, background('assets/images/backgrounds/main_notext.png'))
            self.main_menu("EXIT", [750,480], self.exit_game)
            pygame.display.update()
            self.clock.tick(60)

    def credits():
        bg = background('assets/images/backgrounds/credits.jpg')
        while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill((255,255,255))
            self.screen.blit(bg.image, bg.rect)
            self.button_menu("MAIN MENU", [575,600], self.main_screen)

if __name__ == "__main__":
    display = window()
    display.main_screen()

#Desktop/UP_Files/EEE_111/DesignProject
