import random
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class MultiplayerSnakeGame:
    def __init__(self, grid_width=20, grid_height=20):
        """
        Initialize the multiplayer snake game (server-side logic).
        
        Args:
            grid_width: Number of tiles horizontally
            grid_height: Number of tiles vertically
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # Initialize snake - start in the middle
        start_x = grid_width // 2
        start_y = grid_height // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Multiple fruits - one per connected player
        # Dictionary: player_id -> (x, y)
        self.fruits = {}
        
        # Game state
        self.score = 0
        self.game_over = False
        self.running = True
    
    def add_fruit_player(self, player_id):
        """Add a new fruit player and generate their initial position."""
        if player_id not in self.fruits:
            self.fruits[player_id] = self.generate_fruit_position()
    
    def remove_fruit_player(self, player_id):
        """Remove a fruit player."""
        if player_id in self.fruits:
            del self.fruits[player_id]
    
    def generate_fruit_position(self):
        """Generate a fruit position that's not on the snake or other fruits."""
        max_attempts = 100
        for _ in range(max_attempts):
            food_x = random.randint(0, self.grid_width - 1)
            food_y = random.randint(0, self.grid_height - 1)
            position = (food_x, food_y)
            
            # Check if position is valid (not on snake, not on other fruits)
            if position not in self.snake and position not in self.fruits.values():
                return position
        
        # Fallback: return a random position if we can't find a good one
        return (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
    
    def update_fruit_position(self, player_id, new_x, new_y):
        """Update a fruit player's position."""
        if player_id in self.fruits:
            # Validate position is within bounds
            if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                # Check if new position doesn't overlap with snake or other fruits
                new_pos = (new_x, new_y)
                if new_pos not in self.snake:
                    # Allow overlapping with other fruits (fruits can be on same tile)
                    self.fruits[player_id] = new_pos
                    return True
        return False
    
    def check_border_collision(self, head):
        """Check if the snake head hits the border."""
        x, y = head
        return x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height
    
    def check_self_collision(self, head):
        """Check if the snake head hits its own body."""
        return head in self.snake[1:]
    
    def update(self):
        """Update game state."""
        if self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        dx, dy = self.direction.value
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)
        
        # Check border collision
        if self.check_border_collision(new_head):
            self.game_over = True
            return
        
        # Check self collision
        if self.check_self_collision(new_head):
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if any fruit is eaten
        eaten_fruits = []
        for player_id, fruit_pos in self.fruits.items():
            if new_head == fruit_pos:
                eaten_fruits.append(player_id)
                self.score += 10
        
        # Regenerate eaten fruits
        for player_id in eaten_fruits:
            self.fruits[player_id] = self.generate_fruit_position()
        
        # If no fruit eaten, remove tail
        if not eaten_fruits:
            self.snake.pop()
    
    def set_direction(self, direction_str):
        """Set the snake's direction from a string."""
        direction_map = {
            'UP': Direction.UP,
            'DOWN': Direction.DOWN,
            'LEFT': Direction.LEFT,
            'RIGHT': Direction.RIGHT
        }
        
        if direction_str in direction_map:
            new_direction = direction_map[direction_str]
            # Prevent reversing into itself
            if (self.direction == Direction.UP and new_direction != Direction.DOWN) or \
               (self.direction == Direction.DOWN and new_direction != Direction.UP) or \
               (self.direction == Direction.LEFT and new_direction != Direction.RIGHT) or \
               (self.direction == Direction.RIGHT and new_direction != Direction.LEFT):
                self.next_direction = new_direction
    
    def get_game_state(self):
        """Get the current game state as a dictionary."""
        return {
            'snake': self.snake,
            'fruits': {pid: pos for pid, pos in self.fruits.items()},
            'score': self.score,
            'game_over': self.game_over,
            'grid_width': self.grid_width,
            'grid_height': self.grid_height
        }
    
    def reset(self):
        """Reset the game."""
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Regenerate all fruit positions
        for player_id in list(self.fruits.keys()):
            self.fruits[player_id] = self.generate_fruit_position()
        
        self.score = 0
        self.game_over = False
