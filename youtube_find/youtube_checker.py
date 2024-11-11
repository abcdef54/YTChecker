import logging
import string
import time
import random
from typing import List, Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webelement import WebElement


from youtube_find.yt_action import YTAction
import youtube_find.constant as CONST
import youtube_find.decorators as decorators


# Config logger
logging.basicConfig(level=logging.INFO,
                    filename='logs/app.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(module)s - %(funcName)s')

youtube_logger = logging.getLogger(__name__)
youtube_logger.propagate = True


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
    """
    
    def __init__(self, driver_path: str = CONST.webdriver_path, auto_closing: bool = False) -> None:
        """
        Args:
            driver_path: Path to the Edge webdriver executable
            auto_closing: If True, browser will close automatically when done
        """
        
        self.driver_path = driver_path
        service = Service(executable_path=self.driver_path)
        
        self.actions = YTAction(self)
        
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
        self.actions.close_yt_premium_ad()
        if full_screen:
            self.fullscreen_window()
    
    
    def title(self) -> Optional[str]:
        """Retrive the title of the video"""
        return self._get_element_attribute(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
    
    
    def url(self) -> Optional[str]:
        """Retrive the url of the video"""
        return self._get_element_attribute(By.CSS_SELECTOR, 'meta[property="og:url"]', 'content')
    
    
    def like_count(self) -> Optional[int]:
        """Retrive the like count as an integer"""
        like_count = self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="interactionCount"]')
        if like_count:
            return int(like_count)
        return None
        
    
    def view_count(self) -> Optional[int]:
        """Retrive the view count as an integer"""
        view_count = self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="interactionCount"]', 'content')
        if view_count:
            return int(view_count)
    
    
    def date_upload(self) -> Optional[str]:
        """Retrive the upload date of the video"""
        return self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="uploadDate"]', 'content')
    
    
    def date_publised(self) -> Optional[str]:
        """Retrive the publised date of the video"""
        return self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="datePublished"]', 'content')
    
    

    def video_is_family_friendly(self) -> bool:
        """Check if youtube family friendly meta tag is 'true'"""
        friendly = self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="isFamilyFriendly"]', 'content')
        if friendly:
            return friendly.lower() == 'true'
    
    
    def description_text(self) -> Optional[str]:
        """Retrive the full text of an opened description"""
        if not self.actions.description_is_opened():
            self.actions.open_description()
            
        time.sleep(0.2)
        description_texts = self._get_element_attribute(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string')
        if description_texts:
            return description_texts.text.strip()
    
    
    def video_length(self) -> Optional[str]:
        """Return the formatted video length"""
        vid_length = self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="duration"]', 'content')
        if vid_length:
            return self._format_video_length(vid_length)
    

    def channel_name(self) -> Optional[str]:
        """Get the channel name"""
        return self._get_element_attribute(By.ID, 'channel-name').text
    
    
    def comment_count(self) -> Optional[int]:
        """Retrive the comment count as an integer"""
        if self.actions.description_is_opened():    # simulate human user 
            self.actions.close_description()        # only then youtube will allow scrolling
        else:
            self.actions.open_description()
            
        time.sleep(random.uniform(0.8, 1.2))
        
        max_scroll_attempts = 4
        scroll_attempts = 0
        scroll_pause_time = random.uniform(0.1, 0.4)  # Pause between scrolls to mimic human-like behavior
        scroll_height = 400

        while scroll_attempts < max_scroll_attempts:
            self.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(scroll_pause_time)
            scroll_height += 400
            scroll_attempts += 1
        
        time.sleep(random.uniform(0.8, 1.2))
        try:
            comment_count_element = self.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]')
            if comment_count_element:
                self.actions.scroll_to_view(comment_count_element)
                count_text = comment_count_element.text.split(' ')[0]
                return int(count_text.replace(",", ""))
        except Exception as e:
            youtube_logger.exception(f'Unexpected Error: {e}')

        return None
    
    
    def sub_count(self) -> Optional[str]:
        """Get the subcriber count of the channel"""
        sub_count = self._get_element_attribute(By.ID, 'owner-sub-count')
        if sub_count:
            sub_count: List = sub_count.text.split(' ')
            sub_count = sub_count[0]
            return sub_count
    
    
    def thumbnail(self) -> Optional[str]:
        """Retrive the thumnail url of the video"""
        return self._get_element_attribute(By.CSS_SELECTOR, 'meta[property="og:image"]', 'content')


    def video_genre(self) -> Optional[str]:
        """Get the genre of the video"""
        return self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="genre"]', 'content')
    
    
    def keywords_tags(self) -> List[str]:
        keywords = self._get_element_attribute(By.CSS_SELECTOR, 'meta[name="keywords"]', 'content')
        if keywords:
            return keywords.split(',')
    
    
    def regions_allowed(self) -> List[str]:
        regions_allowed = self._get_element_attribute(By.CSS_SELECTOR, 'meta[itemprop="regionsAllowed"]', 'content')
        if regions_allowed:
            return regions_allowed.split(',')
    
    
    @decorators.error_handle
    def banned_regions(self) -> List[str]:
        allowed_regions = set(self.regions_allowed())
        banned_regions = []
        
        try:
            with open("Tags.txt", "r") as file:
                all_regions = file.read().splitlines()
                for region in all_regions:
                    if region not in allowed_regions:
                        banned_regions.append(region)
           
        except FileNotFoundError:
            youtube_logger.error("Error: Tags.txt file not found.")
            raise
            
        return banned_regions
    
    
    def retrieve_infos(self, url: str) -> Optional[Dict[Any, Any]]:
        if not url:
            return None
        
        self.open(url)
        self.implicitly_wait(6)
        
        infos = {
            'Title' : self.title(),
            'Length' : self.video_length(),
            'View' : self.view_count(),
            'Like' : self.like_count(),
            'CommentCount' : self.comment_count(),
            'Date' : self.date_upload(),
            'ChannelName' : self.channel_name(),
            'SubCount' : self.sub_count(),
            'Description' : self.description_text(),
            'URL' : self.url(),
            'Thumbnail' : self.thumbnail(),
            'FamilyFriendly' : self.video_is_family_friendly(),
            'Genre' : self.video_genre(),
            'KeyWords' : self.keywords_tags(),
            'BannedRegions' : self.banned_regions(),
            'RegionsAllowed' : self.regions_allowed()
        }
        return infos
    
    
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
    
    
    @decorators.error_handle
    def _get_element_attribute(self, by: By, value: str, attribute: str = None, wait_time: int = 7) -> None | str | WebElement:
        """
        Return the attribute of the web element, if no attribute is inputed, return that web element
        """
        element = WebDriverWait(self, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
        if element:
            if attribute:
                return element.get_attribute(attribute)
            else:
                return element
        
        
    @decorators.error_handle
    def _get_all_element(self, by: By, value: str, wait_time: int = 7) -> Optional[List[WebElement]]:
        elements = WebDriverWait(self, wait_time).until(
            EC.presence_of_all_elements_located((by, value))
        )
        if elements:
            return elements
    
    
    @staticmethod
    def _format_video_length(length: str) -> str:
        length = length[2:]
        minutes = ""
        seconds = ""
        count = 0
        
        for letter in length:
            if letter in string.ascii_letters:
                count += 1
                break
            else:
                count += 1
                minutes += letter
        time = int(length[count: -1]) + int(minutes) * 60
        
        hour = time // 3600
        minutes = (time % 3600) // 60
        seconds = time - (hour * 3600 + minutes * 60)
        
        return f"{hour:02}:{minutes:02}:{seconds:02}"
