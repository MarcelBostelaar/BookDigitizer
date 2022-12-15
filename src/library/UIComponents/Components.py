from src.library.UIComponents.UIComponentFactory import UIComponentFactory

Button = UIComponentFactory()\
    .addChildFunctionality()\
    .drawInternalRegular()\
    .defaultText()\
    .defaultColor()\
    .afterBuild(lambda parent: parent.addChild(
        UIComponentFactory()
        .drawRectangle()
        .copyProperty(parent, "color")
        .copyProperty(parent, "width")
        .copyProperty(parent, "height")
        .build()
        )
    )\
    .afterBuild(lambda parent: parent.addChild(
        UIComponentFactory()
        .drawText()
        .defaultTextColor()
        .defaultFontSize()
        .copyProperty(parent, "width")
        .copyProperty(parent, "height")
        .copyProperty(parent, "text")
        .build()
        )
    )

UIGroup = UIComponentFactory()\
    .addChildFunctionality()\
    .drawInternalRegular()\
    .resizeWithChildren()