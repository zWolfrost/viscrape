import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PIL.ImageQt import ImageQt

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
from PyQt5.QtCore import QPoint, QRect, Qt

def getCoordsGUI(image):
   app = QApplication([])
   win = QMainWindow()

   class Window(QWidget):
      def __init__(self):
         super().__init__()

         self.setWindowTitle("Image Coordinates")

         self.begCS = 50
         self.endCS = 50

         self.setGeometry(0, 0, 1280 + self.begCS + self.endCS, 720 + self.begCS + self.endCS)
         self.setMinimumSize(500, 500)

         self.original_image = ImageQt(image)
         self.image = self.original_image.scaled(self.width() - (self.begCS+self.endCS), self.height() - (self.begCS+self.endCS), Qt.KeepAspectRatio)

         self.coords = QLabel("", self)
         self.coords.setFont(QFont("Arial", 20))
         self.coords.setTextInteractionFlags(Qt.TextSelectableByMouse)

         self.beg = QPoint(-2, -2)
         self.end = QPoint(-2, -2)


      def getCoords(self):
         ratio = self.original_image.width() / self.image.width()

         scrcrop = [self.beg.x(), self.beg.y(), self.end.x(), self.end.y()]

         if (scrcrop[0] > scrcrop[2]): scrcrop[0], scrcrop[2] = scrcrop[2], scrcrop[0]
         if (scrcrop[1] > scrcrop[3]): scrcrop[1], scrcrop[3] = scrcrop[3], scrcrop[1]

         imgcrop = []
         imgcrop.append( max( min(int((scrcrop[0]-self.begCS)*ratio), self.original_image.width()  ), 0) )
         imgcrop.append( max( min(int((scrcrop[1]-self.begCS)*ratio), self.original_image.height() ), 0) )
         imgcrop.append( max( min(int((scrcrop[2]-self.begCS)*ratio), self.original_image.width()  ), 0) )
         imgcrop.append( max( min(int((scrcrop[3]-self.begCS)*ratio), self.original_image.height() ), 0) )

         return imgcrop

      def updateCoords(self, text=None):
         if (text == None):
            coords = self.getCoords()
            text = f"({str(coords[0])}, {str(coords[1])}); ({str(coords[2])}, {str(coords[3])})"

         self.coords.setText(text)

         textwidth = self.coords.fontMetrics().boundingRect(self.coords.text()).width()

         self.coords.move(int((self.width() - textwidth) / 2), self.height() - self.endCS + 5)

         self.coords.adjustSize()


      def paintEvent(self, event):
         paint = QPainter(self)

         paint.drawImage(self.begCS, self.begCS, self.image)

         paint.setBrush(QBrush(QColor(100, 10, 10, 50)))

         paint.drawRect(QRect(QPoint(self.beg.x()-1, self.beg.y()-2), QPoint(self.end.x()-1, self.end.y()-2)))

      def mousePressEvent(self, event):
         self.end = event.pos()

         self.end.setX( max( min(self.end.x(), self.image.width()  + self.endCS    ), self.begCS) )
         self.end.setY( max( min(self.end.y(), self.image.height() + self.endCS + 1), self.begCS) )

         self.beg = self.end

         self.updateCoords()
         self.update()

      def mouseMoveEvent(self, event):
         self.end = event.pos()

         self.end.setX( max( min(self.end.x(), self.image.width()  + self.endCS    ), self.begCS) )
         self.end.setY( max( min(self.end.y(), self.image.height() + self.endCS + 1), self.begCS) )

         self.updateCoords()
         self.update()


      def resizeEvent(self, event):
         self.image = self.original_image.scaled(self.width() - (self.begCS + self.endCS), self.height() - (self.begCS + self.endCS), Qt.KeepAspectRatio)

         self.beg = QPoint(-2, -2)
         self.end = QPoint(-2, -2)

         self.updateCoords("Close this window to confirm")

         return super(Window, self).resizeEvent(event)

   win = Window()

   win.show()
   app.exec_()

   return win.getCoords()