
from src.library.UIComponents.Internal.generalUI import RED, BLUE
from src.library.UIComponents.UIComponentFactory import UIComponentFactory
from src.library.UIComponents.UIGroup import UIGroup

draggableCorner = UIComponentFactory()\
    .addChildFunctionality()\
    .resizeWithChildren()\
    .drawInternalCentered()\
    .afterBuild(lambda parent:
                parent
                .addChild(
                    UIComponentFactory()
                    .drawRectangle()
                    .copyProperty(parent, "color")
                    .copyProperty(parent, "width")
                    .copyProperty(parent, "height")
                    .makeDraggable()
                    .afterBuild(lambda square: square.setAttribute("objectToDrag", parent))
                    .build()
                    )
                )


def afterBuilderFunc(polygon):
    corner = draggableCorner.dependantProperty(polygon, "color", lambda x: getattr(x, "squareColor"))
    line = UIComponentFactory().dependantProperty(polygon, "color", lambda x: getattr(x, "lineColor"))
    return polygon\
        .anchorAt(corner, 0, 0, "topLeft")\
        .anchorAt(corner, 1, 0, "topRight")\
        .anchorAt(corner, 0, 1, "bottomLeft")\
        .anchorAt(corner, 1, 1, "bottomRight")\
        .addChild(line.drawLine(polygon.topLeft, polygon.topRight).build())\
        .addChild(line.drawLine(polygon.topRight, polygon.bottomRight).build())\
        .addChild(line.drawLine(polygon.bottomRight, polygon.bottomLeft).build())\
        .addChild(line.drawLine(polygon.bottomLeft, polygon.topLeft).build())


DraggablePolygon_partA = UIGroup\
    .afterBuild(lambda polygon: setattr(polygon, "width", 300))\
    .afterBuild(lambda polygon: setattr(polygon, "height", 300))\
    .defaultLineWidth()\
    .addAttribute("lineColor", RED)\
    .addAttribute("squareColor", BLUE)

DraggablePolygon = DraggablePolygon_partA\
    .afterBuild(afterBuilderFunc)