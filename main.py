import pygame, random, sys, os
import pygwidgets

print("Lokasi file ini berada di:", os.path.abspath(__file__))

#general setup
pygame.init()
screen_width, screen_height = 800, 800
screen_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car game")
clock = pygame.time.Clock()
running = True

#Definisi Warna
Red = (255, 0, 0)
Green = (2, 120, 32)
Grey = (180, 180, 180)
White = (255, 255, 255)

#Class list
#Track
class Track:
    def __init__(self):
        self.track_width, self.track_height = 560, 800
        self.track = pygame.Surface((self.track_width, self.track_height))
        self.track_rect = self.track.get_rect(center=(screen_width / 2, screen_height / 2))
        self.left_line_x = screen_width // 5
        self.right_line_x = screen_width - (screen_width // 5)

    def draw(self):
        pygame.draw.rect(screen_display, Grey, self.track_rect)
        pygame.draw.line(screen_display, Green, (screen_width / 2, 0), (screen_height / 2, screen_height), 10) #midline
        pygame.draw.line(screen_display, White, (self.left_line_x, 0), (self.left_line_x, screen_height), 10) #left line
        pygame.draw.line(screen_display, White, (self.right_line_x, 0), (self.right_line_x, screen_height), 10) #right line

#Player
class Player:
    def __init__(self, track):
        self.player = pygame.image.load("Image/Asset Mobil Player.png").convert_alpha()
        self.track = track
        self.player_rect = self.player.get_rect(midbottom = (self.track.left_line_x + 120, screen_height - 30))
        self.is_left = True
        self.move_music = pygame.mixer.Sound("Music/Asset move fx.wav")
        self.move_music.set_volume(2)
    
    def draw(self):
        screen_display.blit(self.player, self.player_rect)

    def move_left(self):
        if not self.is_left:
            self.move_music.play()
            self.player_rect.x = self.track.left_line_x - 10
            self.is_left = True
    
    def move_right(self):
        if self.is_left:
            self.move_music.play()
            self.player_rect.x = self.track.right_line_x - 220
            self.is_left = False
    
    def reset(self):
        self.player_rect.midbottom = (self.track.left_line_x + 120, screen_height - 30)
        self.is_left = True

#Enemy
class Enemy:
    def __init__(self, track):
        self.enemy = pygame.image.load("Image/Asset Mobil Enemy.png").convert_alpha()
        self.track = track
        self.enemy_rect = self.enemy.get_rect(midtop=(self.track.left_line_x + 120, 30))
        self.speed = 5

    def draw(self):
        screen_display.blit(self.enemy, self.enemy_rect)

    def reset_position(self):
        lane = random.choice(["left", "right"])
        if lane == "left":
            self.enemy_rect.midtop = (self.track.left_line_x + 120, - 100)
        else:
            self.enemy_rect.midtop = (self.track.right_line_x - 100, -100)
    
    def update(self):
        max_speed = 30
        self.enemy_rect.y += self.speed
        if self.enemy_rect.y > screen_height:
            self.reset_position()
            if self.speed < max_speed:
                self.speed += 2

#Game class
class Game:
    def __init__(self):
        self.track = Track()
        self.player = Player(self.track)
        self.enemy = Enemy(self.track)
    
        self.start_time = pygame.time.get_ticks()
        self.state = "RUNNING"
        self.score = 0
        self.last_score_update = self.start_time

        #Music setup
        pygame.mixer.init()
        pygame.mixer.music.load("Music/Asset bg music.wav")
        self.game_over_music = pygame.mixer.Sound("Music/Asset game over fx.wav")

        pygame.mixer.music.set_volume(0.4)  
        self.game_over_music.set_volume(0.2)

        # Play the background music
        self.start_music()

    def start_music(self):
        pygame.mixer.music.play(loops=-1)  

    def draw(self):
        self.display_score = pygwidgets.DisplayText(screen_display,
                    (20, 30),
                    value="SCORE ANDA:"+str(self.score),
                    fontName='Courier',
                    fontSize=30,
                    width=350,
                    justified='left',
                    textColor=(0, 0, 0)
                    )
        self.display_title = pygwidgets.DisplayText(screen_display, (260 ,10),
                    value="CAR GAME",
                    fontName='Courier',
                    fontSize=30,
                    width=300,
                    justified='center',
                    textColor=(0, 0, 0)
                    )
        self.track.draw()
        self.player.draw()
        self.enemy.draw()
        self.display_score.draw()
        self.display_title.draw()

    def update(self):
        if self.state != "STOPPED":
            self.enemy.update()
            current_time = pygame.time.get_ticks()
            self.score = (current_time - self.start_time) // 10
            self.check_collision_with_player()
    
    def check_collision_with_player(self):
        if self.player.player_rect.colliderect(self.enemy.enemy_rect):
            pygame.mixer.music.stop()
            self.game_over_music.play()
            self.game_over()

    def reset(self):
        self.player.reset()
        self.enemy.reset_position()
        self.enemy.speed = 5
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.state = "RUNNING"
        self.last_score_update = self.start_time
        self.start_music()

    def game_over(self):
        self.state = "STOPPED"
    

game = Game()

#Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               game.player.move_left()
            elif event.key == pygame.K_RIGHT:
                game.player.move_right()
            elif event.key == pygame.K_r:
                if game.state == "STOPPED":
                    game.reset()

    #update game
    game.update()

    #Render game
    screen_display.fill(Red)
    game.draw()

    #Game over message
    if game.state == "STOPPED":
        game_over_text = pygwidgets.DisplayText(screen_display, (screen_width / 3.5, screen_height // 2),
                    value="GAME OVER! Press R to restart",
                    fontName='Courier',
                    fontSize=20,
                    justified='center',
                    textColor=(0, 0, 0)
                    )
    
        game_over_text.draw()

    #Update display
    pygame.display.update()
    clock.tick(60)


