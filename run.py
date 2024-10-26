from youtube_find.youtube import YoutubeChecker
import time

bot = YoutubeChecker()
bot.open('https://www.youtube.com/watch?v=5NjJLFI_oYs')
bot.implicitly_wait(5)
print(f'View: {bot.view_count()}')
print(f'Like: {bot.like_count()}')
print(bot.description_is_opened())
bot.open_description()
print(f'Description:\n{bot.description_text()}')
print(bot.description_is_opened())