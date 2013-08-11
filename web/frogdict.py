
import keyword
import re

def isidentifier(s):
    if not isinstance(s, str):
        return False
    return True

class frogdict(dict):
    def __init__(self, v=(), **kwargs):
        super(frogdict, self).__init__(v, **kwargs)
        for k, v in self.iteritems():
            if isidentifier(k) and k not in keyword.kwlist:
                exec 'self.%s = v' % k
