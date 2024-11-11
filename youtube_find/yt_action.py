import time
import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging

import youtube_find.decorators as decorators
youtube_logger = logging.getLogger('youtube_find.youtube_checker')

class YTAction:
    """
    A class for performing actions on YouTube videos.
    
    This class handles user interactions like liking, subscribing,
    commenting, and navigating through YouTube's interface.
    
    Attributes:
        driver (webdriver): Take in YoutubeChecker instance as a webdriver
    """
    
    def __init__(self, driver: webdriver) -> None:
        """
        Args:
            driver: Take in YoutubeChecker instance as a webdriver
        """
        self.driver = driver
    
    
    @decorators.error_handle
    def wait_for_element(self, by: By, value: str, timeout: int = 7) -> None | WebElement:
        """
        Wait for an element to be present and return it.
        Using 'EC.presence_of_element_located()'
        
        Args:
            by: Selenium By locator strategy
            value: Locator value
            timeout: How long to wait for element
            
        Returns:
            WebElement if found, None otherwise
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        if element:
            return element
        return None

    
    def search(self, content: str) -> bool:
        """
        Search for the specified content on YouTube.
        
        Args:
            content: Search query string
            
        Returns:
            bool: True if search was successful, False otherwise
        """
        search_box = self.wait_for_element(By.NAME, 'search_query')
        if search_box:
            search_box.click()
            search_box.send_keys(content)
            search_box.submit()
            return True
        return False
    
    
    def is_liked(self) -> bool:
        """
        Check if the current video is already liked.
        """
        like_count = self.driver.like_count()
        is_liked = self.wait_for_element(By.CSS_SELECTOR, f'button[aria-label="like this video along with {like_count:,} other people"]')
        if is_liked:
            return is_liked.get_attribute('aria-pressed') == 'true'
        return False
    
    
    def like(self) -> bool:
        """
        Like the current video if not already liked.
            
        Returns:
            bool: True if like successful, False otherwise
        """
        if self.is_liked():
            return
        
        like_count = self.driver.like_count()
        like_button = self.wait_for_element(By.CSS_SELECTOR, f'button[aria-label="like this video along with {like_count:,} other people"]')
        if like_button:
            self.scroll_to_view(like_button)
            like_button.click()
            return True
        
        return False
    
    
    def dislike(self) -> None:
        """
        Dislike the current video if not already disliked.
            
        Returns:
            bool: True if disliked successful, False otherwise
        """
        if self.is_dislike():
            return
        dislike_button = self.wait_for_element(By.CSS_SELECTOR, 'button[aria-label="Dislike this video"]')
        if dislike_button:
            self.scroll_to_view(dislike_button)
            dislike_button.click()
            return True
        return False
    
    
    def is_dislike(self) -> bool:
        """
        Return True if already disliked the video, False otherwise,
        """
        dislike_button = self.wait_for_element(By.CSS_SELECTOR, 'button[aria-label="Dislike this video"]')
        if dislike_button:
            return dislike_button.get_attribute('aria-pressed') == 'true'
        return False
    
    
    def comment(self, content: str) -> None:
        """
        Comment on a youtube video
        ***Method not usable due to having to log in to comment***
        """
        if not content:
            return
        
        comment_box = self.wait_for_element(By.ID, 'placeholder-area')
        if comment_box:
            self.scroll_to_view(comment_box)
            time.sleep(0.1)
            comment_box.click()
            time.sleep(0.1)
            comment_box.send_keys(content)
            time.sleep(0.3)
            
            try:
                comment_button = self._comment_button()
                comment_button.click()
            except Exception as e:
                youtube_logger.error(f'Error clicking comment button: {e}')
                
    
    def _comment_button(self) -> WebElement | None:
        """
        ***Method not usable due to having to log in to comment***
        """
        comment_button = self.wait_for_element(By.CSS_SELECTOR, 'button[aria-label="Comment"]')
        if comment_button:
            return comment_button

        return None
        
    
    def to_next_video(self) -> bool:
        """
        Navigate to the next video in the playlist or suggested videos.
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        next_button = self.wait_for_element(By.CSS_SELECTOR, 'a[aria-label="Next keyboard shortcut SHIFT+n"]')
        if next_button:
            self.scroll_to_view(next_button)
            next_button.click()
            return True
        return False
    
    
    def forward(self, wait_time: tuple[float, float] = (0.5, 1)) -> bool:
        """
        Goes one step forward in the browser history.
        
        Args:
            wait_time: Tuple of (min, max) seconds to wait after action
            
        Returns:
            bool: True if forward navigation successful, False otherwise
        """
        try:
            self.driver.forward()
            time.sleep(random.uniform(*wait_time))
            return True
        except Exception as e:
            youtube_logger.exception(f'Error navigating forward: {e}')
        return False
    
    
    def go_back(self, wait_time: tuple[float, float] = (0.5, 1)) -> bool:
        """
        Go backward to the previous page.
        
        Args:
            wait_time: Tuple of (min, max) seconds to wait after action
            
        Returns:
            bool: True if backward navigation successful, False otherwise
        """
        try:
            self.driver.back()
            time.sleep(random.uniform(*wait_time))
            return True
        except Exception as e:
            youtube_logger.exception(f'Error navigating back: {e}')
        return False
    
    
    def refresh(self, wait_time: tuple[float, float] = (1, 1.5)) -> bool:
        """
        Refresh the current page.
        
        Args:
            wait_time: Tuple of (min, max) seconds to wait after refresh
            
        Returns:
            bool: True if refresh successful, False otherwise
        """
        try:
            self.driver.refresh()
            time.sleep(random.uniform(*wait_time))
            return True
        except Exception as e:
            youtube_logger.exception(f'Error refreshing page: {e}')
        return False
    
    
    def click_search_video(self) -> None:
        """
        Click on the first video found after searching for something
        """
        video_title = self.wait_for_element(
            By.ID,
            'video-title'
        )
        if video_title:
            self.scroll_to_view(video_title)
            video_title.click()
    
    
    def scroll_to_view(self, element: WebElement) -> None:
        """
        Scroll element into view with human-like behavior.
        
        Args:
            element: Element to scroll to
        """
        if element.is_displayed():
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    
    
    def is_subbed(self) -> bool:
        """
        Check if currently subscribed to the channel.
        
        Returns:
            bool: True if subscribed, False otherwise
        """
        is_sub = self.wait_for_element(
            By.CLASS_NAME, 
            'yt-spec-button-shape-next__button-text-content'
        )
        if is_sub:
            return is_sub.text == 'Subscribed'
        return False
    
    
    def sub(self) -> None:
        """Subscribe to the channel if not already subscribed."""
        if self.is_subbed():
                return

        sub_button = self.wait_for_element(
            By.ID,
            'subscribe-button'
        )
        if sub_button:
            self.scroll_to_view(sub_button)
            sub_button.click()
    

    def unsub(self) -> None:
        """Unsubscribe from the channel if currently subscribed."""
        if not self.is_subbed():
            return

        sub_button = self.wait_for_element(
            By.CSS_SELECTOR,
            'button[aria-label="Unsubscribe"]'
        )
        if sub_button:
            sub_button.click()
    
    
    def open_description(self) -> None:
        """Open the description if closed"""
        if self.description_is_opened():
            return
        
        description = self.wait_for_element(By.ID, 'bottom-row')
        
        if description:
            self.scroll_to_view(description)
            description.click()
            

    def description_is_opened(self) -> bool:
        description = self.wait_for_element(By.ID, 'collapse')
        if description:
            return description.is_displayed()
    
        return False
    
    
    def close_description(self) -> None:
        """Close the description if opened"""
        if not self.description_is_opened():
            return
        
        close = self.wait_for_element(By.ID, 'collapse')
        if close:
            self.scroll_to_view(close)
            close.click()
    
    
    def click_video_on_main_page(self) -> None:
        video_link = self.wait_for_element(By.ID, 'media-container-link')
        if video_link:
            self.scroll_to_view(video_link)
            video_link.click()
    
    
    def visit_channel(self) -> bool:
        """
        Navigate to the channel page of the current video.
        
        Returns:
            bool: True if navigation to channel successful, False otherwise
        """
        channel_name = self.wait_for_element(By.ID, 'channel-name')
        if channel_name:
            self.scroll_to_view(channel_name)
            channel_name.click()
            return True
        return False
            
    
    def close_yt_premium_ad(self) -> None:
        """
        Close the YouTube Premium advertisement popup if present.
        """
        reject_button = self.wait_for_element(By.CSS_SELECTOR, 'button[aria-label="No thanks"]')
        if reject_button:
            reject_button.click()
            
