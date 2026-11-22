import pygame, sys

from settings import screenWidth,screenHeight,fps, COLOR_BG,COLOR_TEXT,COLOR_COIN, COLOR_PLATFORM, COLOR_PLAYER

from gameObjects import Player , Platform, Coin


from saveManager import LoadProgress, saveProgress

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
high_score = LoadProgress()
score = 0
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()

level_platforms = [
    Platform(0,screenHeight-40,screenWidth,40),
    Platform(150,320,200,40),
    Platform(150,460,200,20)
]

level_coins = [
    Coin(220, 480, 24, 24),
    Coin(520, 340, 24, 24),
    Coin(280, 500, 24, 24),
    Coin(150, 270, 24, 24),
]
for c in level_coins:
    coins.add(c)

for p in level_platforms:
    platforms.add(p)
player = Player(100, screenHeight - 120, 60, 80)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    player.update(platforms)

    collected = pygame.sprite.spritecollide(player, coins, True)
    if collected:
        score += len(collected)
        if score > high_score.get("coins"):
            high_score["coins"] = score
    screen.fill(COLOR_BG)
    platforms.draw(screen)
    coins.draw(screen)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(fps)
saveProgress(high_score)
pygame.quit()
sys.exit()