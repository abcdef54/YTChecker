import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from youtube_find.yt_action import YTAction
from youtube_find.youtube_checker import YoutubeChecker  # Assuming this is your YoutubeChecker class
import youtube_find.constant as CONST

class YouTubeGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("YouTube Interaction")
        self.setGeometry(100, 100, 400, 300)

        # Set up the web driver (this can be set up properly elsewhere in your code)
        self.youtube_checker = YoutubeChecker(CONST.webdriver_path)
        self.yt_action = YTAction(self.youtube_checker)
        

        # Set up UI components
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # URL input field
        self.url_field = QLineEdit(self)
        self.url_field.setPlaceholderText("Enter YouTube video URL")
        layout.addWidget(self.url_field)

        # Button to retrieve video info
        self.info_button = QPushButton("Get Video Info", self)
        self.info_button.clicked.connect(self.get_video_info)
        layout.addWidget(self.info_button)

        # Video Info Display
        self.info_label = QLabel("Video Info: Not loaded", self)
        layout.addWidget(self.info_label)

        # Like/Dislike buttons
        button_layout = QHBoxLayout()

        self.like_button = QPushButton("Like Video", self)
        self.like_button.clicked.connect(self.like_video)
        button_layout.addWidget(self.like_button)

        self.dislike_button = QPushButton("Dislike Video", self)
        self.dislike_button.clicked.connect(self.dislike_video)
        button_layout.addWidget(self.dislike_button)

        layout.addLayout(button_layout)

        # Comment button
        self.comment_button = QPushButton("Comment on Video", self)
        self.comment_button.clicked.connect(self.comment_video)
        layout.addWidget(self.comment_button)

        # Status label
        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        # Set the layout
        self.setLayout(layout)

    def get_video_info(self):
        url = self.url_field.text()
        if url:
            # Retrieve video info using YoutubeChecker
            video_info = self.youtube_checker.retrieve_infos(url)
            if video_info:
                self.info_label.setText(f"Video Info: {video_info.get('Title')}")
                self.status_label.setText("Status: Video info retrieved.")
            else:
                self.status_label.setText("Status: Failed to retrieve video info.")
        else:
            self.status_label.setText("Status: Please enter a valid URL.")

    def like_video(self):
        url = self.url_field.text()
        if url:
            self.yt_action.open_video(url)
            success = self.yt_action.like()
            if success:
                self.status_label.setText("Status: Video liked.")
            else:
                self.status_label.setText("Status: Already liked or failed.")
        else:
            self.status_label.setText("Status: Please enter a valid URL.")

    def dislike_video(self):
        url = self.url_field.text()
        if url:
            self.yt_action.open_video(url)
            success = self.yt_action.dislike()
            if success:
                self.status_label.setText("Status: Video disliked.")
            else:
                self.status_label.setText("Status: Already disliked or failed.")
        else:
            self.status_label.setText("Status: Please enter a valid URL.")

    def comment_video(self):
        url = self.url_field.text()
        if url:
            self.yt_action.open_video(url)
            comment_text = "Great video!"  # You can make this dynamic by allowing user input for comments
            success = self.yt_action.comment(comment_text)
            if success:
                self.status_label.setText("Status: Comment posted.")
            else:
                self.status_label.setText("Status: Failed to post comment.")
        else:
            self.status_label.setText("Status: Please enter a valid URL.")

    def closeEvent(self, event):
        """Clean up the webdriver when closing the application"""
        self.driver.quit()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeGUI()
    window.show()
    sys.exit(app.exec())
