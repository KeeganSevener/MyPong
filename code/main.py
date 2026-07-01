# settings.py are imported from sprites which imports settings.py
from sprites import *
import json

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
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score   )
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # Score keeping
        # Try to get score from text file with json data
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        # Use default score if no file exists.
        except:
            self.score = {'player': 0, 'opponent': 0}
        self.font = pygame.font.Font(None, 160)

    def display_score(self):
        # Player score
        player_surface = self.font.render(str(self.score['player']), True, COLORS['bg text'])
        player_rect = player_surface.get_frect(center = (WINDOW_WIDTH/2 + 175, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surface, player_rect)
        # opponent score
        opponent_surface = self.font.render(str(self.score['opponent']), True, COLORS['bg text'])
        opponent_rect = opponent_surface.get_frect(center=(WINDOW_WIDTH / 2 - 175, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surface, opponent_rect)

        # Line separator
        pygame.draw.line(
            self.display_surface,
            COLORS['bg text'],
            (WINDOW_WIDTH / 2, 0),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT),
            10
        )

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    # Do something
    def run(self):
        while self.running:
            # Get delta time
            dt = self.clock.tick() / 1000
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    with open(join('data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)

            #Updates
            self.all_sprites.update(dt)

            #Drawing
            self.display_surface.fill(COLORS['bg'])
            self.display_score()
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