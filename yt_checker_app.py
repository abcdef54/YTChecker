from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import sys
import re
import requests
import time


from youtube_find.youtube_checker import YoutubeChecker
import youtube_find.constant as CONST
from RetreivalThread import RetrievalWorker

class YoutubeCheckerApp(QWidget):
    def __init__(self, webdirver_path: str = CONST.webdriver_path) -> None:
        super().__init__()
        
        self.yt_checker = YoutubeChecker(webdirver_path, auto_closing=True)
        self.current_url = None
        self.infomations = {}

        self.main_window_settings()
        self.initGUI()
    
    def main_window_settings(self) -> None:
        self.setWindowTitle('Youtube Checker')
        self.setGeometry(380, 160, 900, 500)
        self.setWindowIcon(QIcon('items/youtube_3256012.png'))
    
    
    def initGUI(self) -> None:
        self.create_window_variables()
        self.set_layout()
    
    
    def create_window_variables(self) -> None:
        # Create the search box for URL input
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Enter URL')
        self.search_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_box.returnPressed.connect(self.retrive_button_clicked)
        
        
        self.retrive_button = QPushButton('Retrieve Info', self)
        self.clear_button = QPushButton('Clear', self)
        self.forward_button = QPushButton('Forward', self)
        self.back_button = QPushButton('Back', self)
        self.refresh_button = QPushButton('Refresh', self)
        self.like_button = QPushButton('Like/Undo', self)
        self.dislike_button = QPushButton('Dislike/Undo', self)
        self.sub_button = QPushButton('Sub/Unsub', self)
        self.comment_button = QPushButton('Commnet', self)
        
        
        # action buttons
        self.action_buttons = {
            self.forward_button : self.yt_checker.actions.forward(),
            self.back_button : self.yt_checker.actions.go_back(),
            self.refresh_button : self.yt_checker.actions.refresh(),
            self.like_button : self.yt_checker.actions.like(),
            self.dislike_button : self.yt_checker.actions.dislike(),
            self.sub_button : self.yt_checker.actions.sub()
        }
        
        # Connect all action buttons to action_buttons_pressed
        for button in self.action_buttons:
            button.clicked.connect(self.button_pressed)
            button.setDisabled(True)
            
        """
        # Labels for the retrieved infomations
        self.title_label = QLabel('Title: ', self)
        self.video_length_label = QLabel('Video Length: ', self)
        self.view_label = QLabel('View Count: ', self)
        self.like_label = QLabel('Like Count: ', self)
        self.sub_count_label = QLabel('Sub Count: ', self)
        self.comment_count_label = QLabel('Comment Count: ', self)
        self.video_date_label = QLabel('Upload Date: ', self)
        self.description_label = QLabel('Description: ', self)
        self.video_url_label = QLabel('Video URL: ', self)
        self.thumbnail_url_label = QLabel(self)
        self.family_friendly_label = QLabel('Is Family Friendly: ', self)
        self.video_genre_label = QLabel('Video Genre: ', self)
        self.allowed_regions_label = QLabel('Regions Allowed: ', self)
        self.banned_regions_label = QLabel('Banned Regions: ', self)
        """
        
        # Set pixmap for a label
        youtube_logo = QPixmap('items/youtube_3256012.png')
        self.youtube_logo_label = QLabel(self)
        self.youtube_logo_label.setPixmap(youtube_logo)
        self.youtube_logo_label.setScaledContents(True)
        self.youtube_logo_label.setFixedSize(75, 75)
        
        # All labels in the class
        self.labels = [
            self.title_label, self.video_length_label, self.view_label, self.like_label, self.sub_count_label, self.comment_count_label,
            self.video_date_label, self.description_label, self.video_url_label, self.thumbnail_url_label, self.family_friendly_label,
            self.video_genre_label, self.allowed_regions_label, self.banned_regions_label, self.youtube_logo_label
        ]
        
        for label in self.labels:
            if label in (self.youtube_logo_label, self.thumbnail_url_label):
                continue
            label.hide()
            
            
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.hide()
        
        
        
        label_buttons = [
            'None', 'General Infos', 'Title', 'Video Length', 'View Count', 'Like Count', 'Sub Count', 'Comment Count', 'Upload Date',
            'Description', 'Video URL', 'Thumbnail URL', 'Family Friendly', 'Video Genre', 'KeyWords', 'Allowed Regions', 'Banned Regions',
        ]
        
        # Create list widget for label buttons
        self.label_button_list = QListWidget(self)
        self.label_button_list.addItems(label_buttons)
        self.label_button_list.clicked.connect(self.list_widget_button_clicked)
        self.label_button_list.setDisabled(True)

    
    def set_layout(self) -> None:
        master_layout = QVBoxLayout()

        # Top part of the main window
        top_half = QHBoxLayout()
        top_half.addWidget(self.youtube_logo_label, 2)
        top_half.addWidget(self.thumbnail_url_label, 8)
        
        
        # Middle part of the main window
        middle_master = QHBoxLayout()
        middle_master.addWidget(self.back_button, 1)
        middle_master.addWidget(self.refresh_button, 1)
        middle_master.addWidget(self.search_box, 6)
        middle_master.addWidget(self.forward_button, 1)
        middle_master.setContentsMargins(0, 30, 0, 30)
        
        
        # Bottom part of the main window
        bottom_half = QHBoxLayout()
        
        # Middle part of the bottom half
        middle_bottom_half = QVBoxLayout()
        middle_bottom_half.addWidget(self.text_area)
        for label in self.labels:
            if label == self.youtube_logo_label:
                continue
            middle_bottom_half.addWidget(label)
        middle_bottom_half.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # Left part of the bottom half
        left_side_bottom_half = QVBoxLayout()
        left_side_bottom_half.addWidget(self.label_button_list)

        
        # Right part of the bottom half
        right_side_bottom_half = QVBoxLayout()
        for button in self.action_buttons.keys():
            if button in (self.back_button, self.forward_button, self.refresh_button):
                continue
            else:
                right_side_bottom_half.addWidget(button)


        
        bottom_half.addLayout(left_side_bottom_half, 2)
        bottom_half.addLayout(middle_bottom_half,6)
        bottom_half.addLayout(right_side_bottom_half), 2

        # Add the bottom layout to the main layout
        master_layout.addLayout(top_half, 3)
        master_layout.addLayout(middle_master, 2)
        master_layout.addLayout(bottom_half, 5)

        # Set the layout of the window
        self.setLayout(master_layout)
    

    def button_pressed(self) -> None:
        sender = self.sender()
        
        if sender == self.retrive_button:
            self.retrive_button_clicked()
        
        elif sender == self.clear_button:
            self.search_box.clear()
            self.current_url = None
            
        elif sender in self.actions.keys():
            self.action_buttons.get(sender)


    def list_widget_button_clicked(self) -> None:
        current_item = self.label_button_list.currentItem()
        sender_text = current_item.text() if current_item else None
        
        keys = [
            'Title', 'Video Length', 'View Count', 'Like Count', 'Sub Count', 'Comment Count', 'Upload Date',
            'Description', 'Video URL', 'Thumbnail URL', 'Family Friendly', 'Video Genre', 'KeyWords', 'Allowed Regions', 'Banned Regions',
        ]
        
        if sender_text == 'None':
            self.text_area.hide()
            self.text_area.clear()
            
        elif sender_text == 'General Infos':
            pass
            
        elif sender_text in keys:
            self.text_area.setText(f'{sender_text}: {self.infomations.get(sender_text, 'Error retreiving this infomation :(')}')
        
        self.text_area.show()
        
    
    
    def retrive_button_clicked(self) -> None:
        url = self.search_box.text()
        if url == self.current_url:
            return
    
        # Validate URL
        if not self.is_valid_url(url):
            print("Invalid URL")  # For debugging purposes
            return

        # Attempt to open URL and retrieve information
        
        try:
            self.text_area.show()
            self.text_area.setText('Waiting For Program To Retrive Infomations\nPlease Be Pacient!')
            
            self.current_url = url
            self.retrive_button.setDisabled(True)
            self.infomations = self.yt_checker.retrieve_infos(self.current_url)
            
            
            thumbnail = self.yt_checker.thumbnail()
            response = requests.get(thumbnail)
            response.raise_for_status()
            
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            
            self.thumbnail_url_label.setPixmap(pixmap)
            self.thumbnail_url_label.setScaledContents(True)
            self.thumbnail_url_label.setFixedSize(250, 80)
            self.thumbnail_url_label.show()
            
            
            for button in self.action_buttons:
                button.setEnabled(True)
            self.label_button_list.setEnabled(True)
            
            self.text_area.setText('Infomations Retrieved!')
            self.retrive_button.setEnabled(True)
            
        except Exception as e:
            print(f"Error retrieving data: {e}")
        
    
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
    

    @staticmethod
    def is_valid_url(url: str) -> bool:
        if not url:
            return False
        
        pattern = r'^(?:https?://(?:www\.)?youtube\.com/watch\?v=)?([a-zA-Z0-9_-]{11})$'
        match = re.match(pattern, url)
        return bool(match)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    youtube = YoutubeCheckerApp()
    youtube.show()
    sys.exit(app.exec())