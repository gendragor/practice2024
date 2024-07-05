import cv2
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
    QFileDialog, QInputDialog, QMessageBox
)

"""
Программа для ознакомительной практики
@author Max Dzhigrenyuk KI23-16/1b
@version 1.0
"""

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image = None
        self.image_label = QLabel()

        self.initUI()

    def initUI(self):
        # создание главного окна приложения
        self.setWindowTitle("Окно приложения")
        self.resize(1000, 750)

        # создание кнопок приложения
        load_button = QPushButton("Выбрать и загрузить изображение (Изображение может быть формата png и jpg)", self)
        webcam_button = QPushButton("Подключиться к веб-камере и сделать с нее фотоснимок", self)
        red_channel_button = QPushButton("Показать красный канал изображения", self)
        green_channel_button = QPushButton("Показать зеленый канал изображения", self)
        blue_channel_button = QPushButton("Показать синий канал изображения", self)
        brightness_button = QPushButton("Понизить яркость изображения", self)
        grayscale_button = QPushButton("Получить изображение в оттенках серого.", self)
        rectangle_button = QPushButton("Нарисовать прямоугольник на изображении синим цветом", self)

        # логика кнопок
        load_button.clicked.connect(self.load_image)
        webcam_button.clicked.connect(self.capture_image)
        red_channel_button.clicked.connect(lambda: self.show_channel(2))
        green_channel_button.clicked.connect(lambda: self.show_channel(1))
        blue_channel_button.clicked.connect(lambda: self.show_channel(0))
        brightness_button.clicked.connect(self.decrease_brightness)
        grayscale_button.clicked.connect(self.convert_to_grayscale)
        rectangle_button.clicked.connect(self.draw_rectangle)

        # вывод кнопок
        layout = QVBoxLayout()
        layout.addWidget(load_button)
        layout.addWidget(webcam_button)
        layout.addWidget(red_channel_button)
        layout.addWidget(green_channel_button)
        layout.addWidget(blue_channel_button)
        layout.addWidget(brightness_button)
        layout.addWidget(grayscale_button)
        layout.addWidget(rectangle_button)
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):

        # выбор готового изображения
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Выберете изображение", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is None:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить изображение.")
            else:
                self.display_image(self.image)

    def capture_image(self):

        # выбор изображения с веб-камеры
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть веб-камеру.")
            return
        ret, frame = cap.read()
        if not ret:
            QMessageBox.critical(self, "Ошибка", "Не удалось захватить изображение.")
            return
        self.image = frame
        self.display_image(self.image)
        cap.release()

    def show_channel(self, channel):

        # показать красный, зеленый или синий канал изображения
        if self.image is None:
            QMessageBox.critical(self, "Ошибка", "Изображение еще не загружено.")
            return
        channel_image = np.zeros_like(self.image)
        channel_image[:, :, channel] = self.image[:, :, channel]
        self.display_image(channel_image)

    def decrease_brightness(self):

        # понизить яркость изображения
        if self.image is None:
            QMessageBox.critical(self, "Ошибка", "Изображение еще не загружено.")
            return
        value, ok = QInputDialog.getInt(self, "Уменьшить яркость изображения", "Введите значение на которое следует"
                                                                               " понизить яркость:", 10, 0, 255)
        if ok:
            self.image = np.clip(self.image - value, 0, 255).astype(np.uint8)
            self.display_image(self.image)

    def convert_to_grayscale(self):

        # изображение в оттенках серого
        if self.image is None:
            QMessageBox.critical(self, "Ошибка", "Изображение еще не загружено.")
            return
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.display_image(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR))

    def draw_rectangle(self):

        # нарисовать прямоугольник
        if self.image is None:
            QMessageBox.critical(self, "Ошибка", "Изображение еще не загружено.")
            return
        x, ok1 = QInputDialog.getInt(self, "Рисуем прямоугольник", "Введите координату по x:", 0, 0,
                                     self.image.shape[1])
        y, ok2 = QInputDialog.getInt(self, "Рисуем прямоугольник", "Введите координату по y:", 0, 0,
                                     self.image.shape[0])
        w, ok3 = QInputDialog.getInt(self, "Рисуем прямоугольник", "Введите ширину прямоугольника:", 50, 0,
                                     self.image.shape[1] - x)
        h, ok4 = QInputDialog.getInt(self, "Рисуем прямоугольник", "Введите высоту прямоугольника:", 50, 0,
                                     self.image.shape[0] - y)
        if ok1 and ok2 and ok3 and ok4:
            image_with_rectangle = self.image.copy()
            cv2.rectangle(image_with_rectangle, (x, y), (x + w, y + h), (255, 0, 0), 2)
            self.display_image(image_with_rectangle)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        self.image_label.setPixmap(QPixmap.fromImage(q_image).scaled(
            self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))



