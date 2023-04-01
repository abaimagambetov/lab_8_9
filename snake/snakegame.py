import pygame, sys, random, time

pygame.init()

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LINE_COLOR = (50, 50, 50)

# sizes of screen
HEIGHT = 400
WIDTH = 400
WIDTH2 = 500
BLOCK_SIZE = 20

# other characteristics and scores
FOOD_COUNT = 0
FPS = 5

# creating font and background
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)


class Wall:
    def __init__(self, level):
        self.body = []
        f = open("levels\level{}.txt".format(level), "r")

        # lines = content.split('\n')
        # print(len(lines[0]))

        for y in range(0, HEIGHT // BLOCK_SIZE + 1):
            for x in range(0, WIDTH // BLOCK_SIZE + 1):
                if f.read(1) == '#':
                    self.body.append(Point(x, y))

    def draw(self):
        for point in self.body:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (226, 135, 67), rect)


class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class Food:
    def __init__(self):
        self.location = Point(4, 10)
        self.location_x = 4
        self.location_y = 10
        self.list_colors = ["green", "yellow"]
        self.color = random.choice(self.list_colors)

    def draw(self):
        point = self.location
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        if self.color == "green":
            pygame.draw.rect(SCREEN, GREEN, rect)
        elif self.color == "yellow":
            pygame.draw.rect(SCREEN, YELLOW, rect)


class Snake:
    def __init__(self):
        # initial position
        self.body = [Point(10, 11)]
        self.dx = 0
        self.dy = 0
        self.level = 1
        self.is_ok = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # game over conditions if it hits the wall
        if self.body[0].x * BLOCK_SIZE > WIDTH - 20:
            gameOver()

        if self.body[0].y * BLOCK_SIZE > HEIGHT - 20:
            gameOver()

        if self.body[0].x < 0:
            gameOver()

        if self.body[0].y < 0:
            gameOver()

    def draw(self):
        point = self.body[0]
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, GREEN, rect)

        for point in self.body[1:]:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GREEN, rect)

    # spawn food randomly except on walls and snake
    def check_collision(self, food, wall):
        global FOOD_COUNT
        if self.body[0].x == food.location.x:
            if self.body[0].y == food.location.y:
                self.body.append(Point(food.location.x, food.location.y))
                self.is_ok = 0
                if food.color == "green":
                    FOOD_COUNT += 1
                elif food.color == "yellow":
                    FOOD_COUNT += 2
                    self.body.append(Point(food.location.x, food.location.y))
                food.color = random.choice(food.list_colors)

        food.location_x = random.randint(0, WIDTH // BLOCK_SIZE - 1)
        food.location_y = random.randint(0, HEIGHT // BLOCK_SIZE - 1)

        while self.is_ok == 0:
            self.is_ok = 1
            for point in wall.body:
                if food.location_x == point.x:
                    if food.location_y == point.y:
                        self.is_ok = 0

            for point in self.body:
                if food.location_x == point.x:
                    if food.location_y == point.y:
                        self.is_ok = 0

            if self.is_ok == 0:
                food.location_x = random.randint(0, WIDTH // BLOCK_SIZE - 1)
                food.location_y = random.randint(0, HEIGHT // BLOCK_SIZE - 1)
            else:
                self.is_ok = 1
                food.location = Point(food.location_x, food.location_y)

    # check whether snake collides with wall
    def check_collision1(self, wall):
        for point in wall.body:
            if self.body[0].x == point.x:
                if self.body[0].y == point.y:
                    gameOver()


def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, LINE_COLOR, rect, 1)


def gameOver():
    SCREEN.fill(RED)

    game_over = font.render("Game Over", True, BLACK)
    SCREEN.blit(game_over, (80, 150))
    pygame.display.update()

    time.sleep(3)
    pygame.quit()
    sys.exit()


def youWin():
    SCREEN.fill(GREEN)

    you_win = font.render("You Win", True, BLACK)
    SCREEN.blit(you_win, (120, 150))
    pygame.display.update()

    time.sleep(3)
    pygame.quit()
    sys.exit()


OOD_COUNT = 0
SCREEN = pygame.display.set_mode((WIDTH2, HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(BLACK)

snake = Snake()
food = Food()
wall = Wall(snake.level)

food_delay = 5000
food_event = pygame.USEREVENT + 1
pygame.time.set_timer(food_event, food_delay)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.dx = 1
                snake.dy = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.dx = -1
                snake.dy = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.dx = 0
                snake.dy = -1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.dx = 0
                snake.dy = 1
        if event.type == food_event:
            food.draw()

    snake.move()
    snake.check_collision(food, wall)
    snake.check_collision1(wall)

    # new level after 7 scores
    if len(snake.body) > 7:
        if snake.level == 4:
            youWin()

        snake.level += 1
        wall = Wall(snake.level)
        FPS += 2
        snake.dx = 0
        snake.dy = 0
        snake.body = [Point(10, 11)]

    SCREEN.fill(BLACK)

    snake.draw()
    wall.draw()
    food.draw()

    drawGrid()

    # scores and level number
    scores = font_small.render(str(FOOD_COUNT), True, GREEN)
    SCREEN.blit(scores, (WIDTH2 - 30, 10))

    level_number = font_small.render(str("level {}".format(snake.level)), True, GREEN)
    SCREEN.blit(level_number, (WIDTH2 - 70, 40))

    snake_len = font_small.render(str("length {}".format(len(snake.body))), True, GREEN)
    SCREEN.blit(snake_len, (WIDTH2 - 95, 70))

    pygame.display.update()
    CLOCK.tick(FPS)