import pygame
import math

# Board Class (Enhanced Visual Layout for Snake and Ladder)
class Board:
    def __init__(self):
        self.squares = self.generate_board()
        self.font_small = pygame.font.SysFont('Arial', 10, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 12, bold=True)
        
        # Layout configuration yang diperbaiki untuk menghindari overlap
        self.board_start_x = 50   # Posisi board lebih ke kiri
        self.board_start_y = 150  # Berikan ruang untuk header yang lebih besar
        self.square_size = 65     # Ukuran kotak sedikit lebih kecil
        self.square_height = 50   # Tinggi kotak disesuaikan

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
        # Draw board grid dengan posisi yang sudah diperbaiki
        for row in range(10):
            for col in range(10):
                # Calculate square number based on snake and ladder board layout
                if row % 2 == 0:  # Even rows go left to right
                    square_number = row * 10 + col + 1
                else:  # Odd rows go right to left
                    square_number = row * 10 + (9 - col) + 1
                
                # Positioning yang diperbaiki
                x = col * self.square_size + self.board_start_x
                y = (9 - row) * self.square_height + self.board_start_y
                
                # Determine square color based on position
                if (row + col) % 2 == 0:
                    square_color = (240, 240, 220)  # Light beige
                else:
                    square_color = (220, 220, 200)  # Slightly darker beige
                
                # Fill square background
                pygame.draw.rect(screen, square_color, (x, y, self.square_size, self.square_height))
                
                # Highlight squares with snakes or ladders
                if square_number in self.squares:
                    if self.squares[square_number] > square_number:
                        # Ladder (green gradient)
                        self.draw_ladder(screen, x, y, square_number, self.squares[square_number])
                    else:
                        # Snake (red gradient)
                        self.draw_snake(screen, x, y, square_number, self.squares[square_number])
                
                # Draw square border
                pygame.draw.rect(screen, (100, 100, 100), (x, y, self.square_size, self.square_height), 2)
                
                # Draw square number dengan styling yang diperbaiki
                number_color = (50, 50, 50)
                if square_number in self.squares:
                    number_color = (255, 255, 255) if self.squares[square_number] > square_number else (255, 255, 255)
                
                text = self.font_medium.render(str(square_number), True, number_color)
                text_rect = text.get_rect(center=(x + 12, y + 10))
                screen.blit(text, text_rect)
        
        # Draw legend di posisi yang tidak menghalangi
        self.draw_legend(screen)

    def draw_ladder(self, screen, x, y, start, end):
        """Draw ladder visualization dengan ukuran yang disesuaikan"""
        # Green gradient background
        colors = [(0, 150, 0), (0, 200, 0), (0, 255, 0)]
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + 2 + i, y + 2 + i, self.square_size - 4 - 2*i, self.square_height - 4 - 2*i)
            pygame.draw.rect(screen, color, rect)
        
        # Draw ladder rungs (disesuaikan dengan ukuran baru)
        rung_count = 3
        for i in range(rung_count):
            rung_y = y + 6 + i * (self.square_height - 12) // (rung_count - 1)
            pygame.draw.line(screen, (139, 69, 19), (x + 12, rung_y), (x + self.square_size - 12, rung_y), 2)
        
        # Draw ladder sides
        pygame.draw.line(screen, (101, 67, 33), (x + 15, y + 4), (x + 15, y + self.square_height - 4), 3)
        pygame.draw.line(screen, (101, 67, 33), (x + self.square_size - 15, y + 4), (x + self.square_size - 15, y + self.square_height - 4), 3)
        
        # Draw destination arrow and text
        arrow_text = f"↑{end}"
        arrow_surface = self.font_small.render(arrow_text, True, (255, 255, 255))
        screen.blit(arrow_surface, (x + self.square_size - 20, y + self.square_height - 15))

    def draw_snake(self, screen, x, y, start, end):
        """Draw snake visualization dengan ukuran yang disesuaikan"""
        # Red gradient background
        colors = [(150, 0, 0), (200, 0, 0), (255, 0, 0)]
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + 2 + i, y + 2 + i, self.square_size - 4 - 2*i, self.square_height - 4 - 2*i)
            pygame.draw.rect(screen, color, rect)
        
        # Draw snake body (wavy line) - disesuaikan dengan ukuran baru
        points = []
        for i in range(5):
            snake_x = x + 8 + i * (self.square_size - 16) // 4
            snake_y = y + self.square_height // 2 + math.sin(i * 0.8) * 4
            points.append((snake_x, snake_y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 100, 0), False, points, 4)
            pygame.draw.lines(screen, (0, 150, 0), False, points, 2)
        
        # Draw snake head
        head_x, head_y = points[-1] if points else (x + self.square_size - 12, y + self.square_height // 2)
        pygame.draw.circle(screen, (0, 80, 0), (int(head_x), int(head_y)), 4)
        pygame.draw.circle(screen, (255, 255, 0), (int(head_x - 1), int(head_y - 1)), 1)  # Eye
        pygame.draw.circle(screen, (255, 255, 0), (int(head_x + 1), int(head_y - 1)), 1)  # Eye
        
        # Draw destination arrow and text
        arrow_text = f"↓{end}"
        arrow_surface = self.font_small.render(arrow_text, True, (255, 255, 255))
        screen.blit(arrow_surface, (x + 5, y + self.square_height - 15))

    def draw_legend(self, screen):
        """Draw game legend di posisi yang tidak menghalangi board"""
        legend_x = self.board_start_x + 10 * self.square_size + 20  # Di sebelah kanan board
        legend_y = self.board_start_y + 50
        
        # Background for legend
        legend_rect = pygame.Rect(legend_x - 5, legend_y - 5, 250, 60)
        pygame.draw.rect(screen, (0, 0, 0, 120), legend_rect)
        pygame.draw.rect(screen, (200, 200, 200), legend_rect, 2)
        
        # Legend text dengan font yang lebih kecil
        legend_font = pygame.font.SysFont('Arial', 14, bold=True)
        
        # Ladder info
        ladder_text = "🪜 TANGGA: Naik"
        ladder_surface = legend_font.render(ladder_text, True, (0, 255, 0))
        screen.blit(ladder_surface, (legend_x, legend_y))
        
        # Snake info
        snake_text = "🐍 ULAR: Turun"
        snake_surface = legend_font.render(snake_text, True, (255, 0, 0))
        screen.blit(snake_surface, (legend_x, legend_y + 20))
        
        # Additional info
        info_text = "ke kotak tujuan"
        info_surface = pygame.font.SysFont('Arial', 12).render(info_text, True, (200, 200, 200))
        screen.blit(info_surface, (legend_x, legend_y + 40))

    def get_board_bounds(self):
        """Return the boundaries of the game board for player positioning"""
        return {
            'start_x': self.board_start_x,
            'start_y': self.board_start_y,
            'square_size': self.square_size,
            'square_height': self.square_height
        }

    def get_square_position(self, square_number):
        """Get the pixel position of a specific square"""
        if square_number < 1 or square_number > 100:
            return None
        
        # Calculate row and column
        row = (square_number - 1) // 10
        col = (square_number - 1) % 10
        
        # Adjust for alternating row direction
        if row % 2 == 1:  # Odd rows go right to left
            col = 9 - col
        
        x = col * self.square_size + self.board_start_x
        y = (9 - row) * self.square_height + self.board_start_y
        
        return (x + self.square_size // 2, y + self.square_height // 2)  # Return center of square

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