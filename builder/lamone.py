#! /usr/bin/env python

from types import *

class Lamone:
    '''Lamone - HTML Element, version 1.01'''
    LT, GT = '<>' # left, right
    TP = '\n'
    IND = 3
    BACK = 1   # line feed before end tag, if 0 no line feed before end tag
    def __init__(self, n='', *v, **a):
        self.name = n.strip()
        self.stack = []
        self.attrs = {}
        if v:
            self.extend(*v)
        if a:
            self.modify(**a)
    def extend(self, *v):
        for x in v:
            if isinstance(x, GeneratorType):
                self.extend(*list(x))
            elif isinstance(x, ListType):
                self.extend(*x)
            elif isinstance(x, TupleType):
                self.extend(*x)
            else:
                self.stack.append(x)
    def modify(self, **a):
        for x, y in a.iteritems():
            self.attrs[x] = y
    @staticmethod
    def oneattribute(x, y):
        return ' ' + x + '="' + str(y) + '"'
    def attributes(self):
        return ''.join(self.oneattribute(x, y) for x,y in self.attrs.iteritems())
    def start_label(self):
        return self.LT + self.name + self.attributes() + self.GT
    def end_label(self):
        return self.LT + '/' + self.name + self.GT
    def startswith(self, c):
        # if self starts with n then True else False
        if c == '\n':
            if self.name:
                return self.TP == c
            else:
                return self.startswithLF()
        else:
            return str(self).startswith(c)
    def startswithLF(self):
        # if the contents of self starts with LF then True else False
        if not self.stack:
            return False
        for i in self.stack:
            if i == '':
                continue
            else:
                if hasattr(i,'startswith'):
                    return i.startswith('\n')
                else:
                    return str(i).startswith('\n')
        else:
            return False
    def backLF(self):
        return self.BACK and self.startswithLF() and '\n' or ''
    def content(self):
        return ''.join(str(x) for x in self.stack)
    def indented(self):
        return self.content().replace('\n', '\n'+' '*self.IND) + self.backLF()
    def __str__(self):
        if not self.name:
            return self.content()
        elif not self.stack:
            return self.TP + self.start_label()
        else:
            return self.TP + self.start_label() + self.indented() + self.end_label()
    def __getitem__(self, x):
        if not isinstance(x, str):
            raise TypeError('class name must be str, not %s'%type(x))
        else:
            self.attrs['class'] = x
            return self
    def __call__(self, *v, **a):
        if v:
            self.extend(*v)
        if a:
            self.modify(**a)
        return self
    def __nonzero__(self):
        return (self.name or self.stack) and 1 or 0
    def nohead(self):
        self.TP = ''

EL = Lamone

if __name__ == '__main__':
    from ppage import ciprint

    ciprint(
        separate = True,
        title = 'lamone.py',
        css = '/css/cross',
        text = open('lamone.py').read(),
    )
