import sys

from PySide6.QtWidgets import (
    QApplication
)

import prog

"""
Программа для ознакомительной практики
@author Max Dzhigrenyuk KI23-16/1b
@version 1.0
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = prog.ImageProcessor()
    window.show()
    sys.exit(app.exec())
