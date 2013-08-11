#! /usr/bin/env python

import user
import time
from cilib.util import parse
from lamone import EL

class lamone(object):
    Tag = ''
    def __init__(self, *v, **a):
        self.lamone = EL(self.Tag)
        if v:
            self.lamone.extend(*v)
        if a:
            self.lamone.modify(**a)
    def startswith(self, s):
        return self.lamone.startswith(s)
    def __call__(self, *v, **a):
        if v:
            self.lamone.extend(*v)
        if a:
            self.lamone.modify(**a)
        return self
    def __getitem__(self, cls):
        self.lamone[cls]
        return self
    def __str__(self):
        return str(self.lamone)
    def nohead(self):
        self.lamone.nohead()
        return self

def Tag(n):
    return type(n, (lamone,), dict(Tag=n))

b = Tag('b')
p = Tag('p')
br = lambda:'\n<br>'#Tag('br')
hr = lambda:'\n<hr>'#Tag('hr')
li = Tag('li')
span = Tag('span')
link = Tag('link')
title = Tag('title')
script = Tag('script')

class a(lamone):
    def __init__(self, val, url=''):
        self.lamone = EL('a', href=url)(val)

class spancolor(span):
    Color = ''
    def __init__(self, *v, **a):
        self.lamone = EL('span')(style='color:%s'%self.Color)
        self(*v, **a)

class spangray(spancolor): Color = 'gray'
class spanred(spancolor): Color = 'red'
class spanmint(spancolor): Color = '#6b5'

class number(span):
    def __init__(self, num, mag=5):
        num = ('%5d' % num).replace(' ', '&nbsp;')
        self.lamone = EL('span', num, **{'class':'number'})

class div(lamone):
    def __init__(self, *v, **a):
        self.lamone = EL('div')(*v, **a)
        if not v:
            self.lamone('')

class stamp(lamone):
    def __init__(self, seconds=0):
        self.L = '( '
        self.R = ' )'
        self.FORMAT = '%Y/%m/%d %X'
        if seconds:
            self.time = time.localtime(seconds)
        else:
            self.time = time.localtime()
        self.lamone = span()['stamp']
    def __call__(self, L, R):
        self.L, self.R = L, R
        return self
    def format(self, a):
        self.FORMAT = a
        return self
    def stamp(self):
        return time.strftime(self.L+self.FORMAT+self.R ,self.time)
    def __str__(self):
        self.lamone(self.stamp())
        return str(self.lamone)

class time_stamp(lamone):
    def __init__(self, seconds=0, bracket_style='[]', format='%Y/%m/%d %X'):
        if seconds:
            self.time = time.localtime(seconds)
        else:
            self.time = time.localtime()
        L, R = bracket_style
        self.lamone = span()['stamp']
        self.lamone(time.strftime(L+format+R, self.time))

class nav(lamone):
    def __init__(self, sep='/', sequence=()):
        self.lamone = div()['nav']
        self.SP = '\n'+sep
        for k, v in sequence:
            self.additem(k, v)
    def additem(self, k, v):
        if len(self.lamone.lamone.stack) > 1:
            self.lamone(self.SP)
        self.lamone(a(k, url=v))

class img(lamone):
    def __init__(self, src, alt='-', width=0, height=0):
        self.lamone = EL('img')(src=src, alt=alt)
        if width:
            self.lamone(width=width)
        if height:
            self.lamone(height=height)

def xli(x):
    for y in x:
        yield li(y)

def ali(x):
    return xli(a(i,j) for i,j in x)

class ul(lamone):
    def __init__(self, x):
        self.lamone = EL('ul')(*x)

class aul(lamone):
    def __init__(self, x):
        self.lamone = ul(ali(x))

class ulist(lamone):
    def __init__(self, source):
        self.lamone = EL()
        for cat in source:
            _div = div()[cat['class']](b(cat['name']))
            _div(aul((x['name'], x['url']) for x in cat['items']))
            self.lamone(_div)

class ulparse(lamone):
    def __init__(self, source='', file=''):
        if source and file:
            raise ValueError('ambiguous call')
        elif file:
            self.lamone = ulist(parse(open(file)))
        else:
            self.lamone = ulist(parse(source))

input = Tag('input')

class submit(lamone):
    def __init__(self, value='', onclick=''):
        self.lamone = input(type='submit')
        if value:
            self.lamone(value=value)
        if onclick:
            self.lamone(onclick=onclick)

class form(lamone):
    def __init__(self, action, method='POST'):
        self.lamone = EL('form')(action=action, method=method)

class ciform(lamone):
    def __init__(self, action, value='', inputs=(), append='', onclick='', method='POST'):
        n = '\n'
        self.p = EL('p')
        for a in inputs:
            if self.p.stack:
                if 'newline' in a:
                    self.p(br())
                else:
                    self.p(n, '/')
            if 'input' in a:
                box = input(**a['input'])
            elif 'textarea' in a:
                box = textarea(**a['textarea'])
            self.p(n, a['label'], ' ', box)
        if value and onclick:
            self.p(submit(value, onclick))
        elif value:
            self.p(submit(value))
        else:
            self.p(submit())
        if append:
            self.p(append)
        self.lamone = form(action, method)(self.p)

frog_input = parse("""
- label: name
  input:
    name: name
    size: 10
    class: t
    id: name
- label: color
  input:
    name: color
    size: 10
    class: t
    id: color
- label: line
  input:
    name: line
    size: 10
    class: t
    id: line
- label: comment
  input:
    name: comment
    size: 40
  newline: 1
- label: comment
  textarea:
    name: comment
    cols: 60
    rows: 4
  newline: 1
""")

class textarea(lamone):
    def __init__(self, name, cols, rows, value=''):
        self.lamone = EL('textarea')(value, name=name, cols=cols, rows=rows)

class frog_box(lamone):
    def __init__(self, action, value, mode, onclick, line):
        inputs = frog_input
        inputs[2]['input']['value'] = line
        inputs.pop(mode and 3 or 4)
        l = action + (not mode and '?textmode=1' or '')
        mode = a(mode and 'text' or 'textarea', url=l)
        self.lamone = ciform(action, value, inputs, mode, onclick)

td = Tag('td')

class tr(lamone):
    def __init__(self, v):
        self.lamone = EL('tr')
        t = []
        for cell in v:
            if isinstance(cell, tuple):
                cell, cls = cell
                t.append(td(cell)[cls])
            else:
                t.append(td(cell))
        if t:
            self.lamone(*t)

class table(lamone):
    def __init__(self, rows, by=0, summary='.'):
        self.lamone = EL('table')('', summary=summary)
        if not by:
            self.lamone(tr(row) for row in rows)
        else:
            self.lamone(tr(row) for row in fold(rows, by))

def fold(v, n, d=''):
    b = []
    for m, x in enumerate(v):
        b.append(x)
        if m%n == n-1:
            yield b
            b = []
    if b:
        b += [d] * (n - len(b))
        yield b

def fold_(v, n, d=''):
    pass

if __name__ == '__main__':

    from cilib import ciprint
    from cilib import span
    from random import randrange, choice as c

    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    st = 'background:#%03x;font-family:terminal;padding:0px;margin:0px;'
    content = [
          [span(c(a)+c(a)+c(a))(style=st%(randrange(16**3))) for x in range(19)]
              for y in range(57)]

    ciprint(
        title = 'chip.py',
        content = table(content)(cellspacing=0)(cellpadding=0)['test'],
        separate = True,
        css = '/css/basic2',
    )
