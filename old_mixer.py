from bs4 import BeautifulSoup
import random
import functools
import re
from datetime import datetime

htmlfile = open('de_chua_tron_281022.html')
index = htmlfile.read()
S = BeautifulSoup(index, 'lxml')


body = S.find('body')

for t in body(['p']):
    for a in ['align', 'class', 'lang', 'style']:
        del t[a]
for t in body(['font']):
    for a in ['color']:
        del t[a]
for t in body(['span']):
    for a in ['lang', 'style']:
        del t[a]
for t in body(['img']):
    for a in ['align', 'border', 'name']:
        del t[a]
for t in body(['a']):
    for a in ['name']:
        del t[a]


ps = body.find_all('p')
qs = []
for i in body:
    if str(i).find('Câu') >= 0:
        qs.append([i])
    else:
        if len(qs) < 1:
            continue
        else:
            qs[-1].append(i)


random.shuffle(qs)

mixed = []
correctans = []
for i, q in enumerate(qs):
    bold = S.new_tag('b')
    bold.string = f"Câu {i + 1}:"
    br = S.new_tag('br')
    bold.append(br)

    p = S.new_tag('p')
    p.insert(0, bold)    

    newq = S.new_tag('p')
    newq.insert(0, p)


    imgp = S.new_tag('p')

    imgs = q[2].find_all('img')
    gs = []
    for img in imgs:
        if 'height' in img.attrs:
            if int(img.attrs['height']) >= 40:
                gs.append(img)
    if len(gs) >= 1:
        for g in gs:
            lp = len(imgp)
            imgp.insert(lp, g)


    newq.insert(len(newq), imgp)

    newq.insert(len(newq), q[2])

    ANS = ['A', 'B', 'C', 'D']


    if len(list(filter(lambda y: y >=0, list(map(lambda x: str(x).find('table'), q))))) > 0:
        table = q[4]
        tds = table.find_all('td')
        random.shuffle(tds)

        newans = []
        for i, td in enumerate(tds):
            s = str(td)
            if s.find('<u>') >= 0 and s.find('</u>') >= 0:
                correctans.append(ANS[i])
            dots = [dot.start() for dot in re.finditer('\.', s)]
            dot1 = dots[0]
            dot2 = dots[-1]

            newan = ANS[i] + s[dot1:dot2]
            newantag = S.new_tag('td', attrs={"style":"border: none; padding: 0in", "width":"25%"})
            newantag.insert(0, BeautifulSoup(newan, 'html.parser'))
            newans.append(newantag)
        newtable = S.new_tag('table', attrs={"cellpadding":"0", "cellspacing":"0", "width":"100%"})
        newcol1 = S.new_tag('col', attrs={"width":"64"})
        newcol2 = S.new_tag('col', attrs={"width":"64"})
        newcol3 = S.new_tag('col', attrs={"width":"64"})
        newcol4 = S.new_tag('col', attrs={"width":"64"})
        newtr = S.new_tag('tr', attrs={"valign":"top"})

        newtable.insert(0, newcol1)
        newtable.insert(1, newcol2)
        newtable.insert(2, newcol3)
        newtable.insert(3, newcol4)
        newtable.insert(4, newtr)


        for an in newans:
            newtable.insert(len(newtable), an)
        
        newq.insert(len(newq), newtable)
    else:
        validans = [q[4], q[6], q[8], q[10]]

        random.shuffle(validans)
        newans = []
        for i, an in enumerate(validans):
            s = str(an)
            if s.find('<u>') >= 0 and s.find('</u>') >= 0:
                correctans.append(ANS[i])
            dots = [dot.start() for dot in re.finditer('\.', s)]
            dot1 = dots[0]
            dot2 = dots[-1]

            newan = ANS[i] + s[dot1:dot2]
            newantag = S.new_tag('p')
            newantag.insert(0, BeautifulSoup(newan, 'html.parser'))
            newans.append(newantag)

        newq.insert(len(newq), newans[0])
        newq.insert(len(newq), newans[1])
        newq.insert(len(newq), newans[2])
        newq.insert(len(newq), newans[3])

    mixed.append(newq)

testID = random.randint(0,100)

if testID <10:
    id = '00' + str(testID)
else:
    id = '0' + str(testID)

with open(f'de_da_tron_{id}.html', 'w') as f:
    f.write('<p>ĐỀ KIỂM TRA THƯỜNG XUYÊN 15 PHÚT</p>')
    f.write(f'<p>MÃ ĐỀ: {id}</p>')
    for i in mixed:
        f.write(str(i))

with open('cau_tra_loi.docx', 'a') as f:
    # sa = sorted(ans.items())
    f.write('ĐỀ KIỂM TRA THƯỜNG XUYÊN 15 PHÚT\n')
    f.write(f'MÃ ĐỀ: {id}\n')
    for i, an in enumerate(correctans):
        f.write(f'Câu {i+1}: {an}\n')
    f.write('\n')
print(id)

