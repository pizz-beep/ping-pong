import pygame, random

class Paddle:
    def __init__(self, x, y, width, height, difficulty = "medium"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_speed = 10
        self.difficulty = difficulty
        self._setup_difficulty()

        self.reaction_timer = 0

    def _setup_difficulty(self):
        if self.difficulty == "easy":
            self.speed = self.base_speed * 0.8
            self.reaction_delay = 2  # frames between reactions
            self.error_margin = 15
        elif self.difficulty == "hard":
            self.speed = self.base_speed * 1.5
            self.reaction_delay = 2
            self.error_margin = 5
        else:  # medium
            self.speed = self.base_speed
            self.reaction_delay = 2
            self.error_margin = 10

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        # Wait some frames before reacting (simulate delay)
        self.reaction_timer += 1
        if self.reaction_timer < self.reaction_delay:
            return
        self.reaction_timer = 0

        # Introduce imperfection with error margin
        target_y = ball.y + random.randint(-self.error_margin, self.error_margin)

        if target_y < self.y:
            self.move(-self.speed, screen_height)
        elif target_y > self.y + self.height:
            self.move(self.speed, screen_height)
