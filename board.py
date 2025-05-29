import pygame

# Board Class (Static Layout for Snake and Ladder)
class Board:
    def __init__(self):
        self.squares = self.generate_board()

    def generate_board(self):
        # Snake and Ladder mapping
        board = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        return board

    def draw(self, screen):
        # Draw board
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, (255, 255, 255), (i * 80 + 50, j * 60 + 50, 80, 60), 2)
                square_number = i + j * 10 + 1
                if square_number in self.squares:
                    pygame.draw.rect(screen, (255, 0, 0), (i * 80 + 50, j * 60 + 50, 80, 60), 2)  # Highlight snake/ladder
