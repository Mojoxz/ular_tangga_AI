import pygame
import sys
import math

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Fonts
        self.font_title = pygame.font.SysFont('Arial', 56, bold=True)
        self.font_subtitle = pygame.font.SysFont('Arial', 24)
        self.font_button = pygame.font.SysFont('Arial', 28, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 18)
        self.font_instructions = pygame.font.SysFont('Arial', 16)
        
        self.selected_mode = None
        
        # Animation variables
        self.time = 0
        self.logo_bounce = 0
        
        # Layout configuration - better spacing
        button_width = 300
        button_height = 55
        button_spacing = 12
        start_y = 280
        
        # Center buttons more to the right to leave space for instructions
        center_x = self.width // 2 + 100
        
        # Button rectangles
        self.button_1v1 = pygame.Rect(center_x - button_width//2, start_y, button_width, button_height)
        self.button_1vcomputer_easy = pygame.Rect(center_x - button_width//2, start_y + (button_height + button_spacing), button_width, button_height)
        self.button_1vcomputer_medium = pygame.Rect(center_x - button_width//2, start_y + 2*(button_height + button_spacing), button_width, button_height)
        self.button_1vcomputer_hard = pygame.Rect(center_x - button_width//2, start_y + 3*(button_height + button_spacing), button_width, button_height)
        self.button_quit = pygame.Rect(center_x - button_width//2, start_y + 4*(button_height + button_spacing), button_width, button_height)
        
        # Colors
        self.bg_gradient_top = (25, 50, 25)
        self.bg_gradient_bottom = (15, 30, 15)
        self.button_normal = (70, 130, 70)
        self.button_hover = (90, 160, 90)
        self.button_shadow = (40, 80, 40)
        self.text_title = (255, 215, 0)
        self.text_subtitle = (200, 255, 200)
        self.text_button = (255, 255, 255)
        self.text_instruction = (180, 180, 180)
        self.instruction_bg = (30, 30, 30, 200)

    def draw_gradient_background(self):
        """Draw a gradient background"""
        for y in range(self.height):
            ratio = y / self.height
            r = int(self.bg_gradient_top[0] * (1 - ratio) + self.bg_gradient_bottom[0] * ratio)
            g = int(self.bg_gradient_top[1] * (1 - ratio) + self.bg_gradient_bottom[1] * ratio)
            b = int(self.bg_gradient_top[2] * (1 - ratio) + self.bg_gradient_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))

    def draw_decorative_elements(self):
        """Draw decorative snake and ladder elements - adjusted for left side"""
        # Move decorations to not interfere with instructions
        snake_color = (100, 200, 100)
        
        # Right side snake decoration (moved further right)
        for i in range(5):
            x = self.width - 80 - i * 15
            y = 200 + math.sin(self.time * 0.05 + i * 0.5) * 10
            pygame.draw.circle(self.screen, snake_color, (int(x), int(y)), 8)
            if i > 0:
                prev_x = self.width - 80 - (i-1) * 15
                prev_y = 200 + math.sin(self.time * 0.05 + (i-1) * 0.5) * 10
                pygame.draw.line(self.screen, snake_color, (int(prev_x), int(prev_y)), (int(x), int(y)), 6)
        
        # Draw ladder decorations on the right side only
        ladder_color = (160, 120, 80)
        
        # Right ladder (moved further right)
        ladder_x = self.width - 120
        ladder_y = 450
        pygame.draw.line(self.screen, ladder_color, (ladder_x, ladder_y), (ladder_x, ladder_y + 80), 6)
        pygame.draw.line(self.screen, ladder_color, (ladder_x + 30, ladder_y), (ladder_x + 30, ladder_y + 80), 6)
        for i in range(4):
            rung_y = ladder_y + 15 + i * 18
            pygame.draw.line(self.screen, ladder_color, (ladder_x, rung_y), (ladder_x + 30, rung_y), 4)

    def draw_title_section(self):
        """Draw the title and subtitle with animation"""
        # Animated title with bounce effect
        title_y = 100 + self.logo_bounce
        
        # Draw title shadow first
        title_shadow = self.font_title.render("ULAR TANGGA", True, (100, 100, 0))
        title_shadow_rect = title_shadow.get_rect(center=(self.width//2 + 3, title_y + 3))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        # Draw main title
        title_text = self.font_title.render("ULAR TANGGA", True, self.text_title)
        title_rect = title_text.get_rect(center=(self.width//2, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_subtitle.render("Game Klasik Indonesia", True, self.text_subtitle)
        subtitle_rect = subtitle_text.get_rect(center=(self.width//2, title_y + 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw version info
        version_text = self.font_small.render("Versi 2.0 - Pygame Edition", True, self.text_instruction)
        version_rect = version_text.get_rect(center=(self.width//2, title_y + 75))
        self.screen.blit(version_text, version_rect)

    def draw_button(self, button_rect, text, mouse_pos, icon=""):
        """Draw a modern styled button with shadow and hover effects"""
        # Check if button is hovered
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Button shadow
        shadow_rect = button_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.screen, self.button_shadow, shadow_rect, border_radius=12)
        
        # Button background
        button_color = self.button_hover if is_hovered else self.button_normal
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=12)
        
        # Button border
        border_color = (255, 255, 255) if is_hovered else (150, 150, 150)
        border_width = 3 if is_hovered else 2
        pygame.draw.rect(self.screen, border_color, button_rect, border_width, border_radius=12)
        
        # Button text with icon
        full_text = f"{icon} {text}" if icon else text
        text_surface = self.font_button.render(full_text, True, self.text_button)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Hover glow effect
        if is_hovered:
            glow_surface = pygame.Surface((button_rect.width + 10, button_rect.height + 10))
            glow_surface.set_alpha(50)
            glow_surface.fill((255, 255, 255))
            glow_rect = glow_surface.get_rect(center=button_rect.center)
            self.screen.blit(glow_surface, glow_rect)

    def draw_instructions_left_side(self):
        """Draw enhanced game instructions on the left side"""
        instructions = [
            "🎮 Pilih mode permainan untuk memulai",
            "",
            "🤖 AI Mudah:",
            "   Bermain santai, kadang membuat kesalahan",
            "",
            "🤖 AI Sedang:",
            "   Seimbang antara strategi dan risiko",
            "",
            "🤖 AI Sulit:",
            "   Sangat strategis dan sulit dikalahkan",
            "",
            "🎲 Cara Bermain:",
            "   • Klik dadu untuk melempar",
            "   • 🐍 Hati-hati ular!",
            "   • 🪜 Manfaatkan tangga!",
            "",
            "⌨️ Shortcut Keyboard:",
            "   • 1 = Player vs Player",
            "   • 2 = vs AI Mudah",
            "   • 3 = vs AI Sedang", 
            "   • 4 = vs AI Sulit"
        ]
        
        # Background panel for instructions
        panel_x = 30
        panel_y = 250
        panel_width = 350
        panel_height = 400
        
        # Create semi-transparent background
        instruction_surface = pygame.Surface((panel_width, panel_height))
        instruction_surface.set_alpha(180)
        instruction_surface.fill((20, 20, 20))
        self.screen.blit(instruction_surface, (panel_x, panel_y))
        
        # Draw border
        pygame.draw.rect(self.screen, (100, 150, 100), (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)
        
        # Draw title for instructions panel
        title_font = pygame.font.SysFont('Arial', 20, bold=True)
        title_text = title_font.render("📋 PANDUAN PERMAINAN", True, (255, 215, 0))
        self.screen.blit(title_text, (panel_x + 15, panel_y + 15))
        
        # Draw instructions
        start_y = panel_y + 50
        line_height = 18
        
        for i, instruction in enumerate(instructions):
            if instruction == "":  # Empty line for spacing
                continue
                
            # Determine font and color based on content
            if instruction.startswith("🤖") or instruction.startswith("🎮") or instruction.startswith("🎲") or instruction.startswith("⌨️"):
                font = pygame.font.SysFont('Arial', 16, bold=True)
                color = (255, 255, 150)  # Yellow for headers
            elif instruction.startswith("   "):  # Indented text
                font = pygame.font.SysFont('Arial', 14)
                color = (200, 200, 200)  # Light gray for sub-items
                instruction = instruction[3:]  # Remove indentation
            else:
                font = pygame.font.SysFont('Arial', 15)
                color = self.text_instruction
            
            text_surface = font.render(instruction, True, color)
            text_y = start_y + i * line_height
            
            # Adjust X position for indented items
            text_x = panel_x + 15
            if instruction.startswith("•"):
                text_x += 20
            
            self.screen.blit(text_surface, (text_x, text_y))

    def draw_footer(self):
        """Draw footer information"""
        footer_text = "Dibuat dengan ❤️ menggunakan Pygame | © 2024"
        footer_surface = pygame.font.SysFont('Arial', 14).render(footer_text, True, (120, 120, 120))
        footer_rect = footer_surface.get_rect(center=(self.width//2, self.height - 20))
        self.screen.blit(footer_surface, footer_rect)

    def update_animations(self):
        """Update animation variables"""
        self.time += 1
        
        # Logo bounce animation
        self.logo_bounce = math.sin(self.time * 0.03) * 5

    def draw(self):
        """Main draw method with improved layout"""
        # Update animations
        self.update_animations()
        
        # Draw background
        self.draw_gradient_background()
        
        # Draw decorative elements
        self.draw_decorative_elements()
        
        # Draw title section
        self.draw_title_section()
        
        # Draw instructions on the left side
        self.draw_instructions_left_side()
        
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons (now positioned more to the right)
        self.draw_button(self.button_1v1, "Pemain vs Pemain", mouse_pos, "👥")
        self.draw_button(self.button_1vcomputer_easy, "vs Komputer (Mudah)", mouse_pos, "🤖😊")
        self.draw_button(self.button_1vcomputer_medium, "vs Komputer (Sedang)", mouse_pos, "🤖😐")
        self.draw_button(self.button_1vcomputer_hard, "vs Komputer (Sulit)", mouse_pos, "🤖😤")
        self.draw_button(self.button_quit, "Keluar", mouse_pos, "🚪")
        
        # Draw footer
        self.draw_footer()
        
        pygame.display.flip()

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Keyboard shortcuts
                key_to_mode = {
                    pygame.K_1: "1v1",
                    pygame.K_2: "1vcomputer_easy",
                    pygame.K_3: "1vcomputer_medium",
                    pygame.K_4: "1vcomputer_hard",
                }
                if event.key in key_to_mode:
                    self.selected_mode = key_to_mode[event.key]
                    return True
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check each button individually
                    if self.button_1v1.collidepoint(mouse_pos):
                        self.selected_mode = "1v1"
                        return True
                    elif self.button_1vcomputer_easy.collidepoint(mouse_pos):
                        self.selected_mode = "1vcomputer_easy"
                        return True
                    elif self.button_1vcomputer_medium.collidepoint(mouse_pos):
                        self.selected_mode = "1vcomputer_medium"
                        return True
                    elif self.button_1vcomputer_hard.collidepoint(mouse_pos):
                        self.selected_mode = "1vcomputer_hard"
                        return True
                    elif self.button_quit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
        return False

    def run(self):
        """Main menu loop"""
        while True:
            if self.handle_events():
                return self.selected_mode
            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth animations