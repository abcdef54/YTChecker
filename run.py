from youtube_find.youtube_checker import YoutubeChecker

bot = YoutubeChecker()
infos = bot.retrieve_infos('https://www.youtube.com/watch?v=2Gtl2BKp4gY')
for key,value in infos.items():
    print(f'{key}: {value}\n')
"""
bot.open('https://www.youtube.com/watch?v=2Gtl2BKp4gY')
bot.implicitly_wait(5)
print(f'Title: {bot.title()}')
print(f'URL: {bot.url()}')
print(f'View: {bot.view_count}')
print(f'Like: {bot.like_count()}')
print(dat)

"""