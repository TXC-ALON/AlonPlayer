from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl



class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 1980, 1080)
        self.setWindowIcon(QIcon('player.png'))



        self.init_ui()


        self.show()


    def init_ui(self):

        #create media player object
        self.mediaPlayer1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object

        videowidget1 = QVideoWidget()
        videowidget2 = QVideoWidget()


        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        openBtn2 = QPushButton('Open Video')
        openBtn2.clicked.connect(self.open_file)

        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_video)

        self.playBtn2 = QPushButton()
        self.playBtn2.setEnabled(False)
        self.playBtn2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn2.clicked.connect(self.play_video)

        self.stopBtn2 = QPushButton()
        self.stopBtn2.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn2.clicked.connect(self.stop_video)



        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0,0)
        self.slider2.sliderMoved.connect(self.set_position)


        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)
        hboxLayout.addWidget(self.slider)

        hboxLayout2 = QHBoxLayout()
        hboxLayout2.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout2.addWidget(openBtn2)
        hboxLayout2.addWidget(self.playBtn2)
        hboxLayout2.addWidget(self.stopBtn2)
        hboxLayout2.addWidget(self.slider2)



        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget1)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout2 = QVBoxLayout()
        vboxLayout2.addWidget(videowidget2)
        vboxLayout2.addLayout(hboxLayout2)
        vboxLayout2.addWidget(self.label)

        hboxLayout = QHBoxLayout()
        hboxLayout.addLayout(vboxLayout)
        hboxLayout.addLayout(vboxLayout2)
        self.setLayout(hboxLayout)

        self.mediaPlayer1.setVideoOutput(videowidget1)
        self.mediaPlayer2.setVideoOutput(videowidget2)


        #media player signals

        self.mediaPlayer1.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer1.positionChanged.connect(self.position_changed)
        self.mediaPlayer1.durationChanged.connect(self.duration_changed)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer1.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaPlayer2.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer1.pause()
            self.mediaPlayer2.pause()

        else:
            self.mediaPlayer1.play()
            self.mediaPlayer2.play()

    def stop_video(self):
        self.mediaPlayer1.stop()
        self.slider.setValue(0)

    def mediastate_changed(self, state):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer1.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer1.errorString())





app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())