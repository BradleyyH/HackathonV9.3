import pygame
import random
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, grid_width=20, grid_height=20, tile_size=30):
        """
        Initialize the snake game.
        
        Args:
            grid_width: Number of tiles horizontally
            grid_height: Number of tiles vertically
            tile_size: Size of each tile in pixels
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size
        
        # Calculate window dimensions
        self.window_width = grid_width * tile_size
        self.window_height = grid_height * tile_size
        
        # Colors - two shades of green for checkerboard
        self.green_dark = (34, 139, 34)   # Forest green
        self.green_light = (144, 238, 144)  # Light green
        self.snake_color = (255, 255, 0)  # Yellow
        self.food_color = (255, 0, 0)     # Red
        self.border_color = (0, 0, 0)     # Black
        
        # Initialize snake - start in the middle
        start_x = grid_width // 2
        start_y = grid_height // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Initialize food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.game_over = False
        self.running = True
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
    
    def generate_food(self):
        """Generate food at a random position that's not on the snake."""
        while True:
            food_x = random.randint(0, self.grid_width - 1)
            food_y = random.randint(0, self.grid_height - 1)
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)
    
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
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def handle_input(self, keys):
        """Handle keyboard input."""
        if keys[pygame.K_UP] and self.direction != Direction.DOWN:
            self.next_direction = Direction.UP
        elif keys[pygame.K_DOWN] and self.direction != Direction.UP:
            self.next_direction = Direction.DOWN
        elif keys[pygame.K_LEFT] and self.direction != Direction.RIGHT:
            self.next_direction = Direction.LEFT
        elif keys[pygame.K_RIGHT] and self.direction != Direction.LEFT:
            self.next_direction = Direction.RIGHT
    
    def draw_checkerboard(self):
        """Draw the checkerboard pattern with two shades of green."""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Alternate colors in checkerboard pattern
                if (x + y) % 2 == 0:
                    color = self.green_light
                else:
                    color = self.green_dark
                
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_snake(self):
        """Draw the snake."""
        for segment in self.snake:
            x, y = segment
            rect = pygame.Rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(self.screen, self.snake_color, rect)
            # Add border to snake segments
            pygame.draw.rect(self.screen, self.border_color, rect, 1)
    
    def draw_food(self):
        """Draw the food."""
        x, y = self.food
        rect = pygame.Rect(
            x * self.tile_size,
            y * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        pygame.draw.rect(self.screen, self.food_color, rect)
        pygame.draw.rect(self.screen, self.border_color, rect, 1)
    
    def draw_game_over(self):
        """Draw game over message."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Score: {self.score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        
        # Draw semi-transparent background
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        self.screen.blit(text, text_rect)
        
        restart_text = font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 40))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_score(self):
        """Draw the score."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
    
    def render(self):
        """Render the game."""
        self.draw_checkerboard()
        self.draw_food()
        self.draw_snake()
        self.draw_score()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def reset(self):
        """Reset the game."""
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def run(self, fps=10):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset()
            
            keys = pygame.key.get_pressed()
            self.handle_input(keys)
            self.update()
            self.render()
            self.clock.tick(fps)
        
        pygame.quit()

if __name__ == "__main__":
    # Create game with custom grid size (20x20 tiles, 30 pixels each)
    game = SnakeGame(grid_width=20, grid_height=20, tile_size=30)
    game.run(fps=10)
