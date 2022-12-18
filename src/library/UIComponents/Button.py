from src.library.UIComponents.Internal.UIClass import UIElement
from src.library.UIComponents.Internal.childElementsComponent import addChildFunctionality, drawContained
from src.library.UIComponents.Internal.generalUI import RED, drawRectangle, drawText, BLACK


def newButton():
    buttonTopLevel = UIElement()
    addChildFunctionality(buttonTopLevel)
    buttonTopLevel.onDraw.subscribe(drawContained)
    buttonTopLevel.text = "your text here"
    buttonTopLevel.color = RED
    buttonTopLevel.textColor = BLACK
    buttonTopLevel.fontSize = 24

    background = UIElement()
    background.onDraw.subscribe(drawRectangle)
    background.copyProperty("color", buttonTopLevel)
    background.copyProperty("width", buttonTopLevel)
    background.copyProperty("height", buttonTopLevel)
    buttonTopLevel.addChild(background)

    text = UIElement()
    text.copyProperty("textColor", buttonTopLevel)
    text.copyProperty("fontSize", buttonTopLevel)
    text.copyProperty("width", buttonTopLevel)
    text.copyProperty("height", buttonTopLevel)
    text.onDraw.subscribe(drawText)
    buttonTopLevel.addChild(text)

    return buttonTopLevel

