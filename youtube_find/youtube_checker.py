import logging
import time
import random
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException


from youtube_find.yt_action import YTAction
import youtube_find.constant as CONST


# Config logger
logging.basicConfig(level=logging.ERROR,
                    filename='logs/app.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s')

youtube_logger = logging.getLogger(__name__)


# Selenium options
edge_options = Options()
edge_options.add_experimental_option('detach', True)


class YoutubeChecker(webdriver.Edge):
    """
    A class for extracting information from YouTube videos.
    
    This class provides methods to retrieve various metadata and statistics
    about YouTube videos, such as title, view count, likes, etc.
    
    Attributes:
        driver_path (str): Path to the Edge webdriver executable
        auto_closing (bool): Whether to automatically close the browser
        yt_action (YTAction): Instance of YTAction for performing YouTube actions
    """
    
    def __init__(self, driver_path: str = CONST.webdriver_path, auto_closing: bool = False) -> None:
        """
        Args:
            driver_path: Path to the Edge webdriver executable
            auto_closing: If True, browser will close automatically when done
        """
        
        self.driver_path = driver_path
        service = Service(executable_path=self.driver_path)
        
        self.yt_action = YTAction(self)
        
        self.auto_closing = auto_closing
        if not self.auto_closing:
            super(YoutubeChecker, self).__init__(options=edge_options,service = service)
        else:
            super(YoutubeChecker, self).__init__(service = service)

    
    def open(self, url: str = CONST.base_url,full_screen: bool = False) -> None:
        """
        Open a YouTube URL and handle initial setup.
        
        Args:
            url: The YouTube URL to open
            full_screen: Whether to make the window fullscreen
        """
        self.get(url)
        self.yt_action.close_yt_premium_ad()
        if full_screen:
            self.fullscreen_window()
    
    
    def title(self) -> Optional[str]:
        """Retrive the title of the video"""
        try:
            title = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'title'))
            )
            if title:
                return title.text
        except TimeoutException:
            youtube_logger.error("TimeoutError: Title element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
            
        return None
        
    
    def url(self) -> Optional[str]:
        """Retrive the url of the video"""
        try:
            url = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:url"]'))
            )
            if url:
                return url.get_attribute('content')
        except TimeoutException:
            youtube_logger.error("TimeoutError: url element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
            
        return None
    
    
    def like_count(self) -> Optional[int]:
        """Retrive the like count as an integer"""
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
        except TimeoutException:
            youtube_logger.error("TimeoutError: like count element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return None
    
    
    def view_count(self) -> Optional[int]:
        """Retrive the view count as an integer"""
        try:
            view_count = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="interactionCount"]'))
            )
            if view_count:
                return int(view_count.get_attribute('content'))
        except TimeoutException:
            youtube_logger.error("TimeoutError: view count element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return None
    
    
    def date_upload(self) -> Optional[str]:
        try:
            date = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="uploadDate"]'))
            )
            if date:
                return date.get_attribute('content')
        except TimeoutException:
            youtube_logger.error("TimeoutError: date element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return None
    
    
    def date_publised(self) -> Optional[str]:
        try:
            date = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="datePublished"]'))
            )
            if date:
                return date.get_attribute('content')
        except TimeoutException:
            youtube_logger.error("TimeoutError: date element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return None
    
    
    def video_is_family_friendly(self) -> bool:
        """Check if youtube family friendly meta tag is 'true'"""
        try:
            friendly = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="isFamilyFriendly"]'))
            )
            if friendly:
                return friendly.get_attribute('content').lower() == 'true'
        except TimeoutException:
            youtube_logger.error("TimeoutError: video friendly element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return False
    
    
    def description_text(self) -> Optional[str]:
        """Retrive the full text of an opened description"""
        if not self.description_is_opened():
            self.open_description()
            
        try:
            description_texts = WebDriverWait(self, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'yt-core-attributed-string--link-inherit-color'))
            )
            if description_texts:
                description = """"""
                for section in description_texts:
                    description += section.text + '\n'
                
                return description.strip()
        except TimeoutException:
            youtube_logger.error("TimeoutError: description_texts element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return None
    
    
    def video_length(self) -> Optional[str]:
        pass
    
    
    def channel_name(self) -> Optional[str]:
        """Get the channel name"""
        try:
            channel_name = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'channel-name'))
            )
            if channel_name:
                return channel_name.text
        except TimeoutException:
            youtube_logger.error('Channel name element not found within the given time')
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
        
        return None
    
    
    def comment_count(self) -> Optional[int]:
        """Retrive the comment count as an integer"""
        if self.yt_action.description_is_opened():    # simulate human user 
            self.yt_action.close_description()        # only then youtube will allow scrolling
        else:
            self.yt_action.open_description()
            
        time.sleep(random.uniform(0.8, 1.2))
        
        max_scroll_attempts = 4
        scroll_attempts = 0
        scroll_pause_time = random.uniform(1, 1.5)  # Pause between scrolls to mimic human-like behavior
        scroll_height = 400

        while scroll_attempts < max_scroll_attempts:
            self.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(random.uniform(0.8, 1.2))
            scroll_height += 400
            scroll_attempts += 1
        
        try:
            comment_count_element = self.find_element(By.ID, 'leading-section')
            if comment_count_element:
                self.scroll_to_view(comment_count_element)
                count_text = comment_count_element.text.split(' ')[0]
                return int(count_text.replace(",", ""))  # Remove commas if present
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')

        return None
    
    
    def sub_count(self) -> Optional[str]:
        """Get the subcriber count of the channel"""
        try:
            sub_count = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'owner-sub-count'))
            )
            if sub_count:
                sub_count: List = sub_count.text.split(' ')
                sub_count: str = sub_count[0]
                return sub_count
        except TimeoutException:
            youtube_logger.error('Sub count element not found within the given time')
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
        
        return None
    
    
    def thumbnail(self) -> Optional[str]:
        """Retrive the thumnail url of the video"""
        try:
            thumbnail_url = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:image"]'))
            )
            if thumbnail_url:
                return thumbnail_url.get_attribute('content')
        except TimeoutException:
            youtube_logger.error('thumbnail_url element not found within the given time')
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
        
        return None


    def video_genre(self) -> Optional[str]:
        """Get the genre of the video"""
        try:
            video_genre = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[itemprop="genre"]'))
            )
            if video_genre:
                return video_genre.get_attribute('content')
        except TimeoutException:
            youtube_logger.error('video_genre element not found within the given time')
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
        
        return None
    

    def top_n_comment(self, n: int = 10) -> None:
        pass
    
    
    def close(self) -> None:
        """Safely close the browser and clean up."""
        try:
            super().quit()
        except Exception as e:
            youtube_logger.exception(f'Error closing browser: {e}')
            
    
    def __enter__(self):
        """Enable context manager support."""
        return self
    
    
    def __exit__(self) -> None:
        """Clean up resources when used as context manager."""
        self.close()