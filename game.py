import pygame
import random
from player import Player
from board import Board
from utils import roll_dice

# Game Logic
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.player1 = Player("Player 1", (255, 0, 0))  # Red
        self.player2 = Player("Player 2", (0, 0, 255))  # Blue
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.waiting_for_roll = True
        self.dice_value = 0
        self.font = pygame.font.SysFont('Arial', 24)
        self.message = "Press SPACE to roll dice"

    def draw(self):
        # Fill background with dark green
        self.screen.fill((0, 100, 0))
        
        # Draw board
        self.board.draw(self.screen)
        
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        # Draw game info
        self.draw_game_info()
        
        pygame.display.flip()

    def draw_game_info(self):
        """Draw current player, dice value, and messages"""
        # Current player info
        current_text = f"Current Player: {self.current_player.name}"
        text_surface = self.font.render(current_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 10))
        
        # Player positions
        pos1_text = f"{self.player1.name}: Square {self.player1.position}"
        pos1_surface = self.font.render(pos1_text, True, (255, 255, 255))
        self.screen.blit(pos1_surface, (300, 10))
        
        pos2_text = f"{self.player2.name}: Square {self.player2.position}"
        pos2_surface = self.font.render(pos2_text, True, (255, 255, 255))
        self.screen.blit(pos2_surface, (500, 10))
        
        # Dice value
        if self.dice_value > 0:
            dice_text = f"Dice: {self.dice_value}"
            dice_surface = self.font.render(dice_text, True, (255, 255, 0))
            self.screen.blit(dice_surface, (50, 580))
        
        # Message
        message_surface = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(message_surface, (200, 580))
        
        # Game over message
        if self.game_over and self.winner:
            win_text = f"{self.winner.name} WINS!"
            win_surface = pygame.font.SysFont('Arial', 48).render(win_text, True, (255, 255, 0))
            win_rect = win_surface.get_rect(center=(400, 300))
            pygame.draw.rect(self.screen, (0, 0, 0), win_rect.inflate(20, 20))
            self.screen.blit(win_surface, win_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.waiting_for_roll and not self.game_over:
                    self.roll_and_move()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()

    def roll_and_move(self):
        """Roll dice and move current player"""
        self.dice_value = roll_dice()
        self.message = f"{self.current_player.name} rolled {self.dice_value}"
        
        # Move player
        old_position = self.current_player.position
        self.current_player.move(self.dice_value, self.board)
        
        # Check for win condition
        if self.current_player.position >= 100:
            self.current_player.position = 100
            self.game_over = True
            self.winner = self.current_player
            self.message = f"{self.current_player.name} wins! Press R to restart"
        else:
            # Switch to next player
            self.switch_player()
            self.message = f"Press SPACE to roll dice ({self.current_player.name}'s turn)"

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
        self.dice_value = 0
        self.message = "Press SPACE to roll dice"

    def run(self):
        """Main game loop"""
        while not self.game_over:
            self.handle_input()
            self.draw()
            self.clock.tick(30)  # 30 FPS
        
        # Game over screen loop
        while self.game_over:
            self.handle_input()
            self.draw()
            self.clock.tick(30)