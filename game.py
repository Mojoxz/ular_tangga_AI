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
        from player import Player, EnhancedAIPlayer
        
        self.board = Board()
        self.game_mode = game_mode
        
        # Initialize players based on mode
        if game_mode == "1v1":
            self.player1 = Player("Player 1", (255, 0, 0))  # Red
            self.player2 = Player("Player 2", (0, 0, 255))  # Blue
        elif game_mode == "1vcomputer_easy":
            self.player1 = Player("Player", (255, 0, 0))  # Red
            self.player2 = EnhancedAIPlayer("AI (Mudah)", (0, 0, 255), difficulty="easy")  # Blue
        elif game_mode == "1vcomputer_medium":
            self.player1 = Player("Player", (255, 0, 0))  # Red
            self.player2 = EnhancedAIPlayer("AI (Sedang)", (0, 0, 255), difficulty="medium")  # Blue
        elif game_mode == "1vcomputer_hard":
            self.player1 = Player("Player", (255, 0, 0))  # Red
            self.player2 = EnhancedAIPlayer("AI (Sulit)", (0, 0, 255), difficulty="hard")  # Blue
        else:  # fallback to basic computer
            self.player1 = Player("Player", (255, 0, 0))  # Red
            self.player2 = Player("Computer", (0, 0, 255), is_computer=True)  # Blue
        
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.waiting_for_roll = True
        
        # Initialize dice - positioned in the right panel
        self.dice = Dice(850, 200)
        
        self.font = pygame.font.SysFont('Arial', 24)
        
        # AI decision info for display
        self.ai_decision_info = {}
        
        # Set initial message based on player type
        if self.current_player.is_computer:
            self.message = "Computer sedang berpikir..."
            self.current_player.set_move_time()
            if hasattr(self.current_player, 'get_ai_decision_info'):
                self.ai_decision_info = self.current_player.get_ai_decision_info(
                    self.board, self.get_opponent().position)
        else:
            self.message = "Klik dadu untuk roll"
        
        # Animation variables
        self.moving_animation = False
        self.animation_start_pos = 1
        self.animation_target_pos = 1
        self.animation_progress = 0

    def get_opponent(self):
        """Get the opponent of current player"""
        return self.player2 if self.current_player == self.player1 else self.player1

    def get_difficulty_display(self):
        """Get difficulty display string"""
        if self.game_mode == "1v1":
            return "Pemain vs Pemain"
        elif "easy" in self.game_mode:
            return "vs AI Mudah 🤖😊"
        elif "medium" in self.game_mode:
            return "vs AI Sedang 🤖😐"
        elif "hard" in self.game_mode:
            return "vs AI Sulit 🤖😤"
        else:
            return "vs Computer"

    def draw(self):
        # Fill background with gradient - darker green to lighter
        for y in range(700):
            color_value = int(50 + (y / 700) * 30)  # Gradient from dark to lighter green
            pygame.draw.line(self.screen, (0, color_value, 0), (0, y), (1200, y))
        
        # Draw board with proper positioning
        self.board.draw(self.screen)
        
        # Draw players on the board using proper board coordinates
        self.draw_players_on_board()
        
        # Draw dice
        mouse_pos = pygame.mouse.get_pos()
        self.dice.draw(self.screen, mouse_pos)
        
        # Draw game info in the expanded right panel
        self.draw_game_info()
        
        # Draw AI info if applicable
        if hasattr(self.current_player, 'get_ai_decision_info'):
            self.draw_ai_info()
        
        # Draw back to menu button
        self.draw_back_button()
        
        pygame.display.flip()

    def draw_players_on_board(self):
        """Draw players on their actual board positions"""
        # Get board coordinates for each player
        p1_coords = self.board.get_position_coordinates(self.player1.position)
        p2_coords = self.board.get_position_coordinates(self.player2.position)
        
        # Draw player 1
        if p1_coords:
            # Draw player circle with border
            pygame.draw.circle(self.screen, self.player1.color, p1_coords, 18)
            pygame.draw.circle(self.screen, (255, 255, 255), p1_coords, 18, 3)
            
            # Draw player number/initial
            font = pygame.font.SysFont('Arial', 16, bold=True)
            text = font.render("1", True, (255, 255, 255))
            text_rect = text.get_rect(center=p1_coords)
            self.screen.blit(text, text_rect)
        
        # Draw player 2 (offset slightly if on same position)
        if p2_coords:
            # If both players are on same position, offset player 2
            if self.player1.position == self.player2.position:
                p2_coords = (p2_coords[0] + 25, p2_coords[1])
            
            # Draw player circle with border
            pygame.draw.circle(self.screen, self.player2.color, p2_coords, 18)
            pygame.draw.circle(self.screen, (255, 255, 255), p2_coords, 18, 3)
            
            # Draw player number/initial
            font = pygame.font.SysFont('Arial', 16, bold=True)
            text = font.render("2", True, (255, 255, 255))
            text_rect = text.get_rect(center=p2_coords)
            self.screen.blit(text, text_rect)

    def draw_game_info(self):
        """Draw current player, dice value, and messages in expanded right panel"""
        # Right panel background
        panel_rect = pygame.Rect(720, 0, 480, 700)
        pygame.draw.rect(self.screen, (20, 40, 20), panel_rect)
        pygame.draw.rect(self.screen, (100, 150, 100), panel_rect, 3)
        
        # Title
        title_text = "ULAR TANGGA"
        title_surface = pygame.font.SysFont('Arial', 32, bold=True).render(title_text, True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(960, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Game mode
        mode_text = self.get_difficulty_display()
        mode_surface = pygame.font.SysFont('Arial', 18).render(mode_text, True, (255, 255, 255))
        mode_rect = mode_surface.get_rect(center=(960, 65))
        self.screen.blit(mode_surface, mode_rect)
        
        # Current player info
        current_text = f"Giliran: {self.current_player.name}"
        text_surface = pygame.font.SysFont('Arial', 24, bold=True).render(current_text, True, self.current_player.color)
        self.screen.blit(text_surface, (740, 90))
        
        # Player info boxes - now with more space
        self.draw_player_info_box(self.player1, 740, 120)
        self.draw_player_info_box(self.player2, 740, 220)
        
        # Dice value display
        if self.dice.value > 0:
            dice_text = f"Nilai Dadu: {self.dice.value}"
            dice_surface = pygame.font.SysFont('Arial', 20, bold=True).render(dice_text, True, (255, 255, 0))
            self.screen.blit(dice_surface, (740, 320))
        
        # Game progress bar
        self.draw_game_progress()
        
        # Message area with better styling
        message_rect = pygame.Rect(740, 500, 440, 60)
        pygame.draw.rect(self.screen, (40, 40, 40), message_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), message_rect, 2)
        
        # Message text with word wrapping
        self.draw_wrapped_text(self.message, message_rect, pygame.font.SysFont('Arial', 16), (255, 255, 255))
        
        # Game over message
        if self.game_over and self.winner:
            self.draw_win_screen()

    def draw_wrapped_text(self, text, rect, font, color):
        """Draw text with word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= rect.width - 20:  # 10px margin on each side
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        y_offset = rect.y + 10
        for line in lines:
            if y_offset + font.get_height() <= rect.bottom - 10:
                line_surface = font.render(line, True, color)
                self.screen.blit(line_surface, (rect.x + 10, y_offset))
                y_offset += font.get_height() + 5

    def draw_game_progress(self):
        """Draw game progress visualization"""
        progress_y = 350
        
        # Progress title
        progress_title = "Progress Permainan"
        title_surface = pygame.font.SysFont('Arial', 18, bold=True).render(progress_title, True, (255, 255, 255))
        self.screen.blit(title_surface, (740, progress_y))
        
        # Player 1 progress
        p1_progress = self.player1.position / 100
        p1_rect = pygame.Rect(740, progress_y + 30, 400, 25)
        pygame.draw.rect(self.screen, (100, 100, 100), p1_rect)
        p1_fill_rect = pygame.Rect(740, progress_y + 30, int(400 * p1_progress), 25)
        pygame.draw.rect(self.screen, self.player1.color, p1_fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), p1_rect, 2)
        
        # Player 1 label
        p1_label = f"{self.player1.name}: {self.player1.position}/100"
        p1_surface = pygame.font.SysFont('Arial', 14).render(p1_label, True, (255, 255, 255))
        self.screen.blit(p1_surface, (745, progress_y + 33))
        
        # Player 2 progress
        p2_progress = self.player2.position / 100
        p2_rect = pygame.Rect(740, progress_y + 65, 400, 25)
        pygame.draw.rect(self.screen, (100, 100, 100), p2_rect)
        p2_fill_rect = pygame.Rect(740, progress_y + 65, int(400 * p2_progress), 25)
        pygame.draw.rect(self.screen, self.player2.color, p2_fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), p2_rect, 2)
        
        # Player 2 label
        p2_label = f"{self.player2.name}: {self.player2.position}/100"
        p2_surface = pygame.font.SysFont('Arial', 14).render(p2_label, True, (255, 255, 255))
        self.screen.blit(p2_surface, (745, progress_y + 68))

    def draw_player_info_box(self, player, x, y):
        """Draw enhanced player info box"""
        box_rect = pygame.Rect(x, y, 440, 85)
        
        # Highlight current player's box
        if player == self.current_player:
            pygame.draw.rect(self.screen, (*player.color[:3], 100), box_rect)  # Semi-transparent
            pygame.draw.rect(self.screen, player.color, box_rect, 4)
            text_color = (255, 255, 255)
        else:
            pygame.draw.rect(self.screen, (60, 60, 60), box_rect)
            pygame.draw.rect(self.screen, (150, 150, 150), box_rect, 2)
            text_color = (200, 200, 200)
        
        # Player name and type
        name_surface = pygame.font.SysFont('Arial', 20, bold=True).render(player.name, True, text_color)
        self.screen.blit(name_surface, (x + 10, y + 10))
        
        # Player type
        if player.is_computer:
            if hasattr(player, 'difficulty'):
                type_text = f"AI - {player.difficulty.capitalize()}"
            else:
                type_text = "Computer"
        else:
            type_text = "Human Player"
        
        type_surface = pygame.font.SysFont('Arial', 14).render(type_text, True, text_color)
        self.screen.blit(type_surface, (x + 10, y + 35))
        
        # Position info
        pos_text = f"Posisi: Kotak {player.position}"
        pos_surface = pygame.font.SysFont('Arial', 16, bold=True).render(pos_text, True, text_color)
        self.screen.blit(pos_surface, (x + 10, y + 55))
        
        # Player color indicator
        color_rect = pygame.Rect(x + 400, y + 15, 30, 30)
        pygame.draw.rect(self.screen, player.color, color_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 2)

    def draw_ai_info(self):
        """Draw AI decision making information"""
        if not self.ai_decision_info or not self.current_player.is_computer:
            return
            
        # AI Info Box
        info_rect = pygame.Rect(740, 580, 440, 100)
        pygame.draw.rect(self.screen, (30, 30, 50), info_rect)
        pygame.draw.rect(self.screen, (100, 150, 255), info_rect, 2)
        
        # Title
        title_surface = pygame.font.SysFont('Arial', 16, bold=True).render("AI Decision Making", True, (255, 255, 255))
        self.screen.blit(title_surface, (750, 590))
        
        # AI info in two columns
        y_offset = 610
        font_small = pygame.font.SysFont('Arial', 12)
        
        # Left column
        left_info = [
            f"Strategi: {self.ai_decision_info.get('strategy', 'Unknown')}",
            f"Status: {self.ai_decision_info.get('status', 'Thinking')}"
        ]
        
        # Right column
        right_info = [
            f"Tangga dekat: {self.ai_decision_info.get('ladders_nearby', 0)}",
            f"Ular dekat: {self.ai_decision_info.get('snakes_nearby', 0)}"
        ]
        
        for i, line in enumerate(left_info):
            line_surface = font_small.render(line, True, (220, 220, 220))
            self.screen.blit(line_surface, (750, y_offset + i * 16))
        
        for i, line in enumerate(right_info):
            line_surface = font_small.render(line, True, (220, 220, 220))
            self.screen.blit(line_surface, (950, y_offset + i * 16))
        
        # Thinking animation
        if self.current_player.is_computer and self.waiting_for_roll:
            thinking_dots = "." * ((pygame.time.get_ticks() // 300) % 4)
            thinking_text = f"Berpikir{thinking_dots}"
            thinking_surface = font_small.render(thinking_text, True, (100, 255, 100))
            self.screen.blit(thinking_surface, (750, y_offset + 35))

    def draw_win_screen(self):
        """Draw victory screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((1200, 700))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Victory message
        win_text = f"{self.winner.name} MENANG!"
        win_surface = pygame.font.SysFont('Arial', 60, bold=True).render(win_text, True, (255, 255, 0))
        win_rect = win_surface.get_rect(center=(600, 250))
        self.screen.blit(win_surface, win_rect)
        
        # Game mode info
        mode_text = f"Mode: {self.get_difficulty_display()}"
        mode_surface = pygame.font.SysFont('Arial', 24).render(mode_text, True, (200, 200, 200))
        mode_rect = mode_surface.get_rect(center=(600, 300))
        self.screen.blit(mode_surface, mode_rect)
        
        # Final positions
        final_text = f"Posisi Final - {self.player1.name}: {self.player1.position}, {self.player2.name}: {self.player2.position}"
        final_surface = pygame.font.SysFont('Arial', 20).render(final_text, True, (255, 255, 255))
        final_rect = final_surface.get_rect(center=(600, 340))
        self.screen.blit(final_surface, final_rect)
        
        # Performance stats for AI games
        if self.player2.is_computer and hasattr(self.player2, 'difficulty'):
            perf_text = f"Melawan AI {self.player2.difficulty.capitalize()}"
            perf_surface = pygame.font.SysFont('Arial', 18).render(perf_text, True, (180, 180, 180))
            perf_rect = perf_surface.get_rect(center=(600, 370))
            self.screen.blit(perf_surface, perf_rect)
        
        # Instructions
        restart_text = "Tekan R untuk main lagi | Tekan M untuk menu utama"
        restart_surface = pygame.font.SysFont('Arial', 20).render(restart_text, True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(600, 420))
        self.screen.blit(restart_surface, restart_rect)

    def draw_back_button(self):
        """Draw back to menu button"""
        button_rect = pygame.Rect(1050, 20, 120, 35)
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover effect
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), button_rect)
        else:
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
        
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        button_text = pygame.font.SysFont('Arial', 16).render("Menu Utama", True, (255, 255, 255))
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
        
        # Handle computer player with enhanced AI
        if (self.current_player.is_computer and 
            self.waiting_for_roll and 
            not self.game_over):
            
            # Check if it's enhanced AI
            if hasattr(self.current_player, 'should_computer_roll_enhanced'):
                opponent = self.get_opponent()
                if self.current_player.should_computer_roll_enhanced(self.board, opponent.position):
                    self.roll_and_move()
                # Update AI decision info
                if hasattr(self.current_player, 'get_ai_decision_info'):
                    self.ai_decision_info = self.current_player.get_ai_decision_info(
                        self.board, opponent.position)
            else:
                # Basic computer AI
                if self.current_player.should_computer_roll():
                    self.roll_and_move()

    def move_player(self, dice_value):
        """Move player and handle game logic"""
        old_position = self.current_player.position
        self.current_player.move(dice_value, self.board)
        
        # Calculate where player would land without snakes/ladders
        intended_position = min(old_position + dice_value, 100)
        
        # Update message based on movement
        if self.current_player.position != intended_position:
            # Landed on snake or ladder
            if self.current_player.position > intended_position:
                self.message = f"{self.current_player.name} naik tangga! {intended_position} → {self.current_player.position}"
            else:
                self.message = f"{self.current_player.name} kena ular! {intended_position} → {self.current_player.position}"
        else:
            self.message = f"{self.current_player.name} pindah ke kotak {self.current_player.position}"
        
        # AI commentary for enhanced AI
        if (self.current_player.is_computer and 
            hasattr(self.current_player, 'difficulty') and 
            self.current_player.position != intended_position):
            
            if self.current_player.position > intended_position:
                # AI got a ladder
                comments = {
                    "easy": " | Wah beruntung!",
                    "medium": " | Perhitungan yang tepat",
                    "hard": " | Sesuai strategi!"
                }
            else:
                # AI hit a snake
                comments = {
                    "easy": " | Waduh...",
                    "medium": " | Tidak apa-apa",
                    "hard": " | Risiko yang diperhitungkan"
                }
            
            comment = comments.get(self.current_player.difficulty, "")
            self.message += comment
        
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
                # Update AI decision info for new turn
                if hasattr(self.current_player, 'get_ai_decision_info'):
                    opponent = self.get_opponent()
                    self.ai_decision_info = self.current_player.get_ai_decision_info(
                        self.board, opponent.position)
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
        self.ai_decision_info = {}
        
        if self.current_player.is_computer:
            self.message = "Computer sedang berpikir..."
            self.current_player.set_move_time()
            if hasattr(self.current_player, 'get_ai_decision_info'):
                opponent = self.get_opponent()
                self.ai_decision_info = self.current_player.get_ai_decision_info(
                    self.board, opponent.position)
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