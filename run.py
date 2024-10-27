from youtube_find.youtube import YoutubeChecker
import time

bot = YoutubeChecker()
bot.open('https://www.youtube.com/watch?v=qC-DZ3fnclA')

bot.dislike()
