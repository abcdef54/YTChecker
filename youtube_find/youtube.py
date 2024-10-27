import os
import logging
import time
import random
from typing import List, Any, Optional, Dict
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException
import youtube_find.constant as CONST

os.system('cls')

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
    def __init__(self, driver_path: str = CONST.webdriver_path, auto_closing: bool = False) -> None:
        self.driver_path = driver_path
        service = Service(executable_path=self.driver_path)
        
        self.auto_closing = auto_closing
        if not self.auto_closing:
            super(YoutubeChecker, self).__init__(options=edge_options,service = service)
        else:
            super(YoutubeChecker, self).__init__(service = service)

        
    
    def open(self, url: str = CONST.base_url,full_screen: bool = False) -> None:
        """Open a URL and optionally make the window fullscreen."""
        self.get(url)
        if full_screen:
            self.fullscreen_window()
        
    
    def search(self, content: str) -> None:
        """Search for the specified content on YouTube."""
        try:
            search_box = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.NAME, 'search_query'))
            )
            
            if search_box:
                search_box.click()
                search_box.send_keys(content)
                search_box.submit()
        except TimeoutException:
            youtube_logger.error("TimeoutError: Search box not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
    
    
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
    
    
    def open_description(self) -> None:
        """Open the description if closed"""
        if self.description_is_opened():
            return
        try:
            description = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'bottom-row'))
            )
            if description:
                description.click()
        except TimeoutException:
            youtube_logger.error("TimeoutError: description element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
            

    def description_is_opened(self) -> bool:
        try:
            description = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'collapse'))
            )
            if description:
                return description.is_displayed()
        except TimeoutException:
            youtube_logger.error("TimeoutError: description element not found within the given time.")
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error in title: {e}')
        
        return False
    
    
    def close_description(self) -> None: # Not Working Yet
        """Close the description if opened"""
        if not self.description_is_opened():
            return
        try:
            close = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'collapse'))
            )
            if close:
                close.click()
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')
    
    
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
        if self.description_is_opened():    # simulate human user 
            self.close_description()        # only then youtube will allow scrolling
        else:
            self.open_description()
            
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
    
    
    def visit_channel(self) -> None:
        """Go to the channel that uploaded of the video"""
        try:
            channel_name = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'channel-name'))
            )
            if channel_name:
                channel_name.click()
        except TimeoutException:
            youtube_logger.error('Channel name element not found within the given time')
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')


    def is_subbed(self) -> bool:
        """Check if is subbed to the channel"""
        try:
            is_sub = self.find_element(By.CLASS_NAME, 'yt-spec-button-shape-next__button-text-content')
            if is_sub:
                return is_sub.text == 'Subscribed'
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')
            return False
        
        return False


    def sub(self) -> None:
        """Subscribe to the channel if not already subscribed."""
        if self.is_subbed():
                return
        try:
            sub_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'subscribe-button'))
            )
            if sub_button:
                self.scroll_to_view(sub_button)
                sub_button.click()
        except TimeoutException:
            youtube_logger.error(f'Timeout: dislike element not found within the given time')
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')


    def unsub(self) -> None:
        """Unsubscribe from the channel if currently subscribed."""
        if not self.is_subbed():
            return

        try:
            sub_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Unsubscribe"]'))
            )
            if sub_button:
                sub_button.click()
        except TimeoutException:
            youtube_logger.error(f'Timeout: dislike element not found within the given time')
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')


    def comment(self, content: str) -> None:
        pass


    def like(self) -> None:
        """like the video if not already liked"""
        if self.is_liked():
            return
        
        like_count = self.like_count()
        try:
            like_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'button[aria-label="like this video along with {like_count:,} other people"]'))
            )
            if like_button:
                self.scroll_to_view(like_button)
                like_button.click()
        except TimeoutException:
            youtube_logger.error(f'Timeout: dislike element not found within the given time')
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')


    def is_liked(self) -> bool:
        """
        Check if the video is already liked.

        Returns:
            bool: True if the video is liked, False otherwise.
        """
        like_count = self.like_count()
        try:
            is_liked = self.find_element(By.CSS_SELECTOR, f'button[aria-label="like this video along with {like_count:,} other people"]')
            if is_liked:
                return is_liked.get_attribute('aria-pressed') == 'true'
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')
            return False

        return False


    def dislike(self) -> None:
        """Dislike the video if not already disliked."""
        try:
            dislike_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Dislike this video"]'))
            )
            if dislike_button:
                self.scroll_to_view(dislike_button)
                dislike_button.click()
        except TimeoutException:
            youtube_logger.error(f'Timeout: dislike element not found within the given time')
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')

     
    def to_next_video(self) -> None:
        """Navigate to the next video in the playlist or suggested videos."""
        try:
            next_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Next keyboard shortcut SHIFT+n"]'))
            )
            if next_button:
                self.scroll_to_view(next_button)
                next_button.click()
        except TimeoutException:
            youtube_logger.error(f'Timeout: dislike element not found within the given time')
        except Exception as e:
            youtube_logger.error(f'Unexpected Error: {e}')
            

    def top_n_comment(self, n: int = 10) -> None:
        pass
    
    
    def scroll_to_view(self, element: WebElement) -> None:
        """
        Scroll the page to bring the specified element into view.

        Args:
            element (WebElement): The web element to scroll into view.
        """
        self.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(0.5, 1.0))