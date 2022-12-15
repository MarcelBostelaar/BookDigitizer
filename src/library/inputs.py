import pygame.mouse
from src.library.events import event

x = 0
y = 0
[xMovement, yMovement] = [0,0]
(m1, m2, m3) = (False, False, False)
onMouse1Down = event()
onMouse1Up = event()


def updateMouse():
    global x, y, xMovement, yMovement, state, m1, m2, m3
    (x, y) = pygame.mouse.get_pos()
    [xMovement, yMovement] = pygame.mouse.get_rel()
    (b1, b2, b3) = pygame.mouse.get_pressed()
    if not m1 and b1:
        onMouse1Down.invoke(x, y)
    if m1 and not b1:
        onMouse1Up.invoke(x,y)
    (m1, m2, m3) = (b1, b2, b3)