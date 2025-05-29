import pygame
import random

class Dice:
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.value = 1
        self.rect = pygame.Rect(x, y, size, size)
        self.rolling = False
        self.roll_timer = 0
        self.roll_duration = 30  # frames
        
        # Colors
        self.dice_color = (255, 255, 255)
        self.dot_color = (0, 0, 0)
        self.border_color = (0, 0, 0)
        self.hover_color = (240, 240, 240)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def start_roll(self):
        if not self.rolling:
            self.rolling = True
            self.roll_timer = 0

    def update(self):
        if self.rolling:
            self.roll_timer += 1
            # Change value rapidly while rolling
            if self.roll_timer % 3 == 0:  # Change every 3 frames
                self.value = random.randint(1, 6)
            
            # Stop rolling after duration
            if self.roll_timer >= self.roll_duration:
                self.rolling = False
                self.value = random.randint(1, 6)
                return True  # Roll completed
        return False

    def draw(self, screen, mouse_pos=None):
        # Determine color based on hover
        color = self.dice_color
        if mouse_pos and self.rect.collidepoint(mouse_pos) and not self.rolling:
            color = self.hover_color
        
        # Draw dice background
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 3)
        
        # Draw rounded corners effect
        pygame.draw.circle(screen, color, (self.x + 10, self.y + 10), 10)
        pygame.draw.circle(screen, color, (self.x + self.size - 10, self.y + 10), 10)
        pygame.draw.circle(screen, color, (self.x + 10, self.y + self.size - 10), 10)
        pygame.draw.circle(screen, color, (self.x + self.size - 10, self.y + self.size - 10), 10)
        
        # Draw dots based on value
        self.draw_dots(screen)
        
        # Draw roll instruction
        if not self.rolling:
            font = pygame.font.SysFont('Arial', 14)
            instruction = font.render("Klik untuk roll", True, (100, 100, 100))
            instruction_rect = instruction.get_rect(center=(self.x + self.size//2, self.y + self.size + 20))
            screen.blit(instruction, instruction_rect)

    def draw_dots(self, screen):
        dot_size = 8
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        
        # Dot positions relative to center
        positions = {
            1: [(0, 0)],  # Center
            2: [(-20, -20), (20, 20)],  # Diagonal
            3: [(-20, -20), (0, 0), (20, 20)],  # Diagonal + center
            4: [(-20, -20), (20, -20), (-20, 20), (20, 20)],  # Corners
            5: [(-20, -20), (20, -20), (0, 0), (-20, 20), (20, 20)],  # Corners + center
            6: [(-20, -20), (20, -20), (-20, 0), (20, 0), (-20, 20), (20, 20)]  # Two columns
        }
        
        if self.value in positions:
            for dx, dy in positions[self.value]:
                pygame.draw.circle(screen, self.dot_color, 
                                 (center_x + dx, center_y + dy), dot_size)

    def get_value(self):
        return self.value