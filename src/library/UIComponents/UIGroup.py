from src.library.UIComponents.Internal.UIClass import UIElement
from src.library.UIComponents.Internal.childElementsComponent import addChildFunctionality, drawContained, \
    resizeWithChildren


def UIGroup():
    group = UIElement()
    addChildFunctionality(group)
    resizeWithChildren(group)
    group.onDraw.subscribe(drawContained)
    return group

