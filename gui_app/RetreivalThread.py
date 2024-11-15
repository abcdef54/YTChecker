from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
from youtube_find.youtube_checker import YoutubeChecker
import requests


class RetrievalWorker(QThread):
    retreival_complete = pyqtSignal(dict, QPixmap)
    
    def __init__(self, yt_checker: YoutubeChecker, url: str ) -> None:
        super().__init__()
        
        self.yt_checker = yt_checker
        self.url = url
    
    def retrieve(self):
        try:
            # Retrieve information and thumbnail
            infomations = self.yt_checker.retrieve_infos(self.url)
            thumbnail_url = self.yt_checker.thumbnail()
            
            response = requests.get(thumbnail_url)
            response.raise_for_status()
            
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            # Emit the signal with retrieved data
            self.retrieval_complete.emit(infomations, pixmap)

        except Exception as e:
            print(f"Error retrieving data: {e}")