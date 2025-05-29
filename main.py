import pygame
import random
from player import Player
from board import Board
from game import Game

# Initialize Pygame
pygame.init()

# Game configuration
WIDTH, HEIGHT = 800, 600
FPS = 30

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Tangga 1v1")

# Game Loop
def main():
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()
