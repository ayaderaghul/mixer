from bs4 import BeautifulSoup
import random
import functools
import re
from datetime import datetime
import copy

INPUTFILE = 'de_chua_tron_091122.html'
N = 4 # number of mixed tests, usually 4 or 8

htmlfile = open(INPUTFILE)
index = htmlfile.read()

S = BeautifulSoup(index, 'lxml')

body = S.find('body')
ps = body.find_all('p')
print('ps:', ps[0])
header = []

for i in body:
    if str(i).find('Câu') < 0:
        header.append([i])
    else:
        break

footer = []
fp = 0

for i,e in enumerate(body):
    if str(e).find('ẾT') >= 0:
        fp = i
        break

for i,e in enumerate(body):
    if i >= fp:
        footer.append(e)


tests = {}
for i in range(N):    
    tests[f'S{i}'] = copy.copy(body)

def shuffle_qs(body):
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
    return qs

qs = shuffle_qs(tests['S0'])
print('qs: ', qs)
def mix(qs):
    mixed = []
    correctans = []
    print('qs:', qs)
    for i, q in enumerate(qs):
        print('q: ',q)
        bold = S.new_tag('b')
        bold.string = f"Câu {i + 1}:"
        br = S.new_tag('br')
        bold.append(br)

        p = S.new_tag('p')
        p.insert(0, bold)    

        newq = S.new_tag('p')
        newq.insert(0, p)


        imgp = S.new_tag('p')
        print(q)
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
    return mixed

mixeds = []
for k,v in tests:
    mix(v)

def output_test(mixed):
    testID = random.randint(0,100)

    if testID <10:
        id = '00' + str(testID)
    else:
        id = '0' + str(testID)

    with open(f'de_da_tron_{id}.html', 'w') as f:
        for i in header:
            f.write(str(i[0]))
        f.write(f'MÃ ĐỀ: {id}\n')
        for i in mixed:
            f.write(str(i))
        for i in footer:
            f.write(str(i))

with open('cau_tra_loi.docx', 'a') as f:
    f.write(f'MÃ ĐỀ: {id}\n')
    for i, an in enumerate(correctans):
        f.write(f'Câu {i+1}: {an}\n')
    f.write('\n')
print(id)

