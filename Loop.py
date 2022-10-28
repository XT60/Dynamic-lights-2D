import pygame
import Config
import tile_map
import light_handling


win = pygame.display.set_mode(Config.WINDOW_SIZE)
clock = pygame.time.Clock()
map = tile_map.Tile_map()
light = light_handling.light_handling(map.walls, map.points)

flag = True
while flag:
    clock.tick(Config.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    map.update_variables(mouse_pos, mouse_pressed, light)
    light.update_variables(mouse_pos, mouse_pressed)

    win.fill((0,0,0))
    light.draw(win)
    map.draw(win)

    pygame.display.update()