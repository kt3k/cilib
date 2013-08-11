#! /usr/bin/env python

from lamone import EL
from frame import Sandwich

def ciprint(**args):
    print Sandwich(**args)

if __name__ == '__main__':

    ciprint(
        text = open('ppage.py').read(),
        title = 'ppage.py',
    )
