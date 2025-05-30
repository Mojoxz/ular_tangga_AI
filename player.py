import pygame
import time
import random

# Player Class (Original)
class Player:
    def __init__(self, name, color, is_computer=False):
        self.name = name
        self.color = color
        self.position = 1  # Start at square 1, not 0
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.font = pygame.font.SysFont('Arial', 16)
        self.is_computer = is_computer
        
        # Computer AI variables
        if self.is_computer:
            self.move_start_time = None
            self.move_delay = 1.5  # Delay in seconds before computer moves

    def move(self, steps, board):
        """Move player and handle snakes and ladders"""
        new_position = self.position + steps
        if new_position > 100:
            new_position = 100  # Limit to 100
        
        self.position = new_position
        
        # Check if landed on snake or ladder
        if self.position in board.squares:
            old_pos = self.position
            self.position = board.squares[self.position]
            if self.position > old_pos:
                print(f"{self.name} climbed a ladder from {old_pos} to {self.position}!")
            else:
                print(f"{self.name} slid down a snake from {old_pos} to {self.position}!")

    def get_screen_position(self):
        """Convert board position to screen coordinates"""
        if self.position < 1:
            return (50, 590)
        
        # Adjust for 1-based indexing
        pos = self.position - 1
        row = pos // 10
        col = pos % 10
        
        # Handle zigzag pattern of snake and ladder board
        if row % 2 == 1:  # Odd rows go right to left
            col = 9 - col
        
        x = col * 80 + 50 + 25  # Center in square
        y = (9 - row) * 60 + 50 + 15  # Center in square, flip Y
        
        return (x, y)

    def draw(self, screen):
        """Draw player on the board"""
        x, y = self.get_screen_position()
        
        # Draw player circle
        pygame.draw.circle(screen, self.color, (x, y), 15)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 15, 2)  # Black border
        
        # Draw player name
        text = self.font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x, y - 25))
        screen.blit(text, text_rect)

    # Computer AI methods
    def set_move_time(self):
        """Set the time when computer should make a move"""
        if self.is_computer:
            self.move_start_time = time.time()

    def should_computer_roll(self):
        """Check if computer should roll the dice"""
        if not self.is_computer or self.move_start_time is None:
            return False
        
        current_time = time.time()
        return (current_time - self.move_start_time) >= self.move_delay


# TAMBAHKAN ENHANCED AI PLAYER DI SINI
class EnhancedAIPlayer(Player):
    """Enhanced AI Player dengan strategi yang lebih pintar"""
    
    def __init__(self, name, color, difficulty="medium"):
        super().__init__(name, color, is_computer=True)
        self.difficulty = difficulty
        self.strategy_weights = self.get_strategy_weights()
        self.move_delay = self.get_move_delay()  # Override delay based on difficulty
    
    def get_move_delay(self):
        """Get move delay based on difficulty"""
        delays = {
            "easy": 1.0,    # Fast moves
            "medium": 1.5,  # Normal speed
            "hard": 2.0     # Slower, more "thoughtful"
        }
        return delays.get(self.difficulty, 1.5)
    
    def get_strategy_weights(self):
        """Define strategy weights based on difficulty level"""
        if self.difficulty == "easy":
            return {
                'aggressive': 0.3,
                'cautious': 0.5,
                'random': 0.2
            }
        elif self.difficulty == "hard":
            return {
                'aggressive': 0.7,
                'cautious': 0.3,
                'random': 0.0
            }
        else:  # medium
            return {
                'aggressive': 0.5,
                'cautious': 0.4,
                'random': 0.1
            }
    
    def analyze_board_position(self, board, opponent_position):
        """Analyze board position to determine strategy"""
        analysis = {
            'nearby_ladders': [],
            'nearby_snakes': [],
            'distance_to_opponent': abs(self.position - opponent_position),
            'progress_percentage': self.position / 100,
            'opponent_ahead': opponent_position > self.position
        }
        
        # Find ladders and snakes within reach (1-6 steps)
        for steps in range(1, 7):
            target_pos = self.position + steps
            if target_pos <= 100 and target_pos in board.squares:
                if board.squares[target_pos] > target_pos:
                    analysis['nearby_ladders'].append({
                        'steps': steps,
                        'from': target_pos,
                        'to': board.squares[target_pos],
                        'gain': board.squares[target_pos] - target_pos
                    })
                else:
                    analysis['nearby_snakes'].append({
                        'steps': steps,
                        'from': target_pos,
                        'to': board.squares[target_pos],
                        'loss': target_pos - board.squares[target_pos]
                    })
        
        return analysis
    
    def calculate_move_desirability(self, steps, board, opponent_position):
        """Calculate how desirable a move is"""
        target_pos = min(self.position + steps, 100)
        score = 0
        
        # Base score: closer to 100 is better
        progress_score = (target_pos - self.position) * 10
        score += progress_score
        
        # Bonus for landing on ladder
        if target_pos in board.squares and board.squares[target_pos] > target_pos:
            ladder_bonus = (board.squares[target_pos] - target_pos) * 15
            score += ladder_bonus
        
        # Penalty for landing on snake
        if target_pos in board.squares and board.squares[target_pos] < target_pos:
            snake_penalty = (target_pos - board.squares[target_pos]) * -20
            score += snake_penalty
        
        # Strategy based on opponent position
        if target_pos > opponent_position:
            score += 8  # Bonus for being ahead
        elif target_pos == opponent_position:
            score += 5  # Small bonus for tying
        
        # End game strategy - be more aggressive near finish
        if self.position > 80:
            if target_pos == 100:
                score += 50  # Big bonus for winning
            elif target_pos > 95:
                score += 20  # Bonus for getting very close
        
        return score
    
    def should_computer_roll_enhanced(self, board, opponent_position):
        """Enhanced version of should_computer_roll with analysis"""
        if not self.should_computer_roll():
            return False
        
        # For easy AI, sometimes make random decisions
        if self.difficulty == "easy" and random.random() < 0.1:
            return random.choice([True, False])
        
        # Analyze position before rolling
        analysis = self.analyze_board_position(board, opponent_position)
        
        # Simulate possible dice outcomes (1-6)
        possible_outcomes = []
        for dice_value in range(1, 7):
            desirability = self.calculate_move_desirability(dice_value, board, opponent_position)
            possible_outcomes.append({
                'dice': dice_value,
                'score': desirability
            })
        
        # Calculate average desirability
        avg_desirability = sum(outcome['score'] for outcome in possible_outcomes) / 6
        best_outcome = max(possible_outcomes, key=lambda x: x['score'])
        worst_outcome = min(possible_outcomes, key=lambda x: x['score'])
        
        # Decision making based on difficulty
        if self.difficulty == "hard":
            # Hard AI is very strategic
            if len(analysis['nearby_snakes']) > 2:
                return avg_desirability > 5  # More cautious with many snakes
            else:
                return avg_desirability > -5  # Generally willing to take risks
                
        elif self.difficulty == "easy":
            # Easy AI is less strategic
            return avg_desirability > -15  # Takes more risks
            
        else:  # medium
            # Medium AI balances risk and reward
            return avg_desirability > -8
    
    def get_ai_decision_info(self, board, opponent_position):
        """Get information about AI's decision making for display"""
        analysis = self.analyze_board_position(board, opponent_position)
        
        decision_info = {
            'thinking': f"Analyzing position {self.position}...",
            'ladders_nearby': len(analysis['nearby_ladders']),
            'snakes_nearby': len(analysis['nearby_snakes']),
            'strategy': self.difficulty.capitalize() + " AI"
        }
        
        if analysis['opponent_ahead']:
            decision_info['status'] = "Trying to catch up"
        else:
            decision_info['status'] = "Playing defensively"
            
        return decision_info