import pygame
import sys
from menu import Menu
from game import Game

# Initialize Pygame
pygame.init()

# Game configuration
WIDTH, HEIGHT = 900, 650

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Tangga 1v1")

def main():
    try:
        while True:
            # Show menu and get selected mode
            menu = Menu(screen)
            selected_mode = menu.run()
            
            if selected_mode:
                # Start game with selected mode
                game = Game(screen, selected_mode)  # Pass both screen and game_mode
                result = game.run()
                
                if result == "quit":
                    break
                # If result is "menu", continue to show menu again
            else:
                break
                
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()