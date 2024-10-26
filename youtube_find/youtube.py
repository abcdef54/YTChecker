import os
from typing import List, Any, Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import youtube_find.constant as CONST

os.system('cls')

edge_options = Options()
edge_options.add_experimental_option('detach', True)

class YoutubeChecker(webdriver.Edge):
    def __init__(self, driver_path: str = CONST.webdriver_path, auto_closing: bool = False) -> None:
        self.driver_path = driver_path
        service = Service(executable_path='D:\Study\Programming\WebDrivers\msedgedriver.exe')
        
        self.auto_closing = auto_closing
        if not self.auto_closing:
            super(YoutubeChecker, self).__init__(options=edge_options,service = service)
        else:
            super(YoutubeChecker, self).__init__(service = service)
        
    
    def open(self, url: str = CONST.base_url,full_screen: bool = False) -> None:
        self.get(url)
        if full_screen:
            self.fullscreen_window()
        
    
    def search(self, content: str) -> None:
        try:
            search_box = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.NAME, 'search_query'))
            )
            
            if search_box:
                search_box.click()
                search_box.send_keys(content)
                search_box.submit()
        except Exception as e:
            print(f'Unexpected Error: {e}')
    
    
    def title(self) -> Optional[str]:
        try:
            title = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'title'))
            )
            if title:
                return title.text
        except Exception as e:
            print(f'Unexpected Error: {e}')
            
        return None
        
    
    def url(self) -> Optional[str]:
        try:
            url = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:url"]'))
            )
            if url:
                return url.get_attribute('content')
        except Exception as e:
            print(f'Unexpected Error: {e}')
            
        return None
    
    
    def like_count(self) -> Optional[int]:
        try:
            like_count = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="I like this"]'))
            )
            if like_count:
                like_num = like_count.get_attribute('aria-label')
                like_num = like_num.split(' ')
                for token in like_num:
                    if token.replace(',','').isdigit():
                        return int(token.replace(',',''))
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return None
    
    
    def view_count(self) -> Optional[int]:
        try:
            view_count = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="interactionCount"]'))
            )
            if view_count:
                return int(view_count.get_attribute('content'))
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return None
    
    
    def date_upload(self) -> Optional[str]:
        try:
            date = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="uploadDate"]'))
            )
            if date:
                return date.get_attribute('content')
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return None
    
    
    def date_publised(self) -> Optional[str]:
        try:
            date = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="datePublished"]'))
            )
            if date:
                return date.get_attribute('content')
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return None
    
    
    def video_is_family_friendly(self) -> bool:
        try:
            date = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="isFamilyFriendly"]'))
            )
            if date:
                return date.get_attribute('content').lower() == 'true'
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return False
    
    
    def description_text(self) -> Optional[str]:
        try:
            description_texts = WebDriverWait(self, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'yt-core-attributed-string--link-inherit-color'))
            )
            if description_texts:
                description = """"""
                for section in description_texts:
                    description += section.text + '\n'
                
                return description.strip()
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return None
    
    
    def open_description(self) -> None:
        try:
            description = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'bottom-row'))
            )
            if description:
                description.click()
        except Exception as e:
            print(f'Unexpected Error: {e}')
            

    def description_is_opened(self) -> bool:
        try:
            description = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'collapse'))
            )
            if description:
                return description.is_displayed()
        except Exception as e:
            print(f'Unexpected Error: {e}')
        
        return False
    
    
    def close_description(self) -> None: # Not Working Yet
        if not self.description_is_opened():
            return
        try:
            close = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'collapse'))
            )
            if close:
                close.click()
        except Exception as e:
            print(f'Unexpected Error: {e}')
    
    
    def video_length(self) -> Optional[str]:
        pass
    
    
    def channel_name(self) -> Optional[str]:
        pass
    
    
    def comment_count(self) -> Optional[int]:
        pass
    
    
    def is_subbed(self) -> bool:
        pass
    
    
    def sub(self) -> None:
        pass
    
    
    def comment(self, content: str) -> None:
        pass
    
    
    def like(self) -> None:
        pass
    
    
    def dislike(self) -> None:
        pass
    

    def to_next_video(self) -> None:
        pass
    
    
    def top_n_comment(self, n: int = 10) -> None:
        pass