import pygame
import math

# Board Class (Enhanced Visual Layout for Snake and Ladder)
class Board:
    def __init__(self):
        self.squares = self.generate_board()
        self.font_small = pygame.font.SysFont('Arial', 12, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 14, bold=True)

    def generate_board(self):
        # Snake and Ladder mapping (square: destination)
        # Ladders (positive moves) - Tangga
        ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        # Snakes (negative moves) - Ular
        snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        
        # Combine both dictionaries
        board = {**ladders, **snakes}
        return board

    def draw(self, screen):
        # Draw board grid with enhanced visuals
        for row in range(10):
            for col in range(10):
                # Calculate square number based on snake and ladder board layout
                if row % 2 == 0:  # Even rows go left to right
                    square_number = row * 10 + col + 1
                else:  # Odd rows go right to left
                    square_number = row * 10 + (9 - col) + 1
                
                x = col * 80 + 50
                y = (9 - row) * 60 + 50  # Flip Y coordinate so square 1 is at bottom
                
                # Determine square color based on position
                if (row + col) % 2 == 0:
                    square_color = (240, 240, 220)  # Light beige
                else:
                    square_color = (220, 220, 200)  # Slightly darker beige
                
                # Fill square background
                pygame.draw.rect(screen, square_color, (x, y, 80, 60))
                
                # Highlight squares with snakes or ladders
                if square_number in self.squares:
                    if self.squares[square_number] > square_number:
                        # Ladder (green gradient)
                        self.draw_ladder(screen, x, y, square_number, self.squares[square_number])
                    else:
                        # Snake (red gradient)
                        self.draw_snake(screen, x, y, square_number, self.squares[square_number])
                
                # Draw square border
                pygame.draw.rect(screen, (100, 100, 100), (x, y, 80, 60), 2)
                
                # Draw square number with better styling
                number_color = (50, 50, 50)
                if square_number in self.squares:
                    number_color = (255, 255, 255) if self.squares[square_number] > square_number else (255, 255, 255)
                
                text = self.font_medium.render(str(square_number), True, number_color)
                text_rect = text.get_rect(center=(x + 15, y + 15))  # Top-left corner
                screen.blit(text, text_rect)
        
        # Draw legend
        self.draw_legend(screen)

    def draw_ladder(self, screen, x, y, start, end):
        """Draw ladder visualization"""
        # Green gradient background
        colors = [(0, 150, 0), (0, 200, 0), (0, 255, 0)]
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + 2 + i, y + 2 + i, 76 - 2*i, 56 - 2*i)
            pygame.draw.rect(screen, color, rect)
        
        # Draw ladder rungs
        for i in range(4):
            rung_y = y + 10 + i * 12
            pygame.draw.line(screen, (139, 69, 19), (x + 20, rung_y), (x + 60, rung_y), 3)
        
        # Draw ladder sides
        pygame.draw.line(screen, (101, 67, 33), (x + 25, y + 8), (x + 25, y + 52), 4)
        pygame.draw.line(screen, (101, 67, 33), (x + 55, y + 8), (x + 55, y + 52), 4)
        
        # Draw destination arrow and text
        arrow_text = f"↑{end}"
        arrow_surface = self.font_small.render(arrow_text, True, (255, 255, 255))
        screen.blit(arrow_surface, (x + 45, y + 35))

    def draw_snake(self, screen, x, y, start, end):
        """Draw snake visualization"""
        # Red gradient background
        colors = [(150, 0, 0), (200, 0, 0), (255, 0, 0)]
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + 2 + i, y + 2 + i, 76 - 2*i, 56 - 2*i)
            pygame.draw.rect(screen, color, rect)
        
        # Draw snake body (wavy line)
        points = []
        for i in range(8):
            snake_x = x + 15 + i * 7
            snake_y = y + 30 + math.sin(i * 0.8) * 8
            points.append((snake_x, snake_y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 100, 0), False, points, 6)
            pygame.draw.lines(screen, (0, 150, 0), False, points, 4)
        
        # Draw snake head
        head_x, head_y = points[-1] if points else (x + 60, y + 30)
        pygame.draw.circle(screen, (0, 80, 0), (int(head_x), int(head_y)), 8)
        pygame.draw.circle(screen, (255, 255, 0), (int(head_x - 2), int(head_y - 2)), 2)  # Eye
        pygame.draw.circle(screen, (255, 255, 0), (int(head_x + 2), int(head_y - 2)), 2)  # Eye
        
        # Draw destination arrow and text
        arrow_text = f"↓{end}"
        arrow_surface = self.font_small.render(arrow_text, True, (255, 255, 255))
        screen.blit(arrow_surface, (x + 5, y + 35))

    def draw_legend(self, screen):
        """Draw game legend/info"""
        legend_x = 50
        legend_y = 620
        
        # Background for legend
        legend_rect = pygame.Rect(legend_x - 10, legend_y - 5, 800, 25)
        pygame.draw.rect(screen, (0, 0, 0, 100), legend_rect)
        
        # Legend text
        legend_font = pygame.font.SysFont('Arial', 16, bold=True)
        
        # Ladder info
        ladder_text = "🪜 TANGGA: Naik ke kotak yang lebih tinggi"
        ladder_surface = legend_font.render(ladder_text, True, (0, 255, 0))
        screen.blit(ladder_surface, (legend_x, legend_y))
        
        # Snake info
        snake_text = "🐍 ULAR: Turun ke kotak yang lebih rendah"
        snake_surface = legend_font.render(snake_text, True, (255, 0, 0))
        screen.blit(snake_surface, (legend_x + 350, legend_y))

    def get_ladders_and_snakes_info(self):
        """Return detailed info about ladders and snakes"""
        ladders = {k: v for k, v in self.squares.items() if v > k}
        snakes = {k: v for k, v in self.squares.items() if v < k}
        return ladders, snakes

    def get_movement_description(self, start_square, dice_value):
        """Get description of player movement"""
        landing_square = start_square + dice_value
        if landing_square > 100:
            landing_square = 100
        
        if landing_square in self.squares:
            final_square = self.squares[landing_square]
            if final_square > landing_square:
                return f"Mendarat di kotak {landing_square} dan naik tangga ke kotak {final_square}! 🪜"
            else:
                return f"Mendarat di kotak {landing_square} dan turun ular ke kotak {final_square}! 🐍"
        else:
            return f"Pindah ke kotak {landing_square}"