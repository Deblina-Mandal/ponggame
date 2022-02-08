import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos,size):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos,size, speed):
        super().__init__(path, x_pos, y_pos,size)
        self.size = size
        self.speed = speed
        self.movement = 0

    def screen_condition(self):
        if self.rect.top <= 30:
            self.rect.top = 30
        if self.rect.bottom >= screen_height -30:
            self.rect.bottom = screen_height -30

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_condition()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, size, paddles):
        super().__init__(path, x_pos, y_pos,size)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.size = size
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1


    def  ball_restart(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, white)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2  , screen_height / 2 + 30))
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, size,speed):
        super().__init__(path, x_pos, y_pos,size)
        self.speed = speed
        self.size = size

    def update(self, ball_group):
        current_time = pygame.time.get_ticks()

        if self.rect.top < ball_group.sprite.rect.y:
            if current_time % 7==0:
                pass
            else:
                self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            if current_time % 7==0:
                  pass
            else:
               self.rect.y -= self.speed

        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.ball_restart()
        self.draw_board()

    def ball_restart(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.ball_restart()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.ball_restart()

    def draw_board(self):
        player_score = basic_font.render(str(self.player_score), True, blue)
        opponent_score = basic_font.render(str(self.opponent_score), True, blue)
        player1 = playerno_font.render('Player 1', True, yellow)
        player2 = playerno_font.render('Player 2', True, yellow)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))
        player1_rect = player1.get_rect(topleft=(screen_width / 2 - 400, screen_height / 7))
        player2_rect = player2.get_rect(topright=(screen_width / 2 + 400, screen_height / 7))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)
        screen.blit(player1, player1_rect)
        screen.blit(player2, player2_rect)

    def check_winner(self):
        if self.opponent_score == 3 or self.player_score == 3:
            if self.opponent_score == 3:
                return 0
            if self.player_score == 3:
                return 1

class GameState():
    def __init__(self):
        self.state='intro'
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                 self.state = 'instruction'

        intro1_text = basic_font.render('Click anywhere to continue ^_^', True, yellow)
        intro1_rect = intro1_text.get_rect(center=(600, 600))

        pygame.mixer.Sound.set_volume(welcome_sound,0.8)
        pygame.mixer.Sound.play(welcome_sound)

        screen.blit(introduction1, (0,0))
        screen.blit(introduction2,(100,250))
        screen.blit(intro1_text, intro1_rect)

        pygame.display.update()

    def instruction(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                welcome_sound.stop()
                self.state = 'main_game'

        instruction1_text = instruction1_font.render('USE ARROW KEYS TO MOVE THE PADDLE', True, yellow)
        instruction1_rect = instruction1_text.get_rect(center=(700, 100))
        instruction2_text = instruction2_font.render('CLICK ON START BUTTON TO START THE GAME!', True, yellow)
        instruction2_rect = instruction2_text.get_rect(center=(700, 500))
        instruction3_text = instruction3_font.render('TARGET SCORE: 3' , True, yellow)
        instruction3_rect = instruction3_text.get_rect(center=(700, 550))

        # screen.fill(bg_color1)
        screen.blit(start_button, (0, 0))

        screen.blit(instruction1_text, instruction1_rect)
        screen.blit(instruction2_text, instruction2_rect)
        screen.blit(instruction3_text, instruction3_rect)

        pygame.display.update()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed

        # Background
        screen.blit(background, (0, 0))

        # divider display
        i = 40
        while (i <= screen_height - 40):
            pygame.draw.line(screen, green, (screen_width / 2, i - 10), (screen_width / 2, i), width=8)
            i += 15

        # Run the game
        game_manager.run_game()

        # Check the winner
        if game_manager.check_winner() == 1 or game_manager.check_winner() == 0:
            self.state = 'game_over'
            self.stime=pygame.time.get_ticks()

        # Rendering
        pygame.display.update()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                pygame.quit()
                sys.exit()
        stime2=pygame.time.get_ticks()
        if game_manager.check_winner() == 1:
            gameover_text = gameover_font.render('CONGRATULATIONS! YOU WIN THE GAME!', True, yellow)
            gameover_rect = gameover_text.get_rect(center=(700, 100))
            win_sound.play()
            if stime2-self.stime>=1000:
                win_sound.stop()

        elif game_manager.check_winner() == 0:
            gameover_text = gameover_font.render('YOU LOSE. BETTER LUCK NEXT TIME!', True, yellow)
            gameover_rect = gameover_text.get_rect(center=(700, 100))
            lose_sound.play()
            if stime2-self.stime>=1000:
                lose_sound.stop()



        surface.fill(red)


        screen.blit(gameover, (300, 150))
        screen.blit(gameover_text, gameover_rect)

        pygame.display.update()

    def state_manager(self):
        if self.state == 'intro' :
            self.intro()

        if self.state == 'instruction':
            self.instruction()

        if self.state == 'main_game':
            self.main_game()

        if self.state == 'game_over':
            self.game_over()




# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

game_state=GameState()

# Main Window
screen_width = 1370
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong game')

# Global Variables
green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)
blue = (135,206,250)
yellow=(255,255,0)

# background
bg_surface = pygame.image.load('pong background1.jfif').convert_alpha()
bg_size = (1370, 700)
background = pygame.transform.scale(bg_surface, bg_size)

start_button_surface=pygame.image.load('buttons 4.jfif').convert_alpha()
startbutton_size = (1370, 690)
start_button = pygame.transform.scale(start_button_surface, startbutton_size)

intro1_surface=pygame.image.load('pong intro 8.png').convert_alpha()
intro1_size = (1370, 700)
introduction1 = pygame.transform.scale(intro1_surface, intro1_size)

intro2_surface=pygame.image.load('pong intro9.png').convert_alpha()
intro2_size = (1000, 800)
introduction2 = pygame.transform.scale(intro2_surface, intro2_size)

over_surface=pygame.image.load('gameover.png').convert_alpha()
over_size = (800, 400)
gameover = pygame.transform.scale(over_surface, over_size)

surface = pygame.display.set_mode((1370, 700))

basic_font = pygame.font.Font('freesansbold.ttf', 40)
playerno_font = pygame.font.Font('freesansbold.ttf', 25)
instruction1_font=pygame.font.SysFont('freesansbold.ttf',60,bold=True,italic=True)
instruction2_font=pygame.font.SysFont('freesansbold.ttf',40,bold=True,italic=True)
instruction3_font=pygame.font.SysFont('freesansbold.ttf',40,bold=True,italic=True)
gameover_font=pygame.font.SysFont('freesansbold.ttf',50,bold=True,italic=True)

welcome_sound = pygame.mixer.Sound("welcome.ogg")
plob_sound = pygame.mixer.Sound("Shrink ray.ogg")
pygame.mixer.Sound.set_volume(plob_sound, 0.3)

score_sound = pygame.mixer.Sound("collide.wav")
win_sound = pygame.mixer.Sound("win")
pygame.mixer.Sound.set_volume(win_sound, 0.1)
lose_sound = pygame.mixer.Sound("lose")
pygame.mixer.Sound.set_volume(lose_sound, 0.1)

# Game objects
player = Player('paddle2.png', 1320, 350,(30, 120), 6)
opponent = Opponent('paddle2.png', 40, 350,(30, 120), 7)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('neon ball3.png', screen_width / 2, screen_height / 2 -15, 8, 8, (45,45),paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)


while True:
    game_state.state_manager()
    clock.tick(60)