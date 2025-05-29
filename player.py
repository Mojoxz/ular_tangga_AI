import pygame

# Player Class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1  # Start at square 1, not 0
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.font = pygame.font.SysFont('Arial', 16)

    def move(self, steps, board):
        """Move player and handle snakes and ladders"""
        new_position = self.position + steps
        if new_position > 100:
            new_position = 100  # Limit to 100
        
        self.position = new_position
        
        # Check if landed on snake or ladder
        if self.position in board.squares:
            old_pos = self.position
            self.position = board.squares[self.position]
            if self.position > old_pos:
                print(f"{self.name} climbed a ladder from {old_pos} to {self.position}!")
            else:
                print(f"{self.name} slid down a snake from {old_pos} to {self.position}!")

    def get_screen_position(self):
        """Convert board position to screen coordinates"""
        if self.position < 1:
            return (50, 590)
        
        # Adjust for 1-based indexing
        pos = self.position - 1
        row = pos // 10
        col = pos % 10
        
        # Handle zigzag pattern of snake and ladder board
        if row % 2 == 1:  # Odd rows go right to left
            col = 9 - col
        
        x = col * 80 + 50 + 25  # Center in square
        y = (9 - row) * 60 + 50 + 15  # Center in square, flip Y
        
        return (x, y)

    def draw(self, screen):
        """Draw player on the board"""
        x, y = self.get_screen_position()
        
        # Draw player circle
        pygame.draw.circle(screen, self.color, (x, y), 15)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 15, 2)  # Black border
        
        # Draw player name
        text = self.font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x, y - 25))
        screen.blit(text, text_rect)