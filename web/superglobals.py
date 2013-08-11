#! /usr/bin/env python

import cgitb;cgitb.enable()
import os
import cgi
import pprint
import cookielib
#import session

class SuperGlobals(object):
    def __init__(self):
        self.method = os.environ['REQUEST_METHOD']
        self.server = os.environ
        arg = {}
        f = cgi.FieldStorage()
        for k in f:
            arg[k] = f.getfirst(k)
        self.arg = arg
        self.f = f

G = SuperGlobals


if __name__ == '__main__':
    g = G()
    import user
    import cilib
    cilib.ciprint(
        text = str(g.arg),
    )
