import pygame
from .paddle import Paddle
from .ball import Ball
import os

pygame.mixer.init()

# Game Engine
WHITE = (255, 255, 255)

# Ensure sounds exist (auto-generate if missing)
if not os.path.exists("sounds/paddle_hit.wav"):
    try:
        import generate_sounds
        generate_sounds.main()
    except Exception as e:
        print("Sound generation failed:", e)

# Load sounds
paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
wall_bounce_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")

# Optional volume tuning
paddle_hit_sound.set_volume(0.9)
wall_bounce_sound.set_volume(0.4)
score_sound.set_volume(0.7)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.target_score = 5
        self.game_over = False
        self.winner_text = ""
        self.ai_difficulty = "medium"

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height, difficulty = self.ai_difficulty)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.menu_font = pygame.font.SysFont("Arial", 40)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def show_difficulty_menu(self, screen):
        screen.fill((0, 0, 0))
        title_font = pygame.font.SysFont("Arial", 50)
        menu_font = pygame.font.SysFont("Arial", 35)

        title_text = title_font.render("Select AI Difficulty", True, (255, 255, 255))
        screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))

        options = [
            "Press 1 - Easy",
            "Press 2 - Medium",
            "Press 3 - Hard",
            "Press ESC - Exit"
        ]

        for i, line in enumerate(options):
            text = menu_font.render(line, True, (255, 255, 255))
            screen.blit(text, (self.width // 2 - text.get_width() // 2, 250 + i * 50))

        pygame.display.flip()

        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.ai_difficulty = "easy"
                        waiting = False
                    elif event.key == pygame.K_2:
                        self.ai_difficulty = "medium"
                        waiting = False
                    elif event.key == pygame.K_3:
                        self.ai_difficulty = "hard"
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Update AI paddle with chosen difficulty
        self.ai.difficulty = self.ai_difficulty
        self.ai._setup_difficulty()


    def update(self):

        if self.game_over:
            return

        self.ball.move()

        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width  # reposition to avoid sticking
            self.ball.velocity_x = abs(self.ball.velocity_x)

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x = -abs(self.ball.velocity_x)

        # Then handle wall collisions, scoring, and AI movement
        if self.ball.x <= 0:
            self.ai_score += 1
            score_sound.play()
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            score_sound.play()
            self.ball.reset()

        # Check for game over
        if self.player_score >= self.target_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
        elif self.ai_score >= self.target_score:
            self.game_over = True
            self.winner_text = "AI Wins!"

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        target_text = self.font.render(f"Playing to {self.target_score} points ", True, WHITE)
        screen.blit(target_text, (self.width // 2 - target_text.get_width() // 2, 60))

    def show_game_over(self, screen):
        if not self.game_over:
            return

        game_over_font = pygame.font.SysFont("Arial", 60)
        text = game_over_font.render(self.winner_text, True, WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))

        screen.blit(text, text_rect)
        pygame.display.flip()

        # Pause so the player can read the result
        pygame.time.delay(3000)  # 3 seconds

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_text = ""
        self.ball.reset()

    def show_replay_menu(self, screen):
        SCREEN_COLOR = (0, 0, 0)
        WHITE = (255, 255, 255)
        screen.fill(SCREEN_COLOR)
        menu_font = pygame.font.SysFont("Arial", 30)

        final_score_text = menu_font.render(
            f"Final Score: Player {self.player_score} - AI {self.ai_score}",
            True,
            (255, 255, 255)
        )

        screen.blit(final_score_text, (self.width // 2 - final_score_text.get_width() // 2, self.height // 2 - 150))

        title = self.menu_font.render("Play Again?", True, WHITE)
        opt1 = self.font.render("Press 3 - Best of 3", True, WHITE)
        opt2 = self.font.render("Press 5 - Best of 5", True, WHITE)
        opt3 = self.font.render("Press 7 - Best of 7", True, WHITE)
        opt4 = self.font.render("Press ESC - Exit", True, WHITE)

        # Center text on screen
        screen.blit(title, (self.width//2 - title.get_width()//2, self.height//2 - 100))
        screen.blit(opt1, (self.width//2 - opt1.get_width()//2, self.height//2 - 20))
        screen.blit(opt2, (self.width//2 - opt2.get_width()//2, self.height//2 + 20))
        screen.blit(opt3, (self.width//2 - opt3.get_width()//2, self.height//2 + 60))
        screen.blit(opt4, (self.width//2 - opt4.get_width()//2, self.height//2 + 120))
        pygame.display.flip()

        # Wait for input
        waiting = True
        selected = None
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    selected = "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.target_score = 2  # best of 3 -> first to 2
                        selected = "replay"
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.target_score = 3  # best of 5 -> first to 3
                        selected = "replay"
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.target_score = 4  # best of 7 -> first to 4
                        selected = "replay"
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        selected = "exit"
                        waiting = False

            pygame.time.delay(50)  # small delay to avoid high CPU usage

        return selected
