from settings import *
from random import choice, uniform

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # images
        # Need to mack the image bigger so the shadow appears inside the drawing surface we are creating
        self.image_size = (SIZE['paddle'][0] + 10, SIZE['paddle'][1])
        self.image = pygame.Surface(self.image_size, pygame.SRCALPHA)
        # Paddle shadow
        pygame.draw.rect(self.image, COLORS['paddle shadow'], pygame.FRect((10, 8), SIZE['paddle']), 0, 10)
        # Paddle
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0,0), SIZE['paddle']), 0, 10)

        # rects
        self.rect = self.image.get_frect(center=POS['player'])
        self.old_rect = self.rect.copy()
        self.direction = 0

    # Function for calculating movement
    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        # Checks to ensure player doesn't go out of bounds
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    # Function to update sprite
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = SPEED['player']


    def get_direction(self):
        keys =  pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

class Opponent(Paddle):
    # Passed the ball through so opponent can access it
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = SPEED['opponent']
        # Rect
        self.rect.center = POS['opponent']
        # Ball
        self.ball = ball

    # Move the paddle based on the balls direction.
    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        # image
        self.ball_surface_size = (45,45)
        self.image = pygame.Surface(self.ball_surface_size, pygame.SRCALPHA)
        # circle gets the image, a center, and a radius
        # Ball shadow
        pygame.draw.circle(self.image, COLORS['ball shadow'], (SIZE['ball'][0] / 2 +5, SIZE['ball'][1] / 2 +5), SIZE['ball'][0] / 2)
        # Ball
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0]/2)

        #rect and movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed_modifier = 0

        # Timer for delay
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500


    # Update shadow
    # def move_shadow(self):
        # update shadow based on position of ball. Call at the end of update()

    # Checks to ensure player doesn't go out of bounds
    def move(self, dt):
        self.rect.x += self.direction.x * SPEED['ball'] * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.y += self.direction.y * SPEED['ball'] * dt * self.speed_modifier
        self.collision('vertical')

    # Check for ball collision with paddles
    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                # Adjust for horizontal collisions
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                # Adjust for vertical collisions
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1
    #Checks for collisions with walls
    def wall_collision(self):
        # Ensure ball doesn't go out of bounds.
        if self.rect.top < 0:
            # Have to reset it to be inbounds are it can glitch out and get stuck
            self.rect.top = 0
            self.direction.y *= -1
        # Bottom check
        elif self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        # Score check
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()

    def reset(self):
        # Reset ball and paddle positions
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        for sprite in self.paddle_sprites:
            sprite.rect.centery = WINDOW_HEIGHT / 2

        # Delay ball for the next round
        self.start_time = pygame.time.get_ticks()
        self.speed_modifier = 0
        # Randomize direction again
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, 1)))

    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(dt)
        self.wall_collision()
