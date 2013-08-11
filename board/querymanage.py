#! /usr/bin/env python

import user
import re
import os
import cgi
import time
import cilib
import logmanage

n = '\n'

class Post(object):
    def __init__(self, form):
        self.name = Name(form)
        self.comment = MyComment(form)
        self.color = form.get('color', 'black')
        self.time = int(time.time())
    def is_spam(self):
        if not self.name.islisted() and self.comment.is_spam():
            self.detect()
            self.sanitize()
            return True
        else:
            self.sanitize()
            return False
    def nocomment(self):
        return self.comment.nocomment()
    def multiline(self):
        return self.comment.multiline()
    def to_datum(self):
        # returns tuple because line-log will never change in future
        return (
            str(self.name),
            self.time,
            str(self.color),
            str(self.comment),
        )
    def detect(self):
        self.comment.detect(self.color)
    def sanitize(self):
        self.name.sanitize()
        self.comment.sanitize()

class tPost(Post):
    def __init__(self, form):
        self.name = Name(form)
        self.comment = MyComment(form)
        self.topic = form.get('topic', 0)
        self.time = int(time.time())
    def detect(self):
        self.comment.detect()
    def to_datum(self):
        return (
            str(self.name),
            self.time,
            self.topic,
            str(self.comment)
        )

class Comment(object):
    def __init__(self, form):
        self.comment = form.get('comment', '')
    def sanitize(self):
        self.comment = self.comment.replace('<', '&lt;').replace('>', '&gt;')
        self.comment = self.comment.replace('\r' ,'').replace('\t', '    ')
        if self.multiline():
            self.comment = self.comment.replace(n, '<br>')
            self.comment = self.comment.replace('><', '> <')
            self.comment = '<pre>' + self.comment + '</pre>'
        self.comment = re.sub(r'&lt;(img .*)&gt;', r'<\1>', self.comment)
    def multiline(self):
        return n in self.comment
    def detect(self):
        pass
    def is_spam(self):
        return cilib.spam(self.comment)
    def nocomment(self):
        return self.comment == ''
    def __str__(self):
        return self.comment

class MyComment(Comment):
    def detect(self, color=''):
        self.comment += '\n'
        self.comment += '\nREMOTE_ADDR: ' + os.environ.get('REMOTE_ADDR', 'no info')
        self.comment += '\nUSER_AGENT: ' + os.environ.get('HTTP_USER_AGENT', 'no info')
        if color:
            self.comment += '\n' + 'color: ' + color
        
class Name(object):
    def __init__(self, form):
        self.name = form.get('name', 'Jabberwocky')
    def islisted(self):
        return self.name in cilib.namelist
    def sanitize(self):
        self.name = self.name.replace('<', '&lt;').replace('>', '&gt;')
        self.name = self.name.replace('\r', '').replace('\n', '')
    def __str__(self):
        return self.name

class MyForm(object):
    def __init__(self):
        self.form = cgi.FieldStorage()
    @staticmethod
    def number(s, default):
        return s and s.strip().isdigit() and int(s) or default
    def get(self, i, k):
        if isinstance(k, int):
            return self.number(self.form.getvalue(i), k)
        elif isinstance(k, str):
            return self.form.getvalue(i, k)

class ShirakawaQuery(object):
    def __init__(self):
        self.form = MyForm()
    @staticmethod
    def method_post():
        return os.environ['REQUEST_METHOD'] == 'POST'
    def process(self):
        post = Post(self.form)
        if not self.method_post() or post.nocomment():
            self.data = logmanage.CurrentLog().read()
        elif post.is_spam():
            logmanage.CurrentSpamLog().write_and_read(post)
            logmanage.SpamArchiveLog().write(post)
            self.data = logmanage.CurrentLog().read()
        else:
            self.data = logmanage.CurrentLog().write_and_read(post)
            logmanage.ArchiveLog().write(post)
        self.line = self.form.get('line', 17)
        self.textmode = self.form.get('textmode', 0)

class TwiceQuery(ShirakawaQuery):
    def process(self):
        post = tPost(self.form)
        if not self.method_post() or post.nocomment():
            self.data = logmanage.CurrentLog().read()
        elif post.is_spam():
            logmanage.CurrentSpamLog().write_and_read(post)
            logmanage.SpamArchiveLog().write(post)
            self.data = logmanage.CurrentLog().read()
        else:
            self.data = logmanage.CurrentLog().write_and_read(post)
            if not post.topic:
                logmanage.ArchiveLog().write(post)
            else:
                self.data = logmanage.SelectLog().write_and_read(post)
        self.line = self.form.get('line', 17)
        self.textmode = self.form.get('textmode', 0)

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
