def spam(s):
    if fullascii(s):
        return True
    elif obvious(s):
        return True
    elif words(s) > 4:
        return True
    else:
        return False

def words(s):
    num = s.count
    level1 = ('free',
              'cheep',
              'ticket',
              'sex',
              'adult',
              'nude',
              'porno',
              'movie',
              'video',
              'finnan',
              'http',
              'href',
              'ringtone',
              'google',
              'disney',
              'Very',
              'Good',
              'Site',
              'Thank',
              'Nice',
              'Hi!',)
    return sum(num(word) for word in level1)

def obvious(s):
    level2 = (
        '[/url]',
        'kandyyy.webng.com',
        'freecities.com',
        'peace.com',
        'End ^)',
    )
    for word in level2:
        if word in s:
            return True
    else:
        return False

def fullascii(s):
    for c in s:
        if ord(c) > 127:
            return False
    else:
        return True
