import pygame
import sys
from game import Game

# Initialize Pygame
pygame.init()

# Game configuration
WIDTH, HEIGHT = 900, 650
FPS = 30

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Tangga 1v1")

# Game Loop
def main():
    try:
        game = Game(screen)
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()