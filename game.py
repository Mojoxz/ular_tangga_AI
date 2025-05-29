import pygame
import random
import time

# Dice Class
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

# Game Logic
class Game:
    def __init__(self, screen, game_mode="1v1"):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Import here to avoid circular import
        from board import Board
        from player import Player
        
        self.board = Board()
        self.game_mode = game_mode
        
        # Initialize players based on mode
        if game_mode == "1v1":
            self.player1 = Player("Player 1", (255, 0, 0))  # Red
            self.player2 = Player("Player 2", (0, 0, 255))  # Blue
        else:  # 1vcomputer
            self.player1 = Player("Player", (255, 0, 0))  # Red
            self.player2 = Player("Computer", (0, 0, 255), is_computer=True)  # Blue
        
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.waiting_for_roll = True
        
        # Initialize dice
        self.dice = Dice(750, 300)
        
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Set initial message based on player type
        if self.current_player.is_computer:
            self.message = "Computer sedang berpikir..."
            self.current_player.set_move_time()
        else:
            self.message = "Klik dadu untuk roll"
        
        # Animation variables
        self.moving_animation = False
        self.animation_start_pos = 1
        self.animation_target_pos = 1
        self.animation_progress = 0

    def draw(self):
        # Fill background with dark green
        self.screen.fill((0, 100, 0))
        
        # Draw board
        self.board.draw(self.screen)
        
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        # Draw dice
        mouse_pos = pygame.mouse.get_pos()
        self.dice.draw(self.screen, mouse_pos)
        
        # Draw game info
        self.draw_game_info()
        
        # Draw back to menu button
        self.draw_back_button()
        
        pygame.display.flip()

    def draw_game_info(self):
        """Draw current player, dice value, and messages"""
        # Current player info with highlight
        current_text = f"Giliran: {self.current_player.name}"
        text_surface = pygame.font.SysFont('Arial', 28, bold=True).render(current_text, True, self.current_player.color)
        self.screen.blit(text_surface, (50, 10))
        
        # Player positions in boxes
        self.draw_player_info_box(self.player1, 50, 50)
        self.draw_player_info_box(self.player2, 300, 50)
        
        # Game mode
        mode_text = f"Mode: {self.game_mode}"
        mode_surface = pygame.font.SysFont('Arial', 20).render(mode_text, True, (255, 255, 255))
        self.screen.blit(mode_surface, (550, 50))
        
        # Dice value display
        if self.dice.value > 0:
            dice_text = f"Dadu: {self.dice.value}"
            dice_surface = pygame.font.SysFont('Arial', 24, bold=True).render(dice_text, True, (255, 255, 0))
            self.screen.blit(dice_surface, (750, 250))
        
        # Message
        message_surface = self.font.render(self.message, True, (255, 255, 255))
        message_rect = pygame.Rect(50, 580, 600, 30)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), message_rect)
        self.screen.blit(message_surface, (55, 585))
        
        # Game over message
        if self.game_over and self.winner:
            self.draw_win_screen()

    def draw_player_info_box(self, player, x, y):
        """Draw player info in a styled box"""
        box_rect = pygame.Rect(x, y, 200, 80)
        
        # Highlight current player's box
        if player == self.current_player:
            pygame.draw.rect(self.screen, player.color, box_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 3)
            text_color = (255, 255, 255)
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), box_rect)
            pygame.draw.rect(self.screen, (150, 150, 150), box_rect, 2)
            text_color = (200, 200, 200)
        
        # Player name
        name_surface = pygame.font.SysFont('Arial', 20, bold=True).render(player.name, True, text_color)
        self.screen.blit(name_surface, (x + 10, y + 10))
        
        # Player position
        pos_text = f"Kotak: {player.position}"
        pos_surface = pygame.font.SysFont('Arial', 18).render(pos_text, True, text_color)
        self.screen.blit(pos_surface, (x + 10, y + 35))
        
        # Player type
        type_text = "Computer" if player.is_computer else "Human"
        type_surface = pygame.font.SysFont('Arial', 14).render(type_text, True, text_color)
        self.screen.blit(type_surface, (x + 10, y + 55))

    def draw_win_screen(self):
        """Draw victory screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((900, 650))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Victory message
        win_text = f"{self.winner.name} MENANG!"
        win_surface = pygame.font.SysFont('Arial', 60, bold=True).render(win_text, True, (255, 255, 0))
        win_rect = win_surface.get_rect(center=(450, 250))
        self.screen.blit(win_surface, win_rect)
        
        # Final positions
        final_text = f"Posisi Final - {self.player1.name}: {self.player1.position}, {self.player2.name}: {self.player2.position}"
        final_surface = pygame.font.SysFont('Arial', 24).render(final_text, True, (255, 255, 255))
        final_rect = final_surface.get_rect(center=(450, 320))
        self.screen.blit(final_surface, final_rect)
        
        # Instructions
        restart_text = "Tekan R untuk main lagi | Tekan M untuk menu utama"
        restart_surface = pygame.font.SysFont('Arial', 20).render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(450, 380))
        self.screen.blit(restart_surface, restart_rect)

    def draw_back_button(self):
        """Draw back to menu button"""
        button_rect = pygame.Rect(750, 580, 120, 40)
        pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        button_text = pygame.font.SysFont('Arial', 18).render("Menu Utama", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        return button_rect

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_m and self.game_over:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check back button
                    back_button = self.draw_back_button()
                    if back_button.collidepoint(mouse_pos):
                        return "menu"
                    
                    # Check dice click
                    if (self.dice.is_clicked(mouse_pos) and 
                        self.waiting_for_roll and 
                        not self.game_over and 
                        not self.current_player.is_computer):
                        self.roll_and_move()
        
        return None

    def roll_and_move(self):
        """Roll dice and move current player"""
        self.dice.start_roll()
        self.waiting_for_roll = False
        self.message = f"{self.current_player.name} sedang roll dadu..."

    def update_game(self):
        """Update game state"""
        # Update dice animation
        if self.dice.update():  # Dice roll completed
            dice_value = self.dice.get_value()
            self.move_player(dice_value)
        
        # Handle computer player
        if (self.current_player.is_computer and 
            self.waiting_for_roll and 
            not self.game_over and
            self.current_player.should_computer_roll()):
            self.roll_and_move()

    def move_player(self, dice_value):
        """Move player and handle game logic"""
        old_position = self.current_player.position
        self.current_player.move(dice_value, self.board)
        
        # Update message based on movement
        if self.current_player.position != old_position + dice_value:
            # Landed on snake or ladder
            if self.current_player.position > old_position + dice_value:
                self.message = f"{self.current_player.name} naik tangga! {old_position + dice_value} → {self.current_player.position}"
            else:
                self.message = f"{self.current_player.name} kena ular! {old_position + dice_value} → {self.current_player.position}"
        else:
            self.message = f"{self.current_player.name} pindah ke kotak {self.current_player.position}"
        
        # Check for win condition
        if self.current_player.position >= 100:
            self.current_player.position = 100
            self.game_over = True
            self.winner = self.current_player
            self.message = f"{self.current_player.name} menang!"
        else:
            # Switch to next player
            self.switch_player()
            
            # Update message for next player
            if self.current_player.is_computer:
                self.message += " | Computer sedang berpikir..."
                self.current_player.set_move_time()
            else:
                self.message += " | Klik dadu untuk roll"
        
        self.waiting_for_roll = True

    def switch_player(self):
        """Switch to the other player"""
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def restart_game(self):
        """Restart the game"""
        self.player1.position = 1
        self.player2.position = 1
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.dice.value = 1
        self.waiting_for_roll = True
        
        if self.current_player.is_computer:
            self.message = "Computer sedang berpikir..."
            self.current_player.set_move_time()
        else:
            self.message = "Klik dadu untuk roll"

    def run(self):
        """Main game loop"""
        while True:
            result = self.handle_input()
            if result:
                return result
            
            self.update_game()
            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth animation