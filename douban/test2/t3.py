import re
mystr = '今天的天气真好，天气真的好'

pattern = re.compile('天气')
match = pattern.match(mystr)
print(match)
search = pattern.search(mystr)
print(search)
find = re.findall(pattern, mystr)
print(find)
