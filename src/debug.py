from src.library.UIComponents.Internal.UIClass import UIElement
from src.library.UIComponents.Internal.generalUI import BLACK, drawTextNew, textSizeCalculator

debugText = UIElement()
debugText.textColor = BLACK
debugText.fontSize = 24
debugText.onDraw.subscribe(drawTextNew)
debugText.text = ""
debugText.width = 500
debugText.height = 200

debugText2 = UIElement()
debugText2.y = 30
debugText2.textColor = BLACK
debugText2.fontSize = 24
debugText2.onDraw.subscribe(drawTextNew)
debugText2.text = ""
debugText2.width = 500
debugText2.height = 200