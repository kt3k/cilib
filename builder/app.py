#! /usr/bin/env python

import os
import sys
import time
import chip

now = int(time.time())

def recent(second):
    return abs(now - second) < 172800

xmark = chip.img(src = '/images/silkapp')
pymark = chip.img(src = '/images/py.gif')
dirmark = chip.img(src = '/images/silkfolder')
textmark = chip.img(src = '/images/silktext')
picmark = chip.img(src = '/images/silkimg')

def item(l, dir):
    suf = l.endswith
    st = os.stat(dir+l)
    sz = st.st_size
    if suf('.py'):
        a = chip.a(l,url='/cat?' + dir+l)
        mark = chip.a(pymark, dir+l)
        ln = len(map(lambda x:1,open(dir+l)))
    elif suf('.pyc'):
        a = chip.spangray(l)
        mark = ''
        ln = ''
    elif filter(suf,('.cgi','.ml','.scm')):
        a = chip.a(l,url='/cat?' + dir+l)
        mark = chip.a(xmark, dir+l)
        ln = len(map(lambda x:1,open(dir+l)))
    elif os.path.isdir(dir+l):
        pth = os.path.normpath(dir + l)
        if pth == '.':
            addr = '/ls'
        else:
            addr = '/ls?' + pth + '/'
        a = chip.a(l+'/', url=addr)
        mark = chip.a(dirmark, url=addr)
        ln = ''
        sz = ''
    elif suf('.gif') or suf('.jpg') or suf('.png') or suf('.PNG'):
        a = chip.a(l, url=dir+l)
        mark = chip.a(picmark, url=dir+l)
        ln = ''
    else:
        a = chip.a(l,url='/cat?' + dir+l)
        mark = chip.a(textmark, url='/cat?' + dir+l)
        ln = len(map(lambda x:1,open(dir+l)))
    tm = st.st_mtime
    if recent(tm):
        tm = chip.stamp(tm)
    else:
        tm = chip.stamp(tm).format('%Y/%m/%d')
    return mark, a, tm, ln, sz

def ls(dir):
    if '..' in dir:
        print 'Location: http://cutter.ivory.ne.jp/ls\n\n'
    if not os.path.exists('./' + dir):
        print 'Location: http://cutter.ivory.ne.jp/ls\n\n'
    lst = os.listdir('./' + dir)
    if dir and not dir.endswith('/'):
        dir += '/'
    lst.sort()
    filter = open('ok.dat').read().split()
    if not dir or dir == './':
        lst = [x for x in lst if not x in filter]
    else:
        lst = ['..'] + [x for x in lst if not x in filter]
    return list(item(l, dir) for l in lst)

def lt(dir=''):
    head = [''] + map(chip.spanmint, ('filename', 'last modified', 'lines', 'size'))
    return chip.table([head]+ls(dir))(**{'class':'smaller'})

if __name__ == '__main__':
    import ppage
    ppage.ciprint(
        title = 'app.py',
    )
