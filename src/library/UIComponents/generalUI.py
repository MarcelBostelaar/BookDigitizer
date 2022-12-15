import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CLEAR = (0,0,0,0)


def scaleDownIfNeeded(img, width, height):
    size = img.get_rect()
    target = pygame.rect.Rect(0,0, width, height)
    newSize = size.fit(target)
    pygame.transform.scale(img, (newSize.width, newSize.height))
    return img


def createText(text, width, height, textcolor, fontsize):
    font = pygame.font.SysFont(None, fontsize)
    img = font.render(text, True, textcolor)
    return scaleDownIfNeeded(img, width, height)


def drawCentered(surface, img, posx, posy, width, height):
    imgSize = img.get_rect()
    xPos = int(posx + ((width - imgSize.width)/2))
    yPos = int(posy + ((height - imgSize.height)/2))
    surface.blit(img, (xPos, yPos))