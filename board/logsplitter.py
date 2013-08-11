
def color_generator():
    table = ['#561', '#516', '#156', '#512', '#125', '#152', '#158', '#851', '#185']
    while 1:
        for color in table:
            yield color

class Thread(object):

    def __init__(self, file):
        self.file = file
        try:
            self.dict = eval(open(file).read())
        except:
            self.dict = {}
        if 0 not in self.dict:
            self.dict[0] = {'thread_count':0, 'color_table': ['#561', '#516', '#156', '#512', '#125', '#152', '#158', '#851', '#185']}

    def save(self):
        open(self.file, 'w').write(str(self.dict))

    def import_log(self, name, data, color=None):
        assert name not in self.dict
        assert data

        buf = {'color': color, 'list': []}
        buf['start'] = data[0][1]
        buf['last'] = data[-1][1]

        while data:
            segment = data[:1000]
            data = data[1000:]

            file = '%s.dat' % segment[0][1]
            buf['list'].append(file)
            open(file, 'w').write('\n'.join(map(str, segment)))

        buf['count'] = len(segment)
        buf['current'] = file
        self.dict[name] = buf
        self.dict[0]['thread_count'] += 1

    def write(self, post):
        if post.thread not in self.dict:
            post.failed = True
            post.errno = 1
            post.msg = 'No such thread: %s' % post.thread
            return

        thread = self.dict[post.thread]
        if thread['count'] >= 1000:
            self.new_file(post)

        file = thread['current']
        thread['count'] += 1
        thread['last'] = post.time
        open(file, 'a').write(post.to_a())

    def new_file(self, post):
        thread = self.dict[post.thread]
        file = '%s.dat' % post.time
        thread['current'] = file
        thread['list'].append(file)
        thread['count'] = 0

    def new_thread(self, query):
        if query.name in self.dict:
            query.failed = True
            query.errno = 1
            query.msg = 'Thread %s already exists.' % query.name
            return

        buf = {'color': query.color, 'count': 1000, 'list': [], 'start': query.time, 'last': query.time}
        self.dict[name] = buf
        self.dict[0]['thread_count'] += 1


def twice2NT_line(line):
    name, time, thread, comment = line
    if name.startswith('kt'):
        color = '#115588'
    else:
        color = 'black'
    return name, time, color, comment

def shirakawa_sergery():
    thread = Thread(file='log.dat')
    data = map(eval, open('raw.dat'))
    thread.import_log(name='0', data=data)
    data = map(eval, open('spamraw.dat'))
    thread.import_log(name='spam', data=data)
    thread.save()

def twice_sergery():
    thread = Thread(file='log.dat')
    #data = map(eval, open('spamraw.dat'))
    #thread.import_log(name='spam', data=data)

    data = map(eval, open('raw.dat'))
    
    d = {}
    for line in data:
        name, time, thr, comment = line
        new_line = twice2NT_line((name, time, thr, comment))
        if thr not in d:
            d[thr] = [new_line]
        else:
            d[thr].append(new_line)

    r = d.keys()
    r.sort()

    for c, k in zip(color_generator(), r):
        if k == 0:
            c = None
        thread.import_log(name=str(k), data=d[k], color=c)

    thread.save()
