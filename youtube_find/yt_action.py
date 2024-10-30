import time
import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging

youtube_logger = logging.getLogger('youtube_find.youtube_checker')

class YTAction:
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        
    
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
    
    
    def is_dislike(self) -> bool:
        pass
    
    
    def comment(self, content: str) -> None:
        pass
    
    
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
    
    
    def go_back(self) -> None:
        pass
    
    
    def refresh(self) -> None:
        pass
    
    
    def click_search_video(self) -> None:
        pass
    
    
    def scroll_to_view(self, element: WebElement) -> None:
        """
        Scroll the page to bring the specified element into view.

        Args:
            element (WebElement): The web element to scroll into view.
        """
        self.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(0.5, 1.0))
    
    
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
    
    
    def click_video_on_main_page(self) -> None:
        pass
    
    
    def sign_in(self, username: str, password: str) -> None:
        pass
    
    
    def sign_out(self) -> None:
        pass
    
    
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