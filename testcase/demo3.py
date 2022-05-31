import re

a = 'display: none; width: 50px; height: 50px; top: -100px; z-index: 999; background-image: url("../static/img/verify/1.jpeg"); background-size: 440px 150px; background-position: -220px -55px;'
link = re.compile('background-position: (.*?)px (.*?)px;')
b = link.search(a)
print -int(b.group(1))
