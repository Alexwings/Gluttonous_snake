from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QScreen, QFont
from PyQt6.QtCore import Qt, pyqtSlot
from components.BasicBrick import Coordinates
import sys
from components.GameBoardWidget import GameBoardWidget

default_origin: Coordinates = None

def get_primary_screen_center() -> Coordinates:
    primary_screen = QApplication.primaryScreen()
    if primary_screen:
        screen_geometry = primary_screen.availableGeometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        return Coordinates(x=float(center_x), y=float(center_y))
    return Coordinates(0,0)

def main():
    app = QApplication(sys.argv)
    window = GameBoardWidget(width=500, height=600)
    window.setStyleSheet('background-color: #72CB7A')
    window.setWindowTitle('蛇贪食')
    # 获取屏幕中央原点
    screen_center = get_primary_screen_center()
    origin_x = screen_center.x - 250 if screen_center.x - 250 > 0 else 0
    origin_y = screen_center.y - 250 if screen_center.y - 250 > 0 else 0
    default_origin = Coordinates(x=origin_x, y=origin_y)
    window.setGeometry(int(default_origin.x), int(default_origin.y), 500, 600)
    window.show()
    window.start_timer()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()