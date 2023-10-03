import sys
from PyQt5.QtGui import QPen, QColor, QBrush, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QGraphicsView, QGraphicsScene, \
    QInputDialog, QGraphicsLineItem, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF
from math import fabs, floor


def sign(x):
    rez = 0 if x == 0 else 1 if x > 0 else -1
    return rez


class LineDrawer:
    @staticmethod
    def draw_line_cda(scene, x1, y1, x2, y2, image, pixmap, pixmap_item):
        dx = x2 - x1
        dy = y2 - y1
        steps = int(fabs(dx) if fabs(dx) > fabs(dy) else fabs(dy))

        x_increment = dx / steps
        y_increment = dy / steps

        x, y = x1 + 0.5 * sign(x_increment), y1 + 0.5 * sign(y_increment)

        image.setPixelColor(floor(x), floor(y), QColor(0, 0, 0))
        print(x - 500, -y + 250)
        print(floor(x-500), floor(-y+250))

        for _ in range(steps-1):
            print(_)
            x += x_increment
            y += y_increment
            print(x-500, -y+250)
            print(floor(x - 500), floor(-y + 250))

            image.setPixelColor(floor(x), floor(y), QColor(0, 0, 0))

        pixmap = QPixmap.fromImage(image)
        pixmap_item.setPixmap(pixmap)
        print('----------------------------')

    @staticmethod
    def draw_line_bresenham(scene, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        x_increment = 1 if dx > 0 else -1
        y_increment = 1 if dy > 0 else -1
        dx = fabs(dx)
        dy = fabs(dy)

        if dx > dy:
            p = 2 * dy - dx
            y = y1
            for x in range(x1, x2, x_increment):
                scene.addLine(x, y, x, y, QPen(Qt.black))
                if p >= 0:
                    y += y_increment
                    p -= 2 * dx
                p += 2 * dy
        else:
            p = 2 * dx - dy
            x = x1
            for y in range(y1, y2, y_increment):
                scene.addLine(x, y, x, y, QPen(Qt.black))
                if p >= 0:
                    x += x_increment
                    p -= 2 * dy
                p += 2 * dx

    @staticmethod
    def draw_wu(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.points = []

    def initUI(self):
        self.setGeometry(50, 50, 1400, 800)

        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItem('ЦДА')
        self.algorithm_combo.addItem('Брезенхем')
        self.algorithm_combo.move(10, 10)

        self.draw_button = QPushButton('Draw', self)
        self.draw_button.move(150, 10)
        self.draw_button.clicked.connect(self.get_coordinates)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.move(280, 10)
        self.clear_button.clicked.connect(self.clear_scene)

        self.debug_button = QPushButton('Debug', self)
        self.debug_button.move(410, 10)
        self.debug_button.clicked.connect(self.debug)

        self.view = QGraphicsView(self)
        # self.view = CoordinateGrid(self)
        self.view.setGeometry(10, 50, 1380, 700)
        self.view.scale(4, 4)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        image_width = 1000
        image_height = 500

        self.image = QImage(image_width, image_height, QImage.Format_RGB32)
        self.image.fill(QColor(255, 255, 255))

        x_pixel = 10
        y_pixel = 20
        self.image.setPixelColor(x_pixel, y_pixel, QColor(0, 0, 0))
        gray_color = QColor(200, 200, 200)

        for x in range(image_width):
            self.image.setPixelColor(x, image_height // 2, gray_color)

        for y in range(image_height):
            self.image.setPixelColor(image_width // 2, y, gray_color)

        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)

        self.scene.addItem(self.pixmap_item)

        # gray_pen = QPen(QColor(100, 100, 100))

        # self.x_axis = QGraphicsLineItem(-680, 0, 680, 0)
        # self.x_axis.setPen(gray_pen)
        # self.y_axis = QGraphicsLineItem(0, -340, 0, 340)
        # self.y_axis.setPen(gray_pen)
        #
        # self.scene.addItem(self.x_axis)
        # self.scene.addItem(self.y_axis)

    def get_coordinates(self):
        first_point, ok = QInputDialog.getText(self, 'Input', 'Enter coordinates for the first point (x, y):')
        if ok:
            second_point, ok = QInputDialog.getText(self, 'Input', 'Enter coordinates for the second point (x, y):')
            if ok:
                first_coordinates = [int(coord) for coord in first_point.split()]
                first_coordinates[0] = min(690, max(-690, first_coordinates[0]))
                first_coordinates[1] = min(350, max(-350, first_coordinates[1]))
                second_coordinates = [int(coord) for coord in second_point.split()]
                second_coordinates[0] = min(690, max(-690, second_coordinates[0]))
                second_coordinates[1] = min(350, max(-350, second_coordinates[1]))
                self.draw_line(*first_coordinates, *second_coordinates)

    def draw_line(self, x1, y1, x2, y2):
        selected_algorithm = self.algorithm_combo.currentText()
        # print(x1, x2, y1, y2)
        if selected_algorithm == 'ЦДА':
            LineDrawer.draw_line_cda(self.scene, x1+500, -y1+250, x2+500, -y2+250, self.image, self.pixmap, self.pixmap_item)
        elif selected_algorithm == 'Брезенхем':
            LineDrawer.draw_line_bresenham(self.scene, x1, -y1, x2, -y2)

    def clear_scene(self):
        pass

    def debug(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
