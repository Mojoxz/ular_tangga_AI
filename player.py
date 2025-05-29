import pygame

# Player Class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0
        self.rect = pygame.Rect(50, 50, 30, 30)  # Default position
        self.font = pygame.font.SysFont('Arial', 24)

    def move(self, steps):
        self.position += steps
        if self.position > 100:
            self.position = 100  # Limit to 100

    def draw(self, screen):
        # Draw player
        x = (self.position % 10) * 80 + 50  # X-coordinate based on position
        y = (self.position // 10) * 60 + 50  # Y-coordinate based on position
        self.rect.topleft = (x, y)
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw player name
        text = self.font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (x, y - 30))
