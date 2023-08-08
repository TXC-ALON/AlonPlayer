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
        self.setGeometry(350, 100, 800, 600)
        self.setWindowIcon(QIcon('player.png'))

        self.init_ui()

        self.show()

    def init_ui(self):

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object

        videowidget1 = QVideoWidget()

        # create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_video)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)
        hboxLayout.addWidget(self.slider)

        # create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget1)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        hboxLayout = QHBoxLayout()
        hboxLayout.addLayout(vboxLayout)

        self.setLayout(hboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget1)

        # media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()


        else:
            self.mediaPlayer.play()

    def stop_video(self):
        self.mediaPlayer.stop()
        self.slider.setValue(0)

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
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
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.window2 = None
        self.window1 = None
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 1980, 1080)
        self.setWindowIcon(QIcon('player.png'))

        self.init_ui()

        self.show()
    def init_ui(self):
        # 创建第一个窗口

        # 创建第二个窗口
        self.window1 = Window()
        self.window2 = Window()
        self.window1.show()
        self.window2.show()

        pushB_Play_All = QPushButton()
        pushB_Play_All.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        pushB_Play_All.clicked.connect(self.play_all)
        pushB_Stop_All = QPushButton()
        pushB_Play_All.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        pushB_Play_All.clicked.connect(self.stop_all)
        pushB_reset_toa = QPushButton()
        pushB_Play_All.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        pushB_Play_All.clicked.connect(self.reset_to_a)
        hbox_PB = QHBoxLayout()
        hbox_PB.addWidget(pushB_Play_All)
        hbox_PB.addWidget(pushB_reset_toa)
        hbox_PB.addWidget(pushB_Stop_All)

        # 创建水平布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.window1)
        hbox.addWidget(self.window2)
        hbox.addLayout(hbox_PB)

        # 创建并显示主窗口
        main_window = QWidget()
        main_window.setLayout(hbox)

    def play_all(self):
        if (self.window1.mediaPlayer.state() == QMediaPlayer.PlayingState) or (self.window2.mediaPlayer.state() == QMediaPlayer.PlayingState)  :
            self.window1.mediaPlayer.pause()
            self.window2.mediaPlayer.pause()

        else:
            self.window1.mediaPlayer.play()
            self.window2.mediaPlayer.play()

    def stop_all(self):
        self.window1.mediaPlayer.stop()
        self.window1.slider.setValue(0)
        self.window2.mediaPlayer.stop()
        self.window2.slider.setValue(0)

    def reset_to_a(self):
        self.window1.mediaPlayer.pause()
        self.window2.mediaPlayer.pause()
        self.window2.mediaPlayer.setPosition()
        self.window2.slider.setValue(self.window1.slider.value())
        self.window1.mediaPlayer.setPosition(self.window2.slider.value())


def appshow():
    app = QApplication(sys.argv)

    # 创建第一个窗口
    window = MainWindow()

    sys.exit(app.exec_())
if __name__ == '__main__':
    appshow()
