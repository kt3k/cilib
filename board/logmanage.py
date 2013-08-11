#! /usr/bin/env python

import user
import re
import os
import cgi
import time
import cilib

n = '\n'

class LogItem(object):
    def __init__(self, n, s=1, e=1, anno='', ln=0, rel=[]):
        self.name = n
        self.start = s
        self.end = e
        self.annotation = anno
        self.lines = ln
        self.related = rel
    def __str__(self):
        return str([self.name, self.start, self.end, self.annotation, self.lines, self.related])

class LogList(object):
    MAX = 1000
    def __init__(self, file):
        self.file = file
        self.data = self.read()
    def read(self):
        d = read_log(self.file)
        if d:
            d = [LogItem(*x) for x in d]
        else:
            d = self.default()
            self.save()
        return d
    def save(self):
        open(self.file, 'w').write(str(self))
    def __str__(self):
        return '\n'.join(map(str, self.data))

class CurrentList(LogList):
    MAX = 200
    def default(self):
        return [LogItem('current.dat')]
    def update(self, s, e):
        self.data[0].start = s
        self.data[0].end = e
        if self.data[0].lines < self.MAX:
            self.data[0].lines += 1
        self.save()

class ArchiveList(LogList):
    def default(self):
        return [LogItem('_.dat')]
    def update(self, l):
        self.data[-1].end = l
        self.data[-1].lines += 1
        self.save()
    def update_all(self):
        for item in self.data:
            lines = read_log(item.name)
            item.start = lines[0][1]
            item.end = lines[-1][1]
            item.lines = len(lines)
        self.save()
    def extend(self, name, time, annotation):
        if self.data[-1].annotation == annotation:
            self.data[-1].annotation = ''
        self.data.append(LogItem(name, time, time, annotation, 0))
        self.save()

class SelectList(LogList):
    LineMax = 1000
    def default(self):
        return [['s0.dat', 1, 1, '', 0, []]]
    def update(self, topic, time):
        self.data[topic - 1].end = time
        self.save()
    def full(self, topic):
        return self.data[topic - 1].lines >= self.LineMax

# note: ***Log classes don't know about log-line structures

class CurrentLog(object):
    Prefix = ''
    File = 'current'
    Line = 200
    def __init__(self):
        self.file = self.Prefix + self.File + '.dat'
        self.list = CurrentList(self.Prefix + self.File + 'list.dat')
    def read(self):
        return read_log(self.file)
    def write_and_read(self, post):
        data = self.read()
        data.append(post.to_datum())
        data = data[-self.Line:]
        open(self.file, 'w').write(frozen_log(data))
        self.list.update(data[0][1], post.time)
        return data

class CurrentSpamLog(CurrentLog):
    Prefix = 'spam'
    Line = 30

class ArchiveLog(object):
    Prefix = 'a'
    ListFile = 'list.dat'
    BoardCount = 'board_count.dat'
    LogMax = 10
    def __init__(self):
        self.cfile = self.Prefix + self.BoardCount
        self.list = ArchiveList(self.Prefix + self.ListFile)
    def write(self, post):
        open(self.next(), 'a').write(str(post.to_datum()) + '\n')
        self.list.update(post.time)
    def current(self):
        return self.Prefix + str(int_file(self.cfile)) + '.dat'
    def next(self):
        if not self.current_exists():
            self.list_extend()
            return self.current()
        elif self.current_full():
            countup(self.cfile)
            return self.next()
        return self.current()
    def current_full(self):
        return file_height(self.current()) >= self.LogMax
    def current_exists(self):
        return os.path.exists(self.current())
    def list_extend(self):
        new = self.current()
        s = int(time.time())
        a = 'latest log'
        self.list.extend(new, s, a)

class SpamArchiveLog(ArchiveLog):
    Prefix = 'spam'

class SelectLog(ArchiveLog):
    Prefix = 's'
    def __init__(self, post=()):
        self.post = post
        self.cfile = self.Prefix + self.BoardCount
        self.list = SelectList(self.Prefix + self.ListFile)
    def filename(self):
        return self.Prefix + str(self.post.topic) + '.dat'
    def read(self):
        return read_log(self.filename())
    def write_and_read(self):
        if self.list.full(self.post.topic):
            post.fail = 1
            post.warning = 'over 1000 comments'
            return self.read()
        else:
            self.write()
            self.list.update(self.post.topic, self.post.time)
            self.read()
    def write(self):
        open(self.filename(), 'a').write(str(self.post.to_datum) + '\n')

def ShirakawaList():
    a = CurrentLog().list.read()
    b = ArchiveLog().list.read()
    c = CurrentSpamLog().list.read()
    d = SpamArchiveLog().list.read()
    return a + b + c + d

def TwiceList():
    a = CurrentLog().list.read()
    b = ArchiveLog().list.read()
    c = SelectLog().list.read()
    d = CurrentSpamLog().list.read()
    e = SpamArchiveLog().list.read()
    return a + c + b + d + e

def frozen_log(data):
    return '\n'.join(map(str, data))

def read_log(file):
    try:
        data = open(file)
    except IOError:
        return []
    else:
        return exite(data)

# exite bbs-log data,
# or exite bbs-log-list data.
# if data include invalid lines, then ignore those lines.

def exite(data):
    buffer = list()
    for line in data:
        try:
            line = check_and_eval(line)
        except:
            continue
        else:
            buffer.append(line)
    return buffer

def check_and_eval(line):
    return eval(line)

def int_file(file):
    try:
        c = int(open(file).read().strip())
    except IOError:
        c = 0
    return c

def file_height(file):
    try:
        h = len(map(id, open(file)))
    except IOError:
        h = 0
    return h

def countup(file):
    count = int_file(file) + 1
    open(file, 'w').write(str(count))
