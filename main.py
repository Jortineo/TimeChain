from PySide6.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QHBoxLayout, QWidget, QPushButton, QLabel, QTimeEdit
from PySide6.QtCore import QTimer, Qt, QTime, QUrl
from PySide6.QtMultimedia import QSoundEffect

import sys

class customTimer(QWidget):
    def __init__(self, ventana):
        super().__init__()

        self.ventana = ventana

        self.setMaximumHeight(100)
        self.setMinimumHeight(100)

        self.timer_label = QLabel("Timer")

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)

        self.time_input = QTimeEdit()
        self.time_input.timeChanged.connect(self.change_time)
        self.time_input.setTime(QTime(0, 0, 0, 0)) #set it to 0
        self.time_input.setDisplayFormat("mm:ss") #set it to minutes, seconds instead of hours, minutes

        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setSource(QUrl.fromLocalFile("Beep.wav"))
        self.sound_effect.setVolume(0.8) #from 0.0 to 1.0

        self.time_label = QLabel(str(self.timer.remainingTime()))

        self.update_timer = QTimer() #hidden, to manage updating the visuals every 100ms
        self.update_timer.setInterval(100)
        self.update_timer.timeout.connect(self.update_visuals)
        self.update_timer.start()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.timer_label)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)

        self.setLayout(self.main_layout)

    def on_timeout(self):
        self.timer.stop()
        self.time_label.setText("0")

        self.sound_effect.play()

        try:
            self.ventana.finish_timer()
        except Exception as error:
            print(f"Error: {error}")

    def update_visuals(self):
        if self.timer.isActive():
            self.time_label.setText(str(self.timer.remainingTime() / 1000)) #seconds

        self.update_timer.start()

    def change_time(self, new_value: QTime):
        self.timer.setInterval((int(new_value.minute() * 60) + int(new_value.second())) * 1000) #receive in minutes * 60 and seconds, *1000 for total ms

        print(f"Time changed to: {new_value}s")

    def start_timer(self):
        self.timer.start()
        print("timer started")

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TimebyBlock")

        self.setMinimumSize(600, 500)
        self.resize(800, 600) #width, height

        self.timer_index = 0

        #main layouts
        vert_layout = QVBoxLayout() #main vertical layout
        button_layout = QHBoxLayout() #main layout for buttons

        #buttons
        new_timer_button = QPushButton("Create new timer")
        new_timer_button.setMaximumSize(400, 100)
        new_timer_button.clicked.connect(self.create_timer)

        delete_timer_button = QPushButton("Delete timer")
        delete_timer_button.setMaximumSize(400, 100)

        start_block_button = QPushButton("Start block")
        start_block_button.setMaximumSize(400, 100)
        start_block_button.clicked.connect(self.start_block)

        button_layout.addWidget(start_block_button)
        button_layout.addWidget(new_timer_button)
        button_layout.addWidget(delete_timer_button)

        # main widget
        main_widget = QWidget()
        main_widget.setLayout(vert_layout)
        self.setCentralWidget(main_widget)

        #timers
        self.timer_layout = QVBoxLayout()
        timer_widget = QWidget()
        timer_widget.setLayout(self.timer_layout)
    
        # adding everything
        vert_layout.addLayout(button_layout)
        vert_layout.addWidget(timer_widget)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop) #put it on top

    def create_timer(self):
        timer = customTimer(self)

        self.timer_layout.addWidget(timer)
        print("timer added")

    def start_block(self):
        if self.timer_index >= self.timer_layout.count():
            self.timer_index = 0

        timer = self.timer_layout.itemAt(self.timer_index).widget()

        if isinstance(timer, customTimer): # if it is a custom timer
            timer.start_timer()

    def finish_timer(self):
        print(f"timer {self.timer_index} finished")

        self.timer_index += 1

        self.start_block()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = mainwindow()
    ventana.show()
    sys.exit(app.exec())