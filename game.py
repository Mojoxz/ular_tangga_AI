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
        
        # Enhanced Colors
        self.dice_color = (250, 250, 250)
        self.dot_color = (45, 45, 45)
        self.border_color = (80, 80, 80)
        self.hover_color = (255, 255, 220)
        self.shadow_color = (0, 0, 0, 50)

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
        # Draw shadow effect
        shadow_rect = pygame.Rect(self.x + 3, self.y + 3, self.size, self.size)
        shadow_surface = pygame.Surface((self.size, self.size))
        shadow_surface.set_alpha(100)
        shadow_surface.fill((0, 0, 0))
        screen.blit(shadow_surface, shadow_rect)
        
        # Determine color based on hover
        color = self.dice_color
        if mouse_pos and self.rect.collidepoint(mouse_pos) and not self.rolling:
            color = self.hover_color
        
        # Draw dice background with gradient effect
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 4)
        
        # Draw inner highlight for 3D effect
        inner_rect = pygame.Rect(self.x + 3, self.y + 3, self.size - 6, self.size - 6)
        pygame.draw.rect(screen, (255, 255, 255, 50), inner_rect, 2)
        
        # Draw rounded corners effect with better styling
        corner_radius = 12
        pygame.draw.circle(screen, color, (self.x + corner_radius, self.y + corner_radius), corner_radius)
        pygame.draw.circle(screen, color, (self.x + self.size - corner_radius, self.y + corner_radius), corner_radius)
        pygame.draw.circle(screen, color, (self.x + corner_radius, self.y + self.size - corner_radius), corner_radius)
        pygame.draw.circle(screen, color, (self.x + self.size - corner_radius, self.y + self.size - corner_radius), corner_radius)
        
        # Draw dots based on value
        self.draw_dots(screen)
        
        # Draw roll instruction with better styling
        if not self.rolling:
            font = pygame.font.SysFont('Arial', 16, bold=True)
            instruction = font.render("Klik untuk roll", True, (255, 255, 255))
            # Draw text background
            text_rect = instruction.get_rect(center=(self.x + self.size//2, self.y + self.size + 25))
            bg_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 2, text_rect.width + 10, text_rect.height + 4)
            pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)
            screen.blit(instruction, text_rect)

    def draw_dots(self, screen):
        dot_size = 10
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
                # Draw dot shadow
                pygame.draw.circle(screen, (0, 0, 0, 80), 
                                 (center_x + dx + 1, center_y + dy + 1), dot_size)
                # Draw main dot
                pygame.draw.circle(screen, self.dot_color, 
                                 (center_x + dx, center_y + dy), dot_size)
                # Draw dot highlight
                pygame.draw.circle(screen, (255, 255, 255, 100), 
                                 (center_x + dx - 2, center_y + dy - 2), dot_size//3)

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
            self.player1 = Player("Player 1", (220, 20, 60))  # Enhanced Red
            self.player2 = Player("Player 2", (30, 144, 255))  # Enhanced Blue
        else:  # 1vcomputer
            self.player1 = Player("Player", (220, 20, 60))  # Enhanced Red
            self.player2 = Player("Computer", (30, 144, 255), is_computer=True)  # Enhanced Blue
        
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.waiting_for_roll = True
        
        # Initialize dice
        self.dice = Dice(750, 300)
        
        # Enhanced fonts
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.main_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.info_font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
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
        # Enhanced background with gradient effect
        for y in range(650):
            color_ratio = y / 650
            r = int(20 + (50 - 20) * color_ratio)
            g = int(120 + (80 - 120) * color_ratio)
            b = int(20 + (50 - 20) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (900, y))
        
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
        # Enhanced header background
        header_rect = pygame.Rect(0, 0, 900, 140)
        header_surface = pygame.Surface((900, 140))
        header_surface.set_alpha(200)
        header_surface.fill((25, 25, 25))
        self.screen.blit(header_surface, header_rect)
        
        # Current player info with enhanced styling
        current_text = f"Giliran: {self.current_player.name}"
        text_surface = self.title_font.render(current_text, True, self.current_player.color)
        # Add text shadow
        shadow_surface = self.title_font.render(current_text, True, (0, 0, 0))
        self.screen.blit(shadow_surface, (52, 12))
        self.screen.blit(text_surface, (50, 10))
        
        # Player positions in enhanced boxes
        self.draw_player_info_box(self.player1, 50, 50)
        self.draw_player_info_box(self.player2, 300, 50)
        
        # Game mode with better styling
        mode_text = f"Mode: {self.game_mode}"
        mode_surface = self.info_font.render(mode_text, True, (255, 255, 255))
        mode_bg = pygame.Rect(545, 45, 120, 30)
        pygame.draw.rect(self.screen, (60, 60, 60), mode_bg)
        pygame.draw.rect(self.screen, (255, 255, 255), mode_bg, 2)
        mode_rect = mode_surface.get_rect(center=mode_bg.center)
        self.screen.blit(mode_surface, mode_rect)
        
        # Enhanced dice value display
        if self.dice.value > 0:
            dice_text = f"Dadu: {self.dice.value}"
            dice_surface = self.main_font.render(dice_text, True, (255, 215, 0))
            dice_bg = pygame.Rect(745, 245, 90, 35)
            pygame.draw.rect(self.screen, (40, 40, 40), dice_bg)
            pygame.draw.rect(self.screen, (255, 215, 0), dice_bg, 3)
            dice_rect = dice_surface.get_rect(center=dice_bg.center)
            self.screen.blit(dice_surface, dice_rect)
        
        # Enhanced message area
        message_rect = pygame.Rect(40, 570, 620, 50)
        pygame.draw.rect(self.screen, (40, 40, 40), message_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), message_rect, 3)
        
        # Add gradient to message box
        for i in range(message_rect.height):
            alpha = 50 + i * 2
            color = (60 + i, 60 + i, 60 + i)
            pygame.draw.line(self.screen, color, 
                           (message_rect.x, message_rect.y + i), 
                           (message_rect.x + message_rect.width, message_rect.y + i))
        
        message_surface = self.info_font.render(self.message, True, (255, 255, 255))
        message_text_rect = message_surface.get_rect(center=message_rect.center)
        self.screen.blit(message_surface, message_text_rect)
        
        # Game over message
        if self.game_over and self.winner:
            self.draw_win_screen()

    def draw_player_info_box(self, player, x, y):
        """Draw player info in a styled box"""
        box_rect = pygame.Rect(x, y, 220, 85)
        
        # Enhanced styling for current player's box
        if player == self.current_player:
            # Glowing effect for current player
            for i in range(5):
                glow_rect = pygame.Rect(x - i, y - i, 220 + 2*i, 85 + 2*i)
                glow_color = (*player.color, 50 - i*10)
                glow_surface = pygame.Surface((220 + 2*i, 85 + 2*i))
                glow_surface.set_alpha(50 - i*10)
                glow_surface.fill(player.color)
                self.screen.blit(glow_surface, glow_rect)
            
            pygame.draw.rect(self.screen, player.color, box_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 4)
            text_color = (255, 255, 255)
            secondary_color = (240, 240, 240)
        else:
            pygame.draw.rect(self.screen, (60, 60, 60), box_rect)
            pygame.draw.rect(self.screen, (120, 120, 120), box_rect, 3)
            text_color = (220, 220, 220)
            secondary_color = (180, 180, 180)
        
        # Enhanced player name with shadow
        name_shadow = self.info_font.render(player.name, True, (0, 0, 0))
        name_surface = self.info_font.render(player.name, True, text_color)
        self.screen.blit(name_shadow, (x + 12, y + 12))
        self.screen.blit(name_surface, (x + 10, y + 10))
        
        # Enhanced player position
        pos_text = f"Kotak: {player.position}"
        pos_surface = self.info_font.render(pos_text, True, secondary_color)
        self.screen.blit(pos_surface, (x + 10, y + 35))
        
        # Enhanced player type with icon-like styling
        type_text = "🤖 Computer" if player.is_computer else "👤 Human"
        type_surface = self.small_font.render(type_text, True, secondary_color)
        self.screen.blit(type_surface, (x + 10, y + 60))

    def draw_win_screen(self):
        """Draw victory screen"""
        # Enhanced semi-transparent overlay
        overlay = pygame.Surface((900, 650))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Victory background panel
        win_panel = pygame.Rect(150, 180, 600, 300)
        pygame.draw.rect(self.screen, (40, 40, 40), win_panel)
        pygame.draw.rect(self.screen, self.winner.color, win_panel, 5)
        
        # Add gradient to win panel
        for i in range(win_panel.height):
            alpha = 20 + i // 10
            color = (40 + i//10, 40 + i//10, 40 + i//10)
            pygame.draw.line(self.screen, color, 
                           (win_panel.x, win_panel.y + i), 
                           (win_panel.x + win_panel.width, win_panel.y + i))
        
        # Enhanced victory message
        win_text = f"🎉 {self.winner.name} MENANG! 🎉"
        win_surface = pygame.font.SysFont('Arial', 48, bold=True).render(win_text, True, (255, 215, 0))
        win_shadow = pygame.font.SysFont('Arial', 48, bold=True).render(win_text, True, (0, 0, 0))
        win_rect = win_surface.get_rect(center=(450, 250))
        shadow_rect = win_shadow.get_rect(center=(452, 252))
        self.screen.blit(win_shadow, shadow_rect)
        self.screen.blit(win_surface, win_rect)
        
        # Enhanced final positions
        final_text = f"Posisi Final - {self.player1.name}: {self.player1.position} | {self.player2.name}: {self.player2.position}"
        final_surface = self.main_font.render(final_text, True, (255, 255, 255))
        final_rect = final_surface.get_rect(center=(450, 320))
        self.screen.blit(final_surface, final_rect)
        
        # Enhanced instructions with styling
        restart_text = "⌨️ Tekan R untuk main lagi | Tekan M untuk menu utama"
        restart_surface = self.info_font.render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(450, 380))
        
        # Add background to instructions
        instruction_bg = pygame.Rect(restart_rect.x - 10, restart_rect.y - 5, 
                                   restart_rect.width + 20, restart_rect.height + 10)
        pygame.draw.rect(self.screen, (60, 60, 60), instruction_bg)
        pygame.draw.rect(self.screen, (150, 150, 150), instruction_bg, 2)
        self.screen.blit(restart_surface, restart_rect)

    def draw_back_button(self):
        """Draw back to menu button"""
        button_rect = pygame.Rect(740, 570, 140, 50)
        
        # Enhanced button with gradient
        for i in range(button_rect.height):
            color_val = 100 + i * 2
            color = (color_val, color_val, color_val)
            pygame.draw.line(self.screen, color, 
                           (button_rect.x, button_rect.y + i), 
                           (button_rect.x + button_rect.width, button_rect.y + i))
        
        pygame.draw.rect(self.screen, (150, 150, 150), button_rect, 3)
        
        # Enhanced button text
        button_text = self.info_font.render("🏠 Menu Utama", True, (255, 255, 255))
        button_shadow = self.info_font.render("🏠 Menu Utama", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        shadow_rect = button_shadow.get_rect(center=(button_rect.centerx + 1, button_rect.centery + 1))
        self.screen.blit(button_shadow, shadow_rect)
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
                self.message = f"🪜 {self.current_player.name} naik tangga! {old_position + dice_value} → {self.current_player.position}"
            else:
                self.message = f"🐍 {self.current_player.name} kena ular! {old_position + dice_value} → {self.current_player.position}"
        else:
            self.message = f"✨ {self.current_player.name} pindah ke kotak {self.current_player.position}"
        
        # Check for win condition
        if self.current_player.position >= 100:
            self.current_player.position = 100
            self.game_over = True
            self.winner = self.current_player
            self.message = f"🏆 {self.current_player.name} menang!"
        else:
            # Switch to next player
            self.switch_player()
            
            # Update message for next player
            if self.current_player.is_computer:
                self.message += " | 🤖 Computer sedang berpikir..."
                self.current_player.set_move_time()
            else:
                self.message += " | 🎲 Klik dadu untuk roll"
        
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
            self.message = "🤖 Computer sedang berpikir..."
            self.current_player.set_move_time()
        else:
            self.message = "🎲 Klik dadu untuk roll"

    def run(self):
        """Main game loop"""
        while True:
            result = self.handle_input()
            if result:
                return result
            
            self.update_game()
            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth animation