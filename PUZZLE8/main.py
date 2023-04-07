
from Puzzle import Puzzle
import pygame
import pygame_gui
import time

pygame.init()
pygame.display.set_caption('Puzzle8')
window_surface = pygame.display.set_mode((1280, 720))
background = pygame.Surface((1280, 720))
background.fill(pygame.Color(255, 255, 255))
manager = pygame_gui.UIManager((1280, 720), None)

solve_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 370, 200, 100), text='Solve', manager=manager)
shuffle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 270, 200, 100), text='Random shuffle', manager=manager)

window_surface.blit(background, (0, 0))
pygame.display.update()
puzzle = Puzzle.new(250, 220, 330, 330, "1,2,3,4,5,6,7,8,0")
puzzle.initialize()
running = True

def draw_blocks(blocks):
    for block in blocks:
        if block['block'] != 0:
            pygame.draw.rect(window_surface, pygame.Color(0, 0, 0), block['rect'])
            textSurf = pygame.font.Font(None, 60).render(str(block['block']), True, pygame.Color(200, 200, 200))
            textRect = textSurf.get_rect()
            textRect.center = block['rect'].left+50, block['rect'].top+50
            window_surface.blit(textSurf, textRect)
        else:
            pygame.draw.rect(window_surface, pygame.Color(100, 100, 100), block['rect'])

def solveAnimation(moves):
    for mv in moves:
        zero = puzzle.matrix.searchBlock(0)
        if mv == "right":
            puzzle.matrix.moveright(zero)
        elif mv == "left":
            puzzle.matrix.moveleft(zero)
        elif mv == "up":
            puzzle.matrix.moveup(zero)
        elif mv == "down":
            puzzle.matrix.movedown(zero)
        puzzle.setBlocksMatrix()
        draw_blocks(puzzle.blocks)
        pygame.display.update()
        time.sleep(0.1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    puzzle.randomBlocks()
                elif event.ui_element == solve_button:
                    puzzle_resolve = puzzle.solve()
                    solveAnimation(puzzle_resolve[::-1])
                    resolve_text = '\n'.join(puzzle_resolve)
                    text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(900, 270, 100, 200), html_text=resolve_text, manager=manager)
        manager.process_events(event)
    manager.update(pygame.time.Clock().tick(60)/1000.0)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    draw_blocks(puzzle.blocks)
    pygame.display.update()