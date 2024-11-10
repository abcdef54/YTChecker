from youtube_find.youtube_checker import YoutubeChecker

import time

bot = YoutubeChecker()
bot.open('https://www.youtube.com/watch?v=2Gtl2BKp4gY')
bot.implicitly_wait(5)
if not bot.actions.description_is_opened():
    bot.actions.open_description()

time.sleep(1)

bot.actions.comment('Hello World')