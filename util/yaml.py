#! /usr/bin/env python

class IndentationChecker(object):
    def __init__( _ ):
        _.stack = []
    def append( _, n, k ):
        _.stack.append((n,k))
    def pop( _, n, k ): # k means 'kind'
        if (n, k) not in _.stack:
            raise IndentationError, 'unindent does not match any outer indentation level'
        else:
            while _.stack[-1][0] > n:
                yield _.stack.pop()
    def check( _, n, k ):
        if not _.stack:
            if n > 0:
                raise Execption, 'first entry must be in column 0'
            else:
                _.append(n, k)
                yield Token('INDENT', k)
                return
        p = _.stack[-1]
        if p == (n, k):
            pass
        elif p[0] < n:
            _.append(n, k)
            yield Token('INDENT', k)
        elif p[0] > n:
            for x in _.pop(n, k):
                yield Token('DEDENT', x[1])
        else:
            raise Exception, 'invalid entry indentation, %s, %s, %s'%(n,k,_.stack)
    def end( _ ):
        for x in reversed(_.stack):
            yield Token('DEDENT', x[1])

class Token(object):
    def __init__( _, id, attr ):
        _.id = id
        _.attr = attr
    def __str__( _ ):
        return 'Token, %s, %s'%(_.id, _.attr)
    def py( _ ):
        if _.id == 'INDENT' and _.attr == 'd': return '{'
        if _.id == 'DEDENT' and _.attr == 'd': return '},'
        if _.id == 'INDENT' and _.attr == 'l': return '['
        if _.id == 'DEDENT' and _.attr == 'l': return '],'
        if _.id == 'key': return `_.attr` + ':'
        else: return `_.attr` + ','

def tokenize( lines ):
    ic = IndentationChecker() # indentation level stack
    for line in lines:
        if ':' in line:
            if line.strip().startswith('-'):
                n = 0
                while line.startswith(' '):
                    line = line[1:]
                    n += 1
                for token in ic.check(n, 'l'):
                    yield token
                line = line[1:]
                n += 1
                while line.startswith(' '):
                    line = line[1:]
                    n += 1
                for token in ic.check(n, 'd'):
                    yield token
                key, rest = line.split(':', 1)
                key = key.strip()
                rest = rest.strip()
                yield Token('key', key)
                if rest:
                    yield Token('scalar', rest)
            else:
                n = 0
                while line.startswith(' '):
                   line = line[1:]
                   n += 1
                for token in ic.check(n, 'd'):
                    yield token
                key, rest = line.split(':', 1)
                key = key.strip()
                rest = rest.strip()
                yield Token('key', key)
                if rest:
                    yield Token('scalar', rest)
        else:
            if line.strip().startswith('-'):
                n = 0
                while line.startswith(' '):
                    line = line[1:]
                    n += 1
                for token in ic.check(n, 'l'):
                    yield token
                yield Token('scalar', line.strip())
            else:
                raise FormError, 'ill-formed yaml'
    for token in ic.end():
        yield token

def compose(s):
    return eval(''.join(x.py() for x in s))[0]

def parse(s='', file=''):
    if s and file:
        raise Exception('cilib.util.parse : ambiguous call')
    elif file:
        return compose(tokenize(open(file)))
    else:
        if isinstance(s, str):
            return compose(tokenize(s.strip().split('\n')))
        else:
            return compose(tokenize(s))

if __name__ == '__main__':
    import user
    from cilib import ciprint
    from pprint import pformat

    source = '../../index.yml'
    text = open(source).read()
    l = list(tokenize(open(source)))
    tokens = '\n'.join(str(x)for x in l)
    sep1 = '\n\n     vvv tokenize vvv\n\n\n'
    sep2 = '\n\n\n     vvv compose vvv\n\n\n'
    text += sep1 + tokens + sep2 + pformat(parse(open(source)))

    ciprint(
        text = text,
        title = 'yaml.py',
        subtitle = '- nothing -',
        separate = True,
        css = '/css/cross',
    )
