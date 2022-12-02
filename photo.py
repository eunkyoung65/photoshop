import sys
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow, 
    QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        # 메뉴바 만들기
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("파일")
        exit = QAction("나가기", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)

        # 메인화면 레이아웃
        main_layout = QHBoxLayout()

        # 사이드바 메뉴버튼
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("좌우반전")
        button3 = QPushButton("상하반전")
        button4 = QPushButton("새로고침")
        button5 = QPushButton("흑백전환")
        button6 = QPushButton("블러처리")
        button7 = QPushButton("사진반전")
        button8 = QPushButton("사진 원형모양 자르기")
        button9 = QPushButton("볼록효과")





        
        button1.clicked.connect(self.show_file_dialog)
        button2.clicked.connect(self.flip_image)
        button3.clicked.connect(self.tp_image)
        button4.clicked.connect(self.clear_label)
        button5.clicked.connect(self.gray_image)
        button6.clicked.connect(self.blur_image)
        button7.clicked.connect(self.reverse_image)
        button8.clicked.connect(self.circle_image)
        button9.clicked.connect(self.convex_image)






        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)
        sidebar.addWidget(button5)
        sidebar.addWidget(button6)
        sidebar.addWidget(button7)
        sidebar.addWidget(button8)
        sidebar.addWidget(button9)

        







        main_layout.addLayout(sidebar)

        self.label1 = QLabel(self)
        self.label1.setFixedSize(640, 480)
        main_layout.addWidget(self.label1)

        self.label2 = QLabel(self)
        self.label2.setFixedSize(640, 480)
        main_layout.addWidget(self.label2)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


    
    def show_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image = cv2.imread(file_name[0])
        h, w, _ = self.image.shape
        bytes_per_line = 3 * w
        image = QImage(
            self.image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label1.setPixmap(pixmap)

    def flip_image(self):
        image = cv2.flip(self.image, 1)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(
            image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    def clear_label(self):
        self.label2.clear()


    def tp_image(self):
        image = cv2.flip(self.image, 0)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(
            image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    
    def gray_image(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        h, w = image.shape
        byte_per_line = 1 * w
        image = QImage(
            image.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

      
      
    def blur_image(self):
        image = cv2.medianBlur(self.image, 5)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)



    def reverse_image(self):
        image = cv2.bitwise_not(self.image)
        h, w, _ = image.shape
        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)


    def circle_image(self):
        image = self.image
        h, w = image.shape[:2]
        mask = np.zeros_like(image)
        cv2.circle(mask, (int(w/2), int(w/2)), int(w/2), (255, 255, 255), -1)
        image = cv2.bitwise_and(image, mask)
        bytes_per_line = 3 * w
        image = QImage(
            image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)




    def convex_image(self):
        image = self.image
        h, w = image.shape[:2]
        exp = 2
        scale = 1
        mapy, mapx = np.indices((h, w), dtype=np.float32)

        mapx = 2 * mapx / (w - 1) -1
        mapy = 2 * mapy / (h - 1) -1

        r, theta = cv2.cartToPolar(mapx, mapy) 
        r[r < scale] = r[r < scale] ** exp 

        mapx, mapy = cv2.polarToCart(r, theta) 
        mapx = ((mapx + 1) * w - 1) /2 
        mapy = ((mapy + 1) * h - 1) / 2 

        image = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR) 

        bytes_per_line = 3 * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)


        



if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
