from youtube_find.youtube import YoutubeChecker
import time

bot = YoutubeChecker()
bot.open('https://www.youtube.com/watch?v=lc73yOh5taA')

print(f'comment: {bot.comment_count()}')