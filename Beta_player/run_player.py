
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from doublePlayer import Ui_MainWindow
from playerlib import Video


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 使用转换的UI文件中的类来设置UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mediaPlayer1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.ui.PB_OpenFile_1.clicked.connect(self.open_file)
        self.ui.PB_Play_Pause_1.clicked.connect(self.play_video)
        self.ui.PB_Next_1.clicked.connect(self.stop_video)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        print(filename)
        if filename != '':
            video = Video(filename)
            video.print_video_simple()
            self.mediaPlayer1.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
    def play_video(self):
        print("按下播放")
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer1.pause()

        else:
            self.mediaPlayer1.play()

    def stop_video(self):
        self.mediaPlayer1.stop()

    def media_state_changed(self, state):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            print("正在播放")

        else:
            print("暂停")

    def position_changed(self, position):
        print("position is {}".format(position))


    def duration_changed(self, duration):
        print("duration is {}".format(duration))

if __name__ == '__main__':
    # 创建一个应用程序对象
    app = QApplication([])
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 启动应用程序的事件循环
    app.exec_()

