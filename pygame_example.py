import pygame

HEIGHT = 600
WIDTH = 800

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    center = (WIDTH // 2, HEIGHT // 2)
    step = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        for x in range(0, WIDTH, step):
            for y in range(0, HEIGHT, step):
                pygame.draw.line(screen, "white", center, (x, y), 1)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
