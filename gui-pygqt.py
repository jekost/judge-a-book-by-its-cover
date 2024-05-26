import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget, QSpacerItem, QSizePolicy, QProgressBar, QLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PIL import Image
import tensorflow as tf
import numpy as np


class ImageProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.model = self.load_model()
        self.layout = QVBoxLayout()

        self.layout.setSpacing(30)  # Vahe komponentide vahel



        # Spacer enne kõiki komponente
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Sisemine paigutus, mis sisaldab kõiki komponente
        inner_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(self.image_label)
        

        # Horisontaalne paigutus tekstide jaoks
        self.prog_layout1 = QHBoxLayout()
        self.prog_layout2 = QHBoxLayout()
        self.prog_layout3 = QHBoxLayout()
        
        self.prog_layout1.addStretch()
        self.prog_layout2.addStretch()
        self.prog_layout3.addStretch()



        
        
        self.label1 = QLabel("")
        self.label1.setAlignment(Qt.AlignCenter)
        self.prog_layout1.addWidget(self.label1)
        
        self.progress_bar1 = QProgressBar()
        self.progress_bar1.setAlignment(Qt.AlignCenter)
        self.progress_bar1.setStyleSheet("QProgressBar::chunk { background-color: rgba(255, 255, 0, 0.8); border: 1px solid gray; border-top-right-radius: 3px; border-bottom-right-radius: 3px; } QProgressBar {border: 1px solid gray; border-radius: 3px;}")
        self.prog_layout1.addWidget(self.progress_bar1)

        self.label2 = QLabel("")
        self.label2.setAlignment(Qt.AlignCenter)
        self.prog_layout2.addWidget(self.label2)
        
        self.progress_bar2 = QProgressBar()
        self.progress_bar2.setAlignment(Qt.AlignCenter)
        self.progress_bar2.setStyleSheet("QProgressBar::chunk { background-color: rgba(255, 0, 0, 0.8); border: 1px solid gray; border-top-right-radius: 3px; border-bottom-right-radius: 3px; } QProgressBar {border: 1px solid gray; border-radius: 3px;}")
        self.prog_layout2.addWidget(self.progress_bar2)

        self.label3 = QLabel("")
        self.label3.setAlignment(Qt.AlignCenter)
        self.prog_layout3.addWidget(self.label3)
        
        self.progress_bar3 = QProgressBar()
        self.progress_bar3.setAlignment(Qt.AlignCenter)
        self.progress_bar3.setStyleSheet("QProgressBar::chunk { background-color: rgba(0, 255, 0, 0.8); border: 1px solid gray; border-top-right-radius: 3px; border-bottom-right-radius: 3px; } QProgressBar {border: 1px solid gray; border-radius: 3px;}")
        self.prog_layout3.addWidget(self.progress_bar3)
        
        width = 80
        height= 20
        
        self.label1.setFixedSize(width, height)
        self.label2.setFixedSize(width, height)
        self.label3.setFixedSize(width, height)

        
        self.progress_bar1.hide()
        self.progress_bar2.hide()
        self.progress_bar3.hide()

        self.prog_layout1.addStretch()
        self.prog_layout2.addStretch()
        self.prog_layout3.addStretch()


        # Lisame horisontaalse paigutuse sisemisse paigutusse
        inner_layout.addLayout(self.prog_layout1)
        inner_layout.addLayout(self.prog_layout2)
        inner_layout.addLayout(self.prog_layout3)




        self.button = QPushButton("Ava pilt")
        self.button.setStyleSheet("border: 1px solid gray; border-radius: 2px; padding: 2px;")
        self.button.clicked.connect(self.open_image)
        inner_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        effect4 = QGraphicsDropShadowEffect()
        effect4.setBlurRadius(4)
        effect4.setColor(QColor('gray'))
        effect4.setOffset(3)
        self.button.setGraphicsEffect(effect4)

        self.question_button = QPushButton("?")
        self.question_button.clicked.connect(self.show_dialog)
        self.question_button.setMaximumSize(30, 30)  # Maksimaalne suurus küsimärgiga nupule
        self.question_button.setToolTip("Abi")  # Kuvab tööriistaipundi
        self.question_button.setStyleSheet("QPushButton { font-size: 18px; }")  # Nupu stiil
        inner_layout.addWidget(self.question_button, alignment=Qt.AlignRight)

        # Lisa sisemine paigutus
        self.layout.addLayout(inner_layout)

        # Spacer pärast kõiki komponente
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)
        self.setWindowTitle("Hinda raamatut kaane järgi")

    def load_model(self):
        # Asendage see funktsioon vastavalt teie mudeli laadimisele
        model = tf.keras.models.load_model('face_ratings_model.h5')
        return model
    
    
    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        
        #image = image.crop(coords_for_crop(image_path))
        image = image.resize((600, 600))  # Ensure the image is 600x600 pixels
        image.show()
        image = np.array(image) / 255.0  # Normalize the image
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        return image

    def ennusta(self, image_path):

        # Preprocess the image
        preprocessed_image = self.preprocess_image(image_path)
        
        # Predict the ratings
        predicted_ratings = self.model.predict(preprocessed_image)

        # Print the predicted ratings
        return predicted_ratings[0]



    def show_dialog(self):
        # Hüpikakna kuvamine
        QMessageBox.information(self, "Abi", "See tehisintellekt on õpetatud hindama inimesi nii, kuidas teised neid näeks.")

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Vali pilt", "", "Image Files (*.jpg *.jpeg *.png)", options=options)
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            image.save("thumbnail.png")

            pixmap = QPixmap("thumbnail.png")
            self.image_label.setPixmap(pixmap)


            vals = self.ennusta(file_path)
            
            self.button.setText("Vali uus pilt")
            
            self.label1.setText("Intelligents:")
            self.label2.setText("Ilu:")
            self.label3.setText("Usaldusväärsus:")

            self.progress_bar1.setValue(int(vals[2]*10))
            self.progress_bar2.setValue(int(vals[1]*10))
            self.progress_bar3.setValue(int(vals[0]*10))

            # Näita progressbare pärast töötlemist
            self.progress_bar1.show()
            self.progress_bar2.show()
            self.progress_bar3.show()

            # Lisa varjuefekt ja animatsioonid pärast progressbaride näitamist
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(5)
            effect.setColor(QColor('gray'))
            effect.setOffset(3)
            effect2 = QGraphicsDropShadowEffect()
            effect2.setBlurRadius(5)
            effect2.setColor(QColor('gray'))
            effect2.setOffset(3)
            effect3 = QGraphicsDropShadowEffect()
            effect3.setBlurRadius(5)
            effect3.setColor(QColor('gray'))
            effect3.setOffset(3)
            

            self.progress_bar1.setGraphicsEffect(effect)
            self.progress_bar2.setGraphicsEffect(effect2)
            self.progress_bar3.setGraphicsEffect(effect3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessorApp()
    ex.resize(800, 600)
    ex.show()
    sys.exit(app.exec_())
