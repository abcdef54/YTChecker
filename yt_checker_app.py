from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt
import sys
import os
os.system('cls')

from youtube_find.youtube_checker import YoutubeChecker
import youtube_find.constant as CONST

class YoutubeCheckerApp(QWidget):
    def __init__(self, webdirver_path: str = CONST.webdriver_path) -> None:
        super().__init__()
        
        self.yt_checker = YoutubeChecker(webdirver_path, auto_closing=True)

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
        
        
        self.retrive_button = QPushButton('Retrieve Info', self)
        self.clear_button = QPushButton('Clear', self)
        self.forward_button = QPushButton('Forward', self)
        self.back_button = QPushButton('Back', self)
        self.refresh_button = QPushButton('Refresh', self)
        self.like_button = QPushButton('Like/Undo', self)
        self.dislike_button = QPushButton('Dislike/Undo', self)
        self.sub_button = QPushButton('Sub/Unsub', self)
        self.comment_button = QPushButton('Commnet', self)
        
        # All action buttons
        self.action_buttons = [
            self.retrive_button, self.clear_button, self.forward_button, self.back_button, self.refresh_button,
            self.like_button, self.dislike_button, self.sub_button, self.comment_button
        ]
        
        # Connect all action buttons to action_buttons_pressed
        for button in self.action_buttons:
            button.clicked.connect(self.action_buttons_pressed)
            
        
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
        self.thumbnail_url_label = QLabel('Thumbnail URL: ', self)
        self.family_friendly_label = QLabel('Is Family Friendly: ', self)
        self.video_genre_label = QLabel('Video Genre: ', self)
        self.allowed_regions_label = QLabel('Regions Allowed: ', self)
        self.banned_regions_label = QLabel('Banned Regions: ', self)
        
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
            if label == self.youtube_logo_label:
                continue
            label.hide()
        
        
        label_buttons = [
            'None', 'General Infos', 'Title', 'Video Length', 'View Count', 'Like Count', 'Sub Count', 'Comment Count', 'Upload Date',
            'Description', 'Video URL', 'Thumbnail URL', 'Family Friendly', 'Video Genre', 'Allowed Regions', 'Banned Regions',
        ]
        
        # Create list widget for label buttons
        self.label_button_list = QListWidget(self)
        self.label_button_list.addItems(label_buttons)
            

    
    def set_layout(self) -> None:
        master_layout = QVBoxLayout()

        # Top part of the main window
        top_half = QHBoxLayout()
        top_half.addWidget(self.youtube_logo_label)
        top_half.addWidget(self.refresh_button)
        top_half.addWidget(self.retrive_button)
        
        
        # Middle part of the main window
        middle_master = QHBoxLayout()
        middle_master.addWidget(self.back_button)
        middle_master.addWidget(self.search_box)
        middle_master.addWidget(self.forward_button)
        middle_master.setContentsMargins(0, 30, 0, 30)
        
        
        # Bottom part of the main window
        bottom_half = QHBoxLayout()
        
        # Middle part of the bottom half
        middle_bottom_half = QVBoxLayout()
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
        for button in self.action_buttons:
            if button in (self.retrive_button, self.back_button, self.forward_button, self.refresh_button):
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
        pass
    
    
    def action_buttons_pressed(self) -> None:
        pass
    
    
    def label_buttons_pressed(self) -> None:
        pass
    
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    youtube = YoutubeCheckerApp()
    youtube.show()
    sys.exit(app.exec())