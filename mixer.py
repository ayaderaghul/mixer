from bs4 import BeautifulSoup
import random
import functools
import re
# docx file should be formatted properly:
# mark the letter of the answer with underline (underline A for example)
# there is only two dots in each answer, after the letter and at the end: "A. here comes the answer A. "

# convert from docx to html using libre
htmlfile = open('output_newest_html.html')

index = htmlfile.read()

S = BeautifulSoup(index, 'lxml')

divs = S.find_all('div')

# silent all the attributes of font, span, p .. tags
for t in divs[2](['span']):
    for a in ['class', 'style']:
        del t[a]

for t in divs[2](['img']):
    for a in ['align', 'hspace']:
        del t[a]

for t in divs[2](['font', 'p']):
    # t.decompose()
    for a in ['face', 'size', 'style', 'color']:
        del t[a]

for t in divs[2](['br']):
    t.decompose()

lst = []
for i in divs[2]:
    lst.append(i)

# each ol is a question
qs = []
for i in lst[4:-15]:
    if str(i)[:2] == '<o':
        qs.append(i)
    else:
        qs[-1].append(i)

# print(qs[0])
# shuffle the questions
random.shuffle(qs)

# shuffle the answers, save the answer with u tag
ans = {}
for i, o in enumerate(qs):
    bold = S.new_tag('b')
    bold.string = f"Câu {i + 1}:"
    br = S.new_tag('br')
    bold.append(br)
    p = S.new_tag('p')
    p.insert(0, bold)
    # g = o.select('.Graph')

    imgs = o.find_all('img')
    gs = []
    for img in imgs:
        if 'height' in img.attrs:
            if int(img.attrs['height']) >= 40:
                gs.append(img)
    if len(gs) >= 1:
        for g in gs:
            lp = len(p)
            p.insert(lp, g)
    o.insert(0, p)
    l = len(o)
    b = S.new_tag('br')
    o.insert(l, b)
    o.name='p'
    lis = o.find_all('li')
    for li in lis:
        li.name = 'p'
    # qnum = o.attrs['start']
    a = o.find_all('u')
    at = list(map(lambda x: [*x.text], a))
    at = [item for sublist in at for item in sublist]
    al = ['A', 'B', 'C', 'D']
    at = list(filter(lambda x: x in al, at))
    atn = al.index(at[0])
    # ans[i+1] = at[0]
    for u in o(['u']):
        u.name = 'span'
    qp = list(o.children)[:4]
    lp = list(o.children)[-1]
    ap = list(o.children)[4:-1]
    fap = list(filter(lambda x: x != '\n', ap))
    ep = S.new_tag('p')
    ep.string='\n'
    ep2 = S.new_tag('p')
    ep2.attrs['lang'] = 'en-US'
    ep2.string='\n'
    ep3 = S.new_tag('p')
    ep3.string='\n\n'
    fap2 = list(filter(lambda x: x != ep and x != ep2 and x.text != ep3.text, fap))
    no = [0,1,2,3]
    random.shuffle(no)
    if len(fap2) == 1:
        s = str(fap2[0])
    elif len(fap2) == 2:
        s = str(fap2[0]) + str(fap2[1])
    else:
        s = ''.join(list(map(lambda x: str(x), fap2)))

    ps = [m.start() for m in re.finditer('\.', s)]
    # fps = list(filter(lambda x: s[x-1] != '>', ps))
    fps = [ps[0]]
    for k in range(1,len(ps)-1,1):
        if s[ps[k]-2:ps[k]] == 'i>' or s[ps[k]+1:ps[k]+4] == 'gif' or s[ps[k]+1:ps[k]+4] == 'png':
            continue
        else:
            fps.append(ps[k])
    fps.append(ps[-1])

    sapA = s[fps[0]+1:fps[1]] + '<br/>'
    sapB = s[fps[2]+1:fps[3]] + '<br/>'
    sapC = s[fps[4]+1:fps[5]] + '<br/>'
    sapD = s[fps[6]+1:fps[7]] + '<br/>'

    l = [sapA, sapB, sapC, sapD]
    nl = []
    for j in range(4):
        # nl.append(l[no[j]].replace(al[no[j]], al[j]))
        nl.append(al[j] + '. ' + l[no[j]])
        if no[j] == atn:
            ans[i+1] = al[j]
    hnl = list(map(lambda x: BeautifulSoup(x, 'html.parser'), nl))  
    r = qp + hnl + [lp]
    r2 = list(map(lambda x: str(x), r))
    r3 = ''.join(r2)
    r4 = BeautifulSoup(r3, 'html.parser')

    o = r4
    qs[i] = o
    # if i < 5:
    #     print(i)
    #     print(qs[i])
    #     print('\n')

mixed = list(map(lambda x: str(x), qs))

with open('de_da_tron.html', 'w') as f:
    for i in mixed:
        f.write(i)

with open('cau_tra_loi.docx', 'w') as f:
    sa = sorted(ans.items())
    for i in sa:
        f.write(f'Câu {i[0]}: {i[1]}\n')
