from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import sys
import re
import logging


from gui_app.app_button_handler import AppButtonHandler
import youtube_find.constant as CONST

youtube_logger = logging.getLogger('youtube_find.youtube_checker')

class YoutubeCheckerApp(QWidget):
    def __init__(self, webdirver_path: str = CONST.webdriver_path) -> None:
        super().__init__()
        
        self.button_handler = AppButtonHandler(self, webdirver_path)
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
        self.set_style()
    
    
    def create_window_variables(self) -> None:
        # Create the search box for URL input
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Enter URL')
        self.search_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_box.returnPressed.connect(self.button_pressed)
        
        
        self.retrive_button = QPushButton('Retrieve Info', self)
        self.clear_button = QPushButton('Clear', self)
        self.pause_button = QPushButton('Pause Video', self)
        self.forward_button = QPushButton('Forward', self)
        self.back_button = QPushButton('Back', self)
        self.refresh_button = QPushButton('Refresh', self)
        self.like_button = QPushButton('Like/Undo', self)
        self.dislike_button = QPushButton('Dislike/Undo', self)
        self.sub_button = QPushButton('Sub/Unsub', self)
        self.comment_button = QPushButton('Commnet', self)
        self.next_video_button = QPushButton('Next Video', self)
        
        
        # action buttons
        self.action_buttons = [
            self.retrive_button, self.clear_button, self.pause_button, self.forward_button, self.back_button, self.refresh_button, self.like_button,
            self.dislike_button, self.sub_button, self.comment_button, self.next_video_button
        ]
        
        # Connect all action buttons to action_buttons_pressed
        for button in self.action_buttons:
            button.clicked.connect(self.button_pressed)
            if button not in (self.retrive_button, self.clear_button):
                button.setDisabled(True)
            
        self.thumbnail_url_label = QLabel(self)
        # Set pixmap for a label
        youtube_logo = QPixmap('items/youtube_3256012.png')
        self.youtube_logo_label = QLabel(self)
        self.youtube_logo_label.setPixmap(youtube_logo)
        self.youtube_logo_label.setScaledContents(True)
        self.youtube_logo_label.setFixedSize(75, 75)
            
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        
        
        label_buttons = [
            'None', 'General Infos', 'Title', 'Video Length', 'View Count', 'Like Count', 'Sub Count', 'Comment Count', 'Upload Date',
            'Description', 'Video URL', 'Thumbnail URL', 'Family Friendly', 'Video Genre', 'KeyWords', 'Allowed Regions', 'Banned Regions',
        ]
        
        # Create list widget for label buttons
        self.label_button_list = QListWidget(self)
        self.label_button_list.addItems(label_buttons)
        self.label_button_list.clicked.connect(self.button_pressed)
        self.label_button_list.setDisabled(True)

    
    def set_layout(self) -> None:
        master_layout = QVBoxLayout()

        # Top part of the main window
        top_half = QHBoxLayout()  # Add layout directly to this widget
        top_half.addWidget(self.youtube_logo_label, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_half.addWidget(self.thumbnail_url_label, 8)
        
        
        # Middle part of the main window
        middle_master = QHBoxLayout()
        middle_master.addWidget(self.back_button, 1)
        middle_master.addWidget(self.refresh_button, 1)
        middle_master.addWidget(self.search_box, 7)
        middle_master.addWidget(self.forward_button, 1)
        middle_master.setContentsMargins(0, 15, 0, 15)
        
        
        # Bottom part of the main window
        bottom_half = QHBoxLayout()
        
        # Middle part of the bottom half
        middle_bottom_half = QVBoxLayout()
        middle_bottom_half.addWidget(self.text_area)
        middle_bottom_half.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # Left part of the bottom half
        left_side_bottom_half = QVBoxLayout()
        left_side_bottom_half.addWidget(self.label_button_list)

        
        # Right part of the bottom half
        right_side_bottom_half = QVBoxLayout()
        for button in self.action_buttons:
            if button not in (self.back_button, self.forward_button, self.refresh_button):
                right_side_bottom_half.addWidget(button)
     

        
        bottom_half.addLayout(left_side_bottom_half, 2)
        bottom_half.addLayout(middle_bottom_half,7)
        bottom_half.addLayout(right_side_bottom_half,1)

        # Add the bottom layout to the main layout
        master_layout.addLayout(top_half, 2)
        master_layout.addLayout(middle_master, 2)
        master_layout.addLayout(bottom_half, 6)

        # Set the layout of the window
        self.setLayout(master_layout)
    
    
    def set_style(self) -> None:
        self.clear_button.setObjectName('ClearButton')
        self.retrive_button.setObjectName('RetreiveButton')
        
        self.setStyleSheet("""
                           QWidgets{
                               background-color: #262625;
                           }
                           
                           QPushButton{
                               background-color: #333230;
                               padding: 2px;
                               color: #dbd9d9;
                               font-weight: bold;
                               font-size: 12px;
                               border-radius: 4px;
                           }
                           
                           QPushButton:hover{
                               background-color: #7a7a7a;
                           }
                           
                           QPushButton:pressed{
                               background-color: #4a4a4a;
                           }
                           
                           QPushButton#ClearButton{
                               background-color: #8a3511;
                               color: #bfbfbf;
                           }
                           
                           QPushButton#ClearButton:hover{
                               background-color: #a1351d;
                           }
                           
                           QPushButton#RetreiveButton{
                               background-color: #a68221;
                               color: #bfbfbf;
                           }
                           
                           QPushButton#RetreiveButton:hover{
                               background-color: #c79306;
                           }
                           
                           QLineEdit{
                               background-color: #dbd9d9;
                               color: #1a1919;
                               font-weight: bold;
                               font-size: 12px;
                               border-radius: 3px;
                           }
                           
                           
                           QListWidget{
                               background-color: #dbd9d9;
                               color: #1a1919;
                               font-weight: bold;
                               font-size: 12px;
                               border-radius: 2px;
                           }
                           
                           QListWidget::item:selected{
                                background-color: #292828;
                                color: white;
                                border: 1px solid #a8a7a7;
                           }
                           
                           QTextEdit{
                               background-color: #302e2e;
                               color: #dbd9d9;
                               font-weight: bold;
                               border-radius: 8px;
                               margin-left: 7px;
                               margin-right: 7px;
                           }
                           """)
    

    def button_pressed(self) -> None:
        sender = self.sender()
        self.button_handler.button_pressed(sender)
            
    
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
        
    @staticmethod
    def format_url(url: str) -> str:
        pass
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    youtube = YoutubeCheckerApp()
    youtube.show()
    sys.exit(app.exec())