import pygame

# Board Class (Static Layout for Snake and Ladder)
class Board:
    def __init__(self):
        self.squares = self.generate_board()

    def generate_board(self):
        # Snake and Ladder mapping (square: destination)
        # Ladders (positive moves)
        ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        # Snakes (negative moves) - adding some snakes for proper gameplay
        snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        
        # Combine both dictionaries
        board = {**ladders, **snakes}
        return board

    def draw(self, screen):
        # Draw board grid
        for row in range(10):
            for col in range(10):
                # Calculate square number based on snake and ladder board layout
                if row % 2 == 0:  # Even rows go left to right
                    square_number = row * 10 + col + 1
                else:  # Odd rows go right to left
                    square_number = row * 10 + (9 - col) + 1
                
                x = col * 80 + 50
                y = (9 - row) * 60 + 50  # Flip Y coordinate so square 1 is at bottom
                
                # Draw square border
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 80, 60), 2)
                
                # Highlight squares with snakes or ladders
                if square_number in self.squares:
                    if self.squares[square_number] > square_number:
                        # Ladder (green)
                        pygame.draw.rect(screen, (0, 255, 0), (x + 2, y + 2, 76, 56))
                    else:
                        # Snake (red)
                        pygame.draw.rect(screen, (255, 0, 0), (x + 2, y + 2, 76, 56))
                
                # Draw square number
                font = pygame.font.SysFont('Arial', 16)
                text = font.render(str(square_number), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 40, y + 30))
                screen.blit(text, text_rect)