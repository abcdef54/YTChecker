from youtube_find.youtube_checker import YoutubeChecker

import time

bot = YoutubeChecker()
bot.open('https://www.youtube.com/watch?v=j7VZsCCnptM&t=8681s')
bot.implicitly_wait(5)

print(bot.yt_action.description_is_opened())
if not bot.yt_action.description_is_opened():
    bot.yt_action.open_description()

time.sleep(1)

if bot.yt_action.description_is_opened():
    bot.yt_action.close_description()

print(bot.yt_action.description_is_opened())