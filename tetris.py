import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# Colors for tetromino shapes
SHAPES_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_tetromino = self.new_tetromino()
        self.next_tetromino = self.new_tetromino()
        self.game_over = False
        self.score = 0

    def new_tetromino(self):
        shape = random.choice(SHAPES)
        color = SHAPES_COLORS[SHAPES.index(shape)]
        return Tetromino(shape, color)

    def draw_board(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.board[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def draw_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, tetromino.color, ((tetromino.x + x) * GRID_SIZE, (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def valid_move(self, tetromino, dx, dy):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = tetromino.x + x + dx
                    new_y = tetromino.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and self.board[new_y][new_x] != BLACK):
                        return False
        return True

    def freeze_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[tetromino.y + y][tetromino.x + x] = tetromino.color

    def clear_lines(self):
        lines_to_clear = [y for y, row in enumerate(self.board) if all(cell != BLACK for cell in row)]
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        self.score += len(lines_to_clear)

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_tetromino(self.current_tetromino)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_tetromino, -1, 0):
                        self.current_tetromino.x -= 1
                    elif event.key == pygame.K_RIGHT and self.valid_move(self.current_tetromino, 1, 0):
                        self.current_tetromino.x += 1
                    elif event.key == pygame.K_DOWN and self.valid_move(self.current_tetromino, 0, 1):
                        self.current_tetromino.y += 1
                    elif event.key == pygame.K_UP:
                        self.current_tetromino.rotate()
                        if not self.valid_move(self.current_tetromino, 0, 0):
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()

            if not self.valid_move(self.current_tetromino, 0, 1):
                self.freeze_tetromino(self.current_tetromino)
                self.clear_lines()
                self.current_tetromino = self.next_tetromino
                self.next_tetromino = self.new_tetromino()
                if not self.valid_move(self.current_tetromino, 0, 0):
                    self.game_over = True
            else:
                self.current_tetromino.y += 1

            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    Tetris().run()
