class NumberedText:
    def __init__( _, text):
        _.text = text.strip()
        _.__markup()
        _.text = _.text.split('\n')
    def __markup( _ ):
        _.text = _.text.replace('&','&amp;')
        _.text = _.text.replace('<','&lt;').replace('>','&gt;')
        d = {
             'builder': 'cilib/builder/__init__.py',
             'util': 'cilib/util/__init__.py',
             'ppage': 'cilib/builder/ppage.py',
             'app': 'cilib/builder/app.py',
             'lamone': 'cilib/builder/lamone.py',
             'chip': 'cilib/builder/chip.py',
             'frame': 'cilib/builder/frame.py',
             'yaml': 'cilib/util/yaml.py',
             'escape': 'cilib/util/escape.py',
             'web': 'cilib/web/__init__.py',
             'spam': 'cilib/web/spam.py',
             'namelist': 'cilib/web/namelist.py',
             'datamanage': 'cilib/board/datamanage.py',
             'renderer': 'cilib/board/renderer.py',
             'text' : 'cilib/builder/text.py',
             'board': 'cilib/board/__init__.py',
             'py3p': 'py3p/py3p.py',
            }
        for k, v in d.items():
            _.text = _.text.replace('from '+k,'from <a href="/cat?'+v+'">'+k+'</a>')
            _.text = _.text.replace('\nimport '+k,'\nimport <a href="/cat?'+v+'">'+k+'</a>')
        _.text = _.text.replace('from cilib', 'from <a href="/ls?cilib">cilib</a>')
        _.text = _.text.replace('\nimport cilib', '\nimport <a href="/ls?cilib">cilib</a>')
    def num( _, i ):
        return '<span class="number">'+('%5d' % i).replace(' ', '&nbsp;')+' </span>'
    def __numbering( _ ):
        _.text = [_.num(i+1) + L for i, L in enumerate(_.text)]
    def __str__( _ ):
        _.__numbering()
        _.text = '\n'.join(str(x) for x in _.text)
        return _.text
