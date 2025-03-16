import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
INITIAL_PADDLE_SPEED = 7
INITIAL_BALL_SPEED = 7
MIN_SPEED = 3
MAX_SPEED = 15
SPEED_CHANGE = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
SCORE_FONT_SIZE = 64
SPEED_FONT_SIZE = 24
WINNING_SCORE = 5

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.rect = pygame.Rect(WINDOW_WIDTH//2 - BALL_SIZE//2,
                              WINDOW_HEIGHT//2 - BALL_SIZE//2,
                              BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collision (top/bottom)
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Game:
    def __init__(self):
        self.player = Paddle(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2)
        self.opponent = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, 
                             WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2)
        self.ball = Ball()
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.speed_font = pygame.font.Font(None, SPEED_FONT_SIZE)
        self.game_over = False
        self.paddle_speed = INITIAL_PADDLE_SPEED
        self.ball_speed = INITIAL_BALL_SPEED

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Paddle movement
        if keys[pygame.K_w]:
            self.player.move(up=True)
        if keys[pygame.K_s]:
            self.player.move(up=False)
        if keys[pygame.K_UP]:
            self.opponent.move(up=True)
        if keys[pygame.K_DOWN]:
            self.opponent.move(up=False)
            
        # Speed controls
        if keys[pygame.K_1]:  # Decrease paddle speed
            self.paddle_speed = max(MIN_SPEED, self.paddle_speed - SPEED_CHANGE)
            self.player.speed = self.paddle_speed
            self.opponent.speed = self.paddle_speed
        if keys[pygame.K_2]:  # Increase paddle speed
            self.paddle_speed = min(MAX_SPEED, self.paddle_speed + SPEED_CHANGE)
            self.player.speed = self.paddle_speed
            self.opponent.speed = self.paddle_speed
        if keys[pygame.K_3]:  # Decrease ball speed
            self.ball_speed = max(MIN_SPEED, self.ball_speed - SPEED_CHANGE)
            self.ball.speed_x = self.ball_speed * (1 if self.ball.speed_x > 0 else -1)
            self.ball.speed_y = self.ball_speed * (1 if self.ball.speed_y > 0 else -1)
        if keys[pygame.K_4]:  # Increase ball speed
            self.ball_speed = min(MAX_SPEED, self.ball_speed + SPEED_CHANGE)
            self.ball.speed_x = self.ball_speed * (1 if self.ball.speed_x > 0 else -1)
            self.ball.speed_y = self.ball_speed * (1 if self.ball.speed_y > 0 else -1)

    def update(self):
        if not self.game_over:
            self.ball.move()

            # Paddle collision
            if self.ball.rect.colliderect(self.player.rect) or \
               self.ball.rect.colliderect(self.opponent.rect):
                self.ball.speed_x *= -1.1  # Increase speed slightly on paddle hits

            # Score points
            if self.ball.rect.left <= 0:
                self.opponent.score += 1
                self.ball.reset()
            elif self.ball.rect.right >= WINDOW_WIDTH:
                self.player.score += 1
                self.ball.reset()

            # Check for game over
            if self.player.score >= WINNING_SCORE or self.opponent.score >= WINNING_SCORE:
                self.game_over = True

    def draw(self):
        screen.fill(BLACK)
        
        # Draw center line
        pygame.draw.aaline(screen, WHITE, 
                         (WINDOW_WIDTH//2, 0), 
                         (WINDOW_WIDTH//2, WINDOW_HEIGHT))

        # Draw scores
        player_score = self.score_font.render(str(self.player.score), True, WHITE)
        opponent_score = self.score_font.render(str(self.opponent.score), True, WHITE)
        screen.blit(player_score, (WINDOW_WIDTH//4, 20))
        screen.blit(opponent_score, (3*WINDOW_WIDTH//4, 20))

        # Draw speed information
        paddle_speed_text = self.speed_font.render(f'Paddle Speed: {self.paddle_speed}', True, GRAY)
        ball_speed_text = self.speed_font.render(f'Ball Speed: {self.ball_speed}', True, GRAY)
        controls_text = self.speed_font.render('Speed Controls: 1/2 - Paddle, 3/4 - Ball', True, GRAY)
        
        screen.blit(paddle_speed_text, (10, WINDOW_HEIGHT - 70))
        screen.blit(ball_speed_text, (10, WINDOW_HEIGHT - 40))
        screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, WINDOW_HEIGHT - 30))

        # Draw game elements
        self.player.draw()
        self.opponent.draw()
        self.ball.draw()

        # Draw game over message
        if self.game_over:
            winner = "Left" if self.player.score > self.opponent.score else "Right"
            game_over_text = self.score_font.render(f"{winner} Player Wins!", True, WHITE)
            restart_text = self.speed_font.render("Press SPACE to restart", True, GRAY)
            screen.blit(game_over_text, 
                       (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                        WINDOW_HEIGHT//2 - game_over_text.get_height()//2))
            screen.blit(restart_text,
                       (WINDOW_WIDTH//2 - restart_text.get_width()//2,
                        WINDOW_HEIGHT//2 + game_over_text.get_height()))

        pygame.display.flip()

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_SPACE:
                    game = Game()  # Reset the game

        game.handle_input()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()
