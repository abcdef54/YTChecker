from gui_app.yt_checker_app import YoutubeCheckerApp
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
youtube = YoutubeCheckerApp()
youtube.show()
sys.exit(app.exec())