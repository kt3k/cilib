#! /usr/bin/env python

def formatescape( s ):
    return s.replace('%', '%%')

def metaescape( s ):
    for k, v in (('&','&amp;'), ('>','&gt;'), ('<','&lt;')):
        s = s.replace(k, v)
    return s

ef = formatescape
em = metaescape

if __name__ == '__main__':

    import user
    from cilib import ppage

    print ppage(title = 'escape.py',
                text = metaescape(open('escape.py').read()),
                separate = True,
                css = '/css/sky',)
