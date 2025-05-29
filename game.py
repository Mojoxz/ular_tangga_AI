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
        self.player1 = Player("Player 1", (255, 0, 0))
        self.player2 = Player("Player 2", (0, 0, 255))
        self.current_player = self.player1
        self.game_over = False

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill background
        self.board.draw(self.screen)
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def run(self):
        while not self.game_over:
            self.handle_input()
            self.draw()

            if not self.game_over:
                roll = roll_dice()  # Roll dice
                self.current_player.move(roll)
                if self.current_player.position == 100:
                    self.game_over = True
                    print(f"{self.current_player.name} wins!")
                else:
                    self.switch_player()

            self.clock.tick(fps)
