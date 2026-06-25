#from operator import truediv (autoloaded in i think. pretty sure i dont need it)
# settings are imported from sprites which imports settings.
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Keegan\'s Pong')
        self.running = True
        self.clock = pygame.time.Clock()

        #Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        # Create the player for right hand side and the ball
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)


    # Runs the main game loop
    def run(self):
        while self.running:
            # Get delta time
            dt = self.clock.tick() / 1000
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            # Updates
            self.all_sprites.update(dt)

            # Drawing
            self.display_surface.fill(COLORS['bg'])
            # Draw sprites on display surface
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

# Only run if it is the main file.
if __name__ == '__main__':
    game = Game()
    game.run()

# quit pygame and exit
pygame.quit()
exit()