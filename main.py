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
        if self.rect.top <= 30 or self.rect.bottom >= screen_height -30:
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
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2  -7, screen_height / 2 + 20))
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
        self.draw_score()

    def ball_restart(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.ball_restart()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.ball_restart()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, green)
        opponent_score = basic_font.render(str(self.opponent_score), True, green)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1370
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong game')

# Global Variables
green = (0, 128, 0)
white = (255,255,255)

# background
bg_surface = pygame.image.load('pong background1.jfif').convert_alpha()
bg_size = (1370, 690)
background = pygame.transform.scale(bg_surface, bg_size)

basic_font = pygame.font.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("snappy sound.mpeg")
score_sound = pygame.mixer.Sound("sweet.ogg")

# Game objects
player = Player('paddle2.png', 1320, 350,(40, 150), 5)
opponent = Opponent('paddle2.png', 40, 350,(40, 150), 7)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('neon ball3.png', screen_width / 2, screen_height / 2 -15, 8, 8, (45,45),paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

while True:
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

    # Rendering
    pygame.display.update()
    clock.tick(60)