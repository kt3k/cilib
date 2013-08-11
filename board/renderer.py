#! /usr/bin/env python

import user
import cilib
import time
from pprint import pformat

n = '\n'
now = int(time.time())

def recent(then):
    return abs(now - then) < 172800

def shirakawa_log_line(l):
    name, time, col, comment = l
    a = cilib.span(name, style='color:'+col)
    b = cilib.span(comment, style='color:'+col)
    c = cilib.stamp(time)(*'()').format('%m/%d(%a) %X')
    return cilib.p(a, ' &gt; ', b, c)

def shirakawa_archive_log_line(l):
    name, time, col, comment = l
    a = cilib.span(name, style='color:'+col)
    b = cilib.span(comment, style='color:'+col)
    c = cilib.stamp(time)(*'[]').format('%Y/%m%d(%a) %X')
    return cilib.p(a, ' &gt; ', b, c)

#ColorTable = ['#cca','#cac','#acc','#caa','#aac','#aca','#ace','#dca','#acd',]
ColorTable = ['#561','#516','#156','#512','#125','#152','#158','#851','#185',]

def twice_log_line(l):
    name, time, topic, comment = l
    if topic:
        col = ColorTable[topic%len(ColorTable)]
    else:
        col = 'black'
    a = cilib.span(name, style='color:'+col)
    b = cilib.span(str(topic), style='color:'+col)
    c = cilib.span(comment, style='color:'+col)
    d = cilib.stamp(time)(*'[]').format('%Y/%m/%d(%a) %X')
    return cilib.p(a, ' &gt; ', b,' &gt; ', c, d)

class ShirakawaBoard(object):
    TITLE = 'Shirakawa Board'
    def __init__(self, data, line, textmode):
        self.data = data
        self.line = max((min((line, 200)), 1))
        self.textmode = textmode
    def render(self):
        ciform = cilib.frog_box(action = './',
                                value = 'submit',
                                mode = self.textmode,
                                onclick = 'setcookie();',
                                line = self.line)
        lnk = cilib.a('Log List', url='./list')
        cilib.ciprint(
            title = self.TITLE,
            subtitle = cilib.span('\n--->', lnk),
            js = '/js/frog',
            pymark = '/images/py.gif',
            bar = 'shallow',
            content = (shirakawa_log_line(l) for l in self.data[-self.line:]),
            postcontent = (cilib.div(cilib.hr()), ciform),
            onload = 'getcookie();',
        )

class TwiceBoard(object):
    TITLE = 'Shirakawa Board'
    def __init__(self, data, line, textmode):
        self.data = data
        self.line = max((min((line, 200)), 1))
        self.textmode = textmode
    def render(self):
        ciform = cilib.frog_box(action = './',
                                value = 'submit',
                                mode = self.textmode,
                                onclick = 'setcookie();',
                                line = self.line)
        lnk = cilib.a('Log List', url='./list')
        cilib.ciprint(
            title = self.TITLE,
            subtitle = cilib.span('\n--->', lnk),
            js = '/js/frog',
            pymark = '/images/py.gif',
            bar = 'shallow',
            content = (twice_log_line(l) for l in self.data[-self.line:]),
            postcontent = (cilib.div(cilib.hr()), ciform),
            onload = 'getcookie();',
        )

class BoardBrowse:
    log_line = staticmethod(shirakawa_archive_log_line)
    def __init__(self, data, log_name):
        self.data = data
        self.log_name = log_name
    def render(self):
        log = (self.log_line(l) for l in self.data)
        d = zip(map(cilib.number, xrange(1,len(self.data)+1)), log)
        numbered_log = cilib.table(d)(**{'class':'log'})
        lnk = cilib.a('return to Log List', url='./list')
        cilib.ciprint(
            title = 'Log : "%s"' % self.log_name ,
            subtitle = ('\n--->', lnk),
            pymark = '/images/py.gif',
            bar = 'shallow',
            content = numbered_log,
        )

class tBoardBrowse(BoardBrowse):
    log_line = staticmethod(twice_log_line)

logmark = cilib.img(src='/images/silktext')
diskmark = cilib.img(src='/images/silkdisk')
servermark = cilib.img(src='/images/silkserver')

def thread_row(d):
    name = d.name
    start = d.start
    end = d.end
    anno = d.annotation
    lines = d.lines
    rel = d.related or '-'
    lfmt = '%Y/%m/%d' + recent(end)*' %X'
    sfmt = '%Y/%m/%d' + recent(start)*' %X'
    if anno:
        anno = cilib.spangray(' - ' + anno)
    mark = cilib.a(diskmark, url='browse?'+str(name))
    sp = cilib.span(cilib.a(name, url='browse?'+str(name)),n, anno)
    return (
        mark, sp,
        cilib.stamp(start).format(sfmt),
        cilib.stamp(end).format(lfmt),
        lines, rel,
    )

class ShirakawaBoardList(object):
    def __init__(self, rows):
        head_row = [''] + map(cilib.spanmint, ('log name', 'started',
                                               'last posted', 'lines', 'related'))
        self.rows = [head_row] + map(thread_row, rows)
    def render(self):
        a = cilib.a('return to board', url='./')
        cilib.ciprint(
            title = 'Log Archive',
            subtitle = (n,'--->',a),
            content = cilib.table(self.rows)(**{'class':'smaller'}),
        )

class TwiceBoardList(object):
    def __init__(self, data, t_data):
        self.data = data
        self.t = t_data
    def render(self):
        pass
