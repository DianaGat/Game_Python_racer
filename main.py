import pygame
import random
import math

class MovingMonster():
    def __init__(self, window, image):
        self.image = image
        self.window = window
        self.x_start = random.choice(range(54*3, self.window.get_width() - self.image.get_width()))
        self.y_start = random.choice(range(54*3, self.window.get_height() - self.image.get_height()))
        self.monster_rect = self.image.get_rect(topleft=(self.x_start, self.y_start))
        self.x_saldo = float(0)
        self.y_saldo = float(0)

    def ramdomize_position_for_old_monsters(self):
        self.monster_rect.x = random.choice(range(54*3, self.window.get_width() - self.image.get_width()))
        self.monster_rect.y = random.choice(range(54*3, self.window.get_height() - self.image.get_height()))

    def move(self, robot_rect, letters_area):
        MONSTER_SPEED = 1

        #diff betwen coords of robot and monster:
        x_diff = robot_rect.x - self.monster_rect.x
        y_diff = robot_rect.y - self.monster_rect.y
        next_x_position = self.monster_rect.x
        next_y_position = self.monster_rect.y

        if y_diff == 0:
            if x_diff > 0:
                next_x_position += MONSTER_SPEED
            else:
                next_x_position -= MONSTER_SPEED
        else:
            angle = math.atan2(x_diff, y_diff)
            next_x_position += MONSTER_SPEED * math.sin(angle)
            next_y_position += MONSTER_SPEED * math.cos(angle)
            #to make monsters move smoothly, I use saldo system:
            self.x_saldo += next_x_position % 1
            self.y_saldo += next_y_position % 1
            if self.x_saldo >= 1:
                next_x_position += 1
                self.x_saldo -= 1
            elif self.x_saldo <= -1:
                next_x_position -= 1
                self.x_saldo += 1
            if self.y_saldo >= 1:
                next_y_position += 1
                self.y_saldo -= 1
            elif self.y_saldo <= -1:
                next_y_position -= 1
                self.y_saldo += 1

        self.monster_rect.x = next_x_position
        if x_diff < 0:
            monster_colliding_with_letters = [letter_rect for letter_rect in letters_area if self.monster_rect.colliderect(letter_rect)]
            if monster_colliding_with_letters:
                self.x_saldo = 0.0
                monster_colliding_with_letters_sorted = sorted(monster_colliding_with_letters, key=lambda letter_rect: letter_rect.x, reverse=True)
                self.monster_rect.x = monster_colliding_with_letters_sorted[0].x + monster_colliding_with_letters_sorted[0].width
        if x_diff > 0:
            monster_colliding_with_letters = [letter_rect for letter_rect in letters_area if self.monster_rect.colliderect(letter_rect)]
            if monster_colliding_with_letters:
                self.x_saldo = 0.0
                monster_colliding_with_letters_sorted = sorted(monster_colliding_with_letters, key=lambda letter_rect: letter_rect.x)
                self.monster_rect.x = monster_colliding_with_letters_sorted[0].x - self.monster_rect.width
        
        self.monster_rect.y = next_y_position
        if y_diff < 0:
            monster_colliding_with_letters = [letter_rect for letter_rect in letters_area if self.monster_rect.colliderect(letter_rect)]
            if monster_colliding_with_letters:
                self.y_saldo = 0.0
                monster_colliding_with_letters_sorted = sorted(monster_colliding_with_letters, key=lambda letter_rect: letter_rect.y, reverse=True)
                self.monster_rect.y = monster_colliding_with_letters_sorted[0].y + monster_colliding_with_letters_sorted[0].height
        if y_diff > 0:
            monster_colliding_with_letters = [letter_rect for letter_rect in letters_area if self.monster_rect.colliderect(letter_rect)]
            if monster_colliding_with_letters:
                self.y_saldo = 0.0
                monster_colliding_with_letters_sorted = sorted(monster_colliding_with_letters, key=lambda letter_rect: letter_rect.y)
                self.monster_rect.y = monster_colliding_with_letters_sorted[0].y - self.monster_rect.height

class PythonGame:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.initiate_map()
        self.clock = pygame.time.Clock()

        map_rows = len(self.map)
        map_columns = len(self.map[0])
        scale = int(54)

        window_height = scale * (map_rows + 1)
        window_width = scale * map_columns

        self.window = pygame.display.set_mode((window_width, window_height))

        pygame.display.set_caption("Python Racer")
        self.ROBOT_MOVESPEED = 3
        self.record = 0

        self.new_game()

    def new_game(self):
        self.level = 0
        self.game = True
        self.monster_list = []
        self.coin_counter = 0
        self.main_loop()

    def load_images(self):
        robot = pygame.image.load("robot.png")
        monster = pygame.image.load("monster.png")
        self.coin = pygame.image.load("coin.png")
        self.robot = pygame.transform.scale(robot, (robot.get_width() // 1.5, 40))
        self.monster = pygame.transform.scale(monster, (monster.get_width() // 1.5, 40))
        
        self.robot_rect = self.robot.get_rect()
        self.coin_rect = self.coin.get_rect()

    def initiate_map(self):
        #columns = 28
        #rows = 9

        #0 = empty space
        #1 = letter block
        #3 = coin
        #9 = unreachable area
        self.map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 9, 1, 0, 1, 0, 1, 0, 3, 1, 0, 0, 1, 0, 1, 0, 1, 9, 1, 0, 1, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 9, 1, 0, 1, 3, 1, 1, 0, 0, 3],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 9, 1, 0, 1, 0, 0, 1, 0, 0, 0], 
                    [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    def main_loop(self):
        while self.game == True:
            self.check_events_robot()
            self.check_events_monsters()
            self.draw_window()


    def create_map(self):
        letter_color = (173, 216, 230)
        empty_color = (50, 140, 200)
        
        map_x = 0
        map_y = 0

        self.square_blit_list = []
        self.coins_blit_list = [] 

        self.letters_area = []
        self.coin_area = []

        for row in self.map:
                for square in row:
                    if square == 1:
                        self.square_blit_list.append(lambda letter_color=letter_color, map_x=map_x, map_y=map_y: pygame.draw.rect(self.window, letter_color, (map_x, map_y, map_x + 54, map_y + 54)))
                        self.letters_area.append(pygame.Rect(map_x, map_y, 54, 54))
                    elif square == 0 or square == 9:
                        self.square_blit_list.append(lambda empty_color=empty_color, map_x=map_x, map_y=map_y: pygame.draw.rect(self.window, empty_color, (map_x, map_y, map_x + 54, map_y + 54)))
                        if square == 9:
                            self.letters_area.append(pygame.Rect(map_x, map_y, 54, 54))   
                    elif square == 3:
                        self.square_blit_list.append(lambda empty_color=empty_color, map_x=map_x, map_y=map_y: pygame.draw.rect(self.window, empty_color, (map_x, map_y, map_x + 54, map_y + 54)))
                        self.coins_blit_list.append(lambda map_x=map_x, map_y=map_y: self.window.blit(self.coin, (map_x, map_y), self.coin_rect))
                        self.coin_area.append(pygame.Rect(map_x, map_y, 54, 54))
                    map_x += 54
                map_y += 54
                map_x = 0


    def draw_map(self):
        for rect in self.square_blit_list:
            rect()
        for coin in self.coins_blit_list:
            coin()


    def new_level(self):
        self.level += 1
        self.update_record()

        #initial position of robot:
        self.robot_rect.x = 54
        self.robot_rect.y = self.window.get_height()/2 - self.robot.get_height()

        self.to_right = False
        self.to_left = False
        self.to_top = False
        self.to_bot = False

        self.coin_counter = 3

        #randomize positions of old monsters:
        for monster in self.monster_list:
            monster.ramdomize_position_for_old_monsters()

        # add new monster:
        monster = MovingMonster(self.window, self.monster)
        self.monster_list.append(monster)

    def update_record(self):
        if self.level > self.record:
            self.record = self.level

    def draw_window(self):
        self.window.fill((100, 40, 20))

        if self.coin_counter == 0: # start new lvl
            self.initiate_map()
            self.new_level()
            self.create_map()
            self.draw_map()
        else: # continue game
            self.draw_map() 

        self.window.blit(self.robot, self.robot_rect)
        game_lvl_font = pygame.font.SysFont("Arial", 24)
        game_lvl_text = game_lvl_font.render(f"Level: {self.level}", True, (173, 216, 230))
        self.window.blit(game_lvl_text, (self.window.get_width() - game_lvl_text.get_width() - 50, 0))

        game_start_over_font = pygame.font.SysFont("Arial", 15)
        game_start_again_text = game_start_over_font.render("To start over press F2", True, (173, 216, 230))
        self.window.blit(game_start_again_text, (self.window.get_width() - game_start_again_text.get_width(), self.window.get_height()-game_start_again_text.get_height()))

        for monster in self.monster_list:
            self.window.blit(monster.image, monster.monster_rect)

        self.clock.tick(120)
        pygame.display.flip()
    

    def check_events_robot(self):
        if self.coin_counter == 0:
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_top = True
                if event.key == pygame.K_DOWN:
                    self.to_bot = True
                if event.key == pygame.K_F2:
                    self.new_game()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_top = False
                if event.key == pygame.K_DOWN:
                    self.to_bot = False            

        if self.to_right:
            self.robot_rect.x += self.ROBOT_MOVESPEED
            robot_colliding_with_letter = [letter_rect for letter_rect in self.letters_area if self.robot_rect.colliderect(letter_rect)]
            if robot_colliding_with_letter:
                robot_colliding_with_letter_sorted = sorted(robot_colliding_with_letter, key=lambda letter_rect: letter_rect.x)
                self.robot_rect.x = robot_colliding_with_letter_sorted[0].x - self.robot_rect.width
            if self.robot_rect.x >= self.window.get_width() - self.robot_rect.width:
                self.robot_rect.x = self.window.get_width() - self.robot_rect.width
            self.is_robot_colliding_with_coin()

        if self.to_left:
            self.robot_rect.x -= self.ROBOT_MOVESPEED
            robot_colliding_with_letter = [letter_rect for letter_rect in self.letters_area if self.robot_rect.colliderect(letter_rect)]
            if robot_colliding_with_letter:
                robot_colliding_with_letter_sorted = sorted(robot_colliding_with_letter, key=lambda letter_rect: letter_rect.x, reverse=True)
                self.robot_rect.x = robot_colliding_with_letter_sorted[0].x + robot_colliding_with_letter_sorted[0].width
            if self.robot_rect.x <= 0:
                self.robot_rect.x = 0
            self.is_robot_colliding_with_coin()

        if self.to_top:
            self.robot_rect.y -= self.ROBOT_MOVESPEED
            robot_colliding_with_letter = [letter_rect for letter_rect in self.letters_area if self.robot_rect.colliderect(letter_rect)]
            if robot_colliding_with_letter:
                robot_colliding_with_letter_sorted = sorted(robot_colliding_with_letter, key=lambda letter_rect: letter_rect.y, reverse=True)
                self.robot_rect.y= robot_colliding_with_letter_sorted[0].y + robot_colliding_with_letter_sorted[0].height
            if self.robot_rect.y <= 0:
                self.robot_rect.y = 0
            self.is_robot_colliding_with_coin()

        if self.to_bot:
            self.robot_rect.y += self.ROBOT_MOVESPEED
            robot_colliding_with_letter = [letter_rect for letter_rect in self.letters_area if self.robot_rect.colliderect(letter_rect)]
            if robot_colliding_with_letter:
                robot_colliding_with_letter_sorted = sorted(robot_colliding_with_letter, key=lambda letter_rect: letter_rect.y)
                self.robot_rect.y= robot_colliding_with_letter_sorted[0].y - self.robot_rect.height
            if self.robot_rect.y >= self.window.get_height() - self.robot_rect.height:
                self.robot_rect.y = self.window.get_height() - self.robot_rect.height
            self.is_robot_colliding_with_coin()
            
    def is_robot_colliding_with_coin(self):
        robot_colliding_with_coin = [coin_rect for coin_rect in self.coin_area if self.robot_rect.colliderect(coin_rect)]
        if robot_colliding_with_coin:
            self.coin_counter -= 1
            coin_index = self.coin_area.index(robot_colliding_with_coin[0])
            self.coin_area.pop(coin_index)
            self.coins_blit_list.pop(coin_index)
            
    def check_events_monsters(self):
        for monster in self.monster_list:
            monster.move(self.robot_rect, self.letters_area)
            self.is_robot_colliding_with_monster()

    def is_robot_colliding_with_monster(self):
        robot_monster_colliding =  [monster.monster_rect for monster in self.monster_list if self.robot_rect.colliderect(monster.monster_rect)]
        if robot_monster_colliding:
            self.game_over()

    def game_over(self):
        self.game = False 
        while self.game == False:
            self.window.fill((0, 0, 0))
            
            game_over_font = pygame.font.SysFont("Arial", 180)
            game_over_text1 = game_over_font.render("GAME", True, (255, 0, 0))
            self.window.blit(game_over_text1, (self.window.get_width()/2 - game_over_text1.get_width()/2, self.window.get_height()/2 - game_over_text1.get_height() * 0.95))
           
            game_over_text2 = game_over_font.render("OVER", True, (255, 0, 0))
            self.window.blit(game_over_text2, (self.window.get_width()/2 - game_over_text2.get_width()/2, self.window.get_height()/2 - game_over_text2.get_height() * 0.1))
            
            game_record_font = pygame.font.SysFont("Arial", 20)
            game_over_text3 = game_record_font.render(f"Your record: {self.record}", True, (255, 0, 0))
            self.window.blit(game_over_text3, (self.window.get_width()/2 - game_over_text3.get_width()/2, self.window.get_height()/2 + game_over_text2.get_height() * 1))
            
            game_start_over_font = pygame.font.SysFont("Arial", 15)
            game_start_again_text = game_start_over_font.render("To start over press F2", True, (255, 0, 0))
            self.window.blit(game_start_again_text, (self.window.get_width() - game_start_again_text.get_width(), self.window.get_height()-game_start_again_text.get_height()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F2:
                        self.new_game()
            
            self.clock.tick(1)
            pygame.display.flip()

if __name__ == "__main__":
    PythonGame()