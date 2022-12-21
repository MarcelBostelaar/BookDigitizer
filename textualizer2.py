import pygame

from src.debug import debugText, debugText2, debug
from src.library.UIComponents.DraggableQuadrilateral import draggableQuadrilateral
from src.library.UIComponents.UIGroup import UIGroup

from src.library.UIComponents.Internal.generalUI import WHITE
from src.library.UIComponents.splitScreen import leftRightSplitScreen
from src.library.inputs import updateMouse, onMouse1Down, onMouse1Up

maxFramerate = 30
programTitle = "placeholder"

pygame.init()
 
size = (700, 500)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
 
pygame.display.set_caption(programTitle)
 
done = False
 
clock = pygame.time.Clock()

topLevelUI = UIGroup()
onMouse1Down.subscribe(lambda x, y, self=topLevelUI: topLevelUI.onMouseDown.invoke(self, x, y))
onMouse1Up.subscribe(lambda x, y, self=topLevelUI: topLevelUI.onMouseUp.invoke(self, x, y))

poly1 = draggableQuadrilateral()
poly2 = draggableQuadrilateral()
split = leftRightSplitScreen()
split.left.addChild(poly1)
split.right.addChild(poly2)
split.width = 400
split.height = 300
split.centerDivision()
topLevelUI.addChild(split)

topLevelUI.addChild(debug)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)

    updateMouse()
    topLevelUI.onTick.invoke(topLevelUI)

    screen.fill(WHITE)

    topLevelUI.draw(screen)

    pygame.display.flip()


    # --- Limit to X frames per second
    clock.tick(maxFramerate)
 
pygame.quit()