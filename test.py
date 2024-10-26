
a = '2018-09-12T09:00:01-07:00'
date = ''
for char in a:
    if char == 'T':
        break
    else:
        date += char

print(date)