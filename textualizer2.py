import pygame

from src.library.UIComponents.DraggablePolygon import DraggablePolygon
from src.library.UIComponents.UIComponentFactory import UIComponentFactory
from src.library.UIComponents.UIGroup import UIGroup
from src.library.UIComponents.Button import Button

from src.library.UIComponents.Internal.generalUI import WHITE, BLUE
from src.library.inputs import updateMouse, onMouse1Down, onMouse1Up

maxFramerate = 30
programTitle = "placeholder"

 
pygame.init()
 
size = (700, 500)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
 
pygame.display.set_caption(programTitle)
 
done = False
 
clock = pygame.time.Clock()

topLevelUI = UIGroup.build()
onMouse1Down.subscribe(lambda x, y, self=topLevelUI: topLevelUI.mouseDownEvent.invoke(self, x, y))
onMouse1Up.subscribe(lambda x, y, self=topLevelUI: topLevelUI.mouseUpEvent.invoke(self, x, y))

# buttonMenu = UIGroup.build()
# buttonMenu.x = 40
# buttonMenu.y = 70
# topLevelUI.addChild(buttonMenu)
# button2 = Button.addAnchorPoint(0.5, 0.5, "center").build()
# button2.x = 10
# button2.y = 70
# button2.width = 300
# button2.height = 60
# button2.text = "button 2"
# button2.mouseDownEvent.subscribe(lambda self, x, y: print("clicked 2"))
# button2.color = BLUE
# button2.textcolor = WHITE
# button1 = Button.addAnchorPoint(0.5, 0.5, "center").makeDraggable().build()
# # button1.objectToDrag = buttonMenu
# button1.x = 10
# button1.y = 5
# button1.width = 300
# button1.height = 60
# button1.text = "button 1 z"
# button1.mouseDownEvent.subscribe(lambda self, x, y: print("Clicked 1"))
# buttonMenu.addChild(line)
# buttonMenu.addChild(button1)
# buttonMenu.addChild(button2)

poly = DraggablePolygon.build()
poly.x = 40
poly.y = 50

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