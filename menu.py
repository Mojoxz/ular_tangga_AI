import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 32, bold=True)
        self.selected_mode = None
        
        # Button rectangles
        self.button_1v1 = pygame.Rect(300, 250, 300, 60)
        self.button_1vcomputer = pygame.Rect(300, 330, 300, 60)
        self.button_quit = pygame.Rect(300, 410, 300, 60)
        
        # Colors
        self.bg_color = (20, 80, 20)
        self.button_color = (100, 150, 100)
        self.button_hover_color = (150, 200, 150)
        self.text_color = (255, 255, 255)

    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.font_title.render("ULAR TANGGA", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(450, 150))
        self.screen.blit(title_text, title_rect)
        
        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons
        self.draw_button(self.button_1v1, "1 vs 1", mouse_pos)
        self.draw_button(self.button_1vcomputer, "1 vs Computer", mouse_pos)
        self.draw_button(self.button_quit, "Quit", mouse_pos)
        
        # Instructions
        instruction_text = pygame.font.SysFont('Arial', 18).render(
            "Klik untuk memilih mode permainan", True, (200, 200, 200)
        )
        instruction_rect = instruction_text.get_rect(center=(450, 500))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

    def draw_button(self, button_rect, text, mouse_pos):
        # Change color on hover
        if button_rect.collidepoint(mouse_pos):
            color = self.button_hover_color
        else:
            color = self.button_color
        
        # Draw button
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)
        
        # Draw text
        text_surface = self.font_button.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_1v1.collidepoint(mouse_pos):
                        self.selected_mode = "1v1"
                        return True
                    elif self.button_1vcomputer.collidepoint(mouse_pos):
                        self.selected_mode = "1vcomputer"
                        return True
                    elif self.button_quit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        return False

    def run(self):
        while True:
            if self.handle_events():
                return self.selected_mode
            self.draw()
            self.clock.tick(60)