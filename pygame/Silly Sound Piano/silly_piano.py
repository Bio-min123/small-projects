import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Silly Sound Piano")

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 32)

# Load sound files
sounds = {
    pygame.K_a: pygame.mixer.Sound("boing.mp3"),
    pygame.K_s: pygame.mixer.Sound("pop.mp3"),
    pygame.K_d: pygame.mixer.Sound("meow.mp3"),
    pygame.K_f: pygame.mixer.Sound("drum.mp3")
}

labels = {
    pygame.K_a: "A = BOING!",
    pygame.K_s: "S = POP!",
    pygame.K_d: "D = MEOW!",
    pygame.K_f: "F = DRUM!"
}

last_sound = "Press A, S, D, or F!"

running = True

while running:
    screen.fill((255, 245, 200))

    title = font.render("Silly Sound Piano", True, (0, 0, 0))
    screen.blit(title, (230, 50))

    instruction = small_font.render("Press keyboard keys to play funny sounds!", True, (0, 0, 0))
    screen.blit(instruction, (190, 120))

    y = 200
    for text in labels.values():
        label = small_font.render(text, True, (40, 40, 40))
        screen.blit(label, (320, y))
        y += 45

    message = font.render(last_sound, True, (200, 50, 50))
    screen.blit(message, (230, 400))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in sounds:
                sounds[event.key].play()
                last_sound = labels[event.key]

    pygame.display.update()

pygame.quit()