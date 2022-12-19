import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CLEAR = (0,255,0,40)


def drawRectangle(self, surface):
    pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


def drawText(UIObject, surface):
    text = createText(UIObject.text, UIObject.width, UIObject.height, UIObject.textColor, UIObject.fontSize)
    drawCentered_DEPRECATED(surface, text, UIObject.x, UIObject.y, UIObject.width, UIObject.height)


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


def drawCentered_DEPRECATED(surface, img, posx, posy, width, height):
    imgSize = img.get_rect()
    xPos = int(posx + ((width - imgSize.width)/2))
    yPos = int(posy + ((height - imgSize.height)/2))
    surface.blit(img, (xPos, yPos))


def makeText(text, fontSize, color):
    font = pygame.font.SysFont(None, fontSize)
    return font.render(text, True, color)


def drawTextNew(UIObject, surface):
    img = makeText(UIObject.text, UIObject.fontSize, UIObject.textColor)
    surface.blit(img, (UIObject.x, UIObject.y))


def textSizeCalculator(text, fontSize):
    img = makeText(text, fontSize, BLACK)
    return img.get_width(), img.get_height()
