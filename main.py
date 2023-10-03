import sys
from math import fabs, floor

from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QGraphicsView, QGraphicsScene, \
    QInputDialog, QGraphicsPixmapItem


def convertY(y):
    return -(y - 250) + 250


def sign(x):
    rez = 0 if x == 0 else 1 if x > 0 else -1
    return rez


class LineDrawer:
    @staticmethod
    def draw_line_cda(x1, y1, x2, y2, image, pixmap_item):
        dx = x2 - x1
        dy = y2 - y1
        steps = int(fabs(dx) if fabs(dx) > fabs(dy) else fabs(dy))

        x_increment = dx / steps
        y_increment = dy / steps

        x, y = x1 + 0.5 * sign(x_increment), y1 + 0.5 * sign(y_increment)

        image.setPixelColor(floor(x), floor(y), QColor(0, 0, 0))
        print(x - 500, -y + 250)
        print(floor(x - 500), floor(-y + 250))

        for _ in range(steps - 1):
            print(f'Step - {_ + 1}')
            x += x_increment
            y += y_increment
            print(f'X - {x - 500}')
            print(f'Y - {-y + 250}')
            print(f'Plot - ({floor(x - 500)},{floor(-y + 250)})')
            image.setPixelColor(floor(x), floor(y), QColor(0, 0, 0))

        pixmap = QPixmap.fromImage(image)
        pixmap_item.setPixmap(pixmap)
        print('----------------------------')

    @staticmethod
    def draw_line_bresenham(x1, y1, x2, y2, image, pixmap_item):
        dx = x2 - x1
        dy = y2 - y1

        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = x1, y1

        error, t = el / 2, 0

        image.setPixelColor(x, convertY(y), QColor(0, 0, 0))

        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            image.setPixelColor(x, convertY(y), QColor(0, 0, 0))

        pixmap = QPixmap.fromImage(image)
        pixmap_item.setPixmap(pixmap)

    @staticmethod
    def draw_wu(x1, y1, x2, y2, image, pixmap_item):
        points = []

        # Рассчитываем разницу в координатах и определяем направление движения
        dx = x2 - x1
        dy = y2 - y1
        is_steep = abs(dy) > abs(dx)

        # Если линия крутая, то меняем местами x и y координаты
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Если начальная точка справа от конечной, меняем их местами
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        # Рассчитываем разницу в координатах снова, после обмена
        dx = x2 - x1
        dy = y2 - y1

        # Вычисляем коэффициент наклона (наклон линии)
        gradient = dy / dx if dx != 0 else 1

        # Начальная и конечная целочисленные координаты начальной точки
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xpxl1 = xend  # Первая точка на линии
        ypxl1 = int(yend)

        if is_steep:
            points.append((ypxl1, xpxl1))
            points.append((ypxl1 + 1, xpxl1))
        else:
            points.append((xpxl1, ypxl1))
            points.append((xpxl1, ypxl1 + 1))

        # Определяем начальную и конечную точки для второй половины линии
        intery = yend + gradient  # Потенциально пересекающий пиксель

        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xpxl2 = xend  # Вторая точка на линии
        ypxl2 = int(yend)

        if is_steep:
            points.append((ypxl2, xpxl2))
            points.append((ypxl2 + 1, xpxl2))
        else:
            points.append((xpxl2, ypxl2))
            points.append((xpxl2, ypxl2 + 1))

        # Заполняем промежуток между линиями пикселями
        if is_steep:
            for x in range(xpxl1 + 1, xpxl2):
                points.append((int(intery), x))
                points.append((int(intery) + 1, x))
                intery += gradient
        else:
            for x in range(xpxl1 + 1, xpxl2):
                points.append((x, int(intery)))
                points.append((x, int(intery) + 1))
                intery += gradient

        sorted_points = sorted(points)
        for coord in sorted_points:
            x, y = coord
            print(f'X - {x - 500}')
            print(f'Y - {-y + 250}')
            print(f'Plot - ({floor(x - 500)},{floor(-y + 250)})')
            image.setPixelColor(x, y, QColor(0, 0, 0))
        pixmap = QPixmap.fromImage(image)
        pixmap_item.setPixmap(pixmap)
        print(sorted_points)


class QuadraticCurve:

    @staticmethod
    def bresenham_circle(point_x, point_y, radius, image, pixmap_item):
        x = int(radius)
        y = 0
        decision = 1 - int(radius)  # Начальное значение параметра принятия решения
        points = []
        point_y = int(point_y)
        point_x = int(point_x)

        while x >= y:
            # Отобразить точку и её симметричную
            points.append((x + point_x, y + point_y))
            points.append((-x + point_x, y + point_y))
            points.append((x + point_x, -y + point_y))
            points.append((-x + point_x, -y + point_y))
            points.append((y + point_x, x + point_y))
            points.append((-y + point_x, x + point_y))
            points.append((y + point_x, -x + point_y))
            points.append((-y + point_x, -x + point_y))

            y += 1
            if decision <= 0:
                decision += 2 * y + 1
            else:
                x -= 1
                decision += 2 * (y - x) + 1
        sorted_points = sorted(points)
        for coord in sorted_points:
            x, y = coord
            print(f'X - {x - 500}')
            print(f'Y - {-y + 250}')
            print(f'Plot - ({floor(x - 500)},{floor(-y + 250)})')
            image.setPixelColor(x, y, QColor(0, 0, 0))
        pixmap = QPixmap.fromImage(image)
        pixmap_item.setPixmap(pixmap)
        print(sorted_points)
        print(points)


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
        self.algorithm_combo.addItem('Алгоритм Ву')
        self.algorithm_combo.move(10, 10)

        self.draw_button = QPushButton('Линия', self)
        self.draw_button.move(150, 10)
        self.draw_button.clicked.connect(self.get_coordinates)

        self.draw_circle_button = QPushButton('Окружность', self)
        self.draw_circle_button.move(280, 10)
        self.draw_circle_button.clicked.connect(self.get_circle_coordinates)

        self.clear_button = QPushButton('Очистить', self)
        self.clear_button.move(400, 10)
        self.clear_button.clicked.connect(self.clear_scene)

        self.view = QGraphicsView(self)
        # self.view = CoordinateGrid(self)
        self.view.setGeometry(10, 50, 1380, 700)
        self.view.scale(3, 3)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        image_width = 1000
        image_height = 500

        self.image = QImage(image_width, image_height, QImage.Format_RGB32)
        self.image.fill(QColor(255, 255, 255))

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

    def get_circle_coordinates(self):
        point, ok = QInputDialog.getText(self, 'Input', 'Enter coordinates for the centre of circle (x, y):')
        if ok:
            r, ok = QInputDialog.getText(self, 'Input', 'Enter radius for circle:')
            if ok:
                point_coordinates = [int(coord) for coord in point.split()]
                point_coordinates[0] = min(500, max(-500, point_coordinates[0]))
                point_coordinates[1] = min(250, max(-250, point_coordinates[1]))
                self.draw_circle(*point_coordinates, r)

    def draw_circle(self, x, y, r):
        QuadraticCurve.bresenham_circle(x + 500, -y + 250, r, self.image, self.pixmap_item)

    def get_coordinates(self):
        first_point, ok = QInputDialog.getText(self, 'Input', 'Enter coordinates for the first point (x, y):')
        if ok:
            second_point, ok = QInputDialog.getText(self, 'Input', 'Enter coordinates for the second point (x, y):')
            if ok:
                first_coordinates = [int(coord) for coord in first_point.split()]
                first_coordinates[0] = min(500, max(-500, first_coordinates[0]))
                first_coordinates[1] = min(250, max(-250, first_coordinates[1]))
                second_coordinates = [int(coord) for coord in second_point.split()]
                second_coordinates[0] = min(500, max(-500, second_coordinates[0]))
                second_coordinates[1] = min(250, max(-250, second_coordinates[1]))
                self.draw_line(*first_coordinates, *second_coordinates)

    def draw_line(self, x1, y1, x2, y2):
        selected_algorithm = self.algorithm_combo.currentText()
        # print(x1, x2, y1, y2)
        if selected_algorithm == 'ЦДА':
            LineDrawer.draw_line_cda(x1 + 500, -y1 + 250, x2 + 500, -y2 + 250, self.image, self.pixmap_item)
        elif selected_algorithm == 'Брезенхем':
            LineDrawer.draw_line_bresenham(x1 + 500, y1 + 250, x2 + 500, y2 + 250, self.image, self.pixmap_item)
        elif selected_algorithm == 'Алгоритм Ву':
            LineDrawer.draw_wu(x1 + 500, -y1 + 250, x2 + 500, -y2 + 250, self.image, self.pixmap_item)
    def clear_scene(self):
        self.image.fill(QColor(255, 255, 255))
        gray_color = QColor(200, 200, 200)

        for x in range(1000):
            self.image.setPixelColor(x, 500 // 2, gray_color)

        for y in range(500):
            self.image.setPixelColor(1000 // 2, y, gray_color)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
