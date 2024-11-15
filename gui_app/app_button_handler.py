from PyQt6.QtGui import QPixmap
import requests
import logging
from youtube_find.youtube_checker import YoutubeChecker

youtube_logger = logging.getLogger('youtube_find.youtube_checker')


class AppButtonHandler:
    def __init__(self, parent, webdriver_path: str) -> None:
        self.app = parent
        self.yt_checker = YoutubeChecker(webdriver_path, auto_closing=True)
        
    def button_pressed(self, sender) -> None:
        if sender == self.app.retrive_button:
            self.retrive_button_clicked(sender)
        elif sender == self.app.search_box:
            self.retrive_button_clicked(sender)
        elif sender == self.app.label_button_list:
            self.list_widget_button_clicked(sender.currentItem())
        elif sender == self.app.clear_button:
            self.app.search_box.clear()
            self.app.current_url = None
        elif sender == self.app.forward_button:
            self.yt_checker.actions.forward()
        elif sender == self.app.back_button:
            self.yt_checker.actions.go_back()
        elif sender == self.app.like_button:
            self.yt_checker.actions.like()
        elif sender == self.app.dislike_button:
            self.yt_checker.actions.dislike()
            
        elif sender == self.app.sub_button:
            if not self.yt_checker.actions.is_subbed():
                self.yt_checker.actions.sub()
            else:
                self.yt_checker.actions.un_sub()

        elif sender == self.app.refresh_button:
            self.yt_checker.refresh()
        elif sender == self.app.pause_button:
            self.yt_checker.actions.pause_video()
        elif sender == self.app.next_video_button:
            self.yt_checker.actions.to_next_video()
        else:
            return
        
        
    def list_widget_button_clicked(self, current_item) -> None:
        sender_text = current_item.text() if current_item else None
        
        keys = [
            'Title', 'Video Length', 'View Count', 'Like Count', 'Sub Count', 'Comment Count', 'Upload Date',
            'Description', 'Video URL', 'Thumbnail URL', 'Family Friendly', 'Video Genre', 'KeyWords', 'Allowed Regions', 'Banned Regions',
        ]
        
        if sender_text == 'None':
            self.app.text_area.hide()
            self.app.text_area.clear()
            
        elif sender_text == 'General Infos':
            pass
            
        elif sender_text in keys:
            self.app.text_area.setText(f'{sender_text}: {self.app.infomations.get(sender_text, 'Error retreiving this infomation :(')}')
        
        self.app.text_area.show()
        
        
        
    def retrive_button_clicked(self, sender) -> None:
        url = self.app.search_box.text()
        if url == self.app.current_url:
            return
    
        # Validate URL
        if not self.app.is_valid_url(url):
              # For debugging purposes
            return

        
        try:
            self.app.text_area.show()
            self.app.text_area.setText('Waiting For Program To Retrive Infomations\nPlease Be Pacient!')
            
            self.app.current_url = url
            sender.setDisabled(True)
            self.app.infomations = self.yt_checker.retrieve_infos(self.app.current_url)
            
            
            thumbnail = self.yt_checker.thumbnail()
            response = requests.get(thumbnail)
            response.raise_for_status()
            
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            
            self.app.thumbnail_url_label.setPixmap(pixmap)
            self.app.thumbnail_url_label.setScaledContents(True)
            self.app.thumbnail_url_label.setFixedSize(250, 80)
            self.app.thumbnail_url_label.show()
            
            
            for button in self.app.action_buttons:
                button.setEnabled(True)
            self.app.label_button_list.setEnabled(True)
            
            self.app.text_area.setText('Infomations Retrieved!')
            sender.setEnabled(True)
            
        except Exception as e:
            youtube_logger.exception(f"Error retrieving data: {e}")
            self.app.text_area.setText(f'Error retrieving data: {e}')