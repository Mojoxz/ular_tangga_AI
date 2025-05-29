import random

def roll_dice():
    """Simulate dice roll (1-6)"""
    return random.randint(1, 6)

def get_board_coordinates(position):
    """Convert board position (1-100) to row, col coordinates"""
    if position < 1 or position > 100:
        return None, None
    
    # Adjust for 0-based indexing
    pos = position - 1
    row = pos // 10
    col = pos % 10
    
    # Handle zigzag pattern (odd rows go right to left)
    if row % 2 == 1:
        col = 9 - col
    
    return row, col