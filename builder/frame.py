#! /usr/bin/env python

from lamone import EL
from chip import lamone
from chip import a, br, hr, p, img, div, span, nav, stamp, time_stamp, script, link

RA_S = 'copied/'

class appbar(object):
    def __init__(self, home='/', icon='/images/py6', mark='default'):
        self.nav = nav()
        self.home = home
        self.icon = icon
        self.mark = mark
        if self.mark == 'default':
            self.rule = (1,0)
        elif self.mark == 'minimal':
            self.rule = (0,)
        elif self.mark == 'all':
            self.rule = (13,12,11,10,9,8,7,6,5,4,3,2,1,0)
        elif self.mark == 'shallow':
            self.rule = (5,6,11,2,1,13)
        elif self.mark == 'vu':
            self.rule = (10,9,6,5,2,12,1,0)
        else:
            raise Exception('illegal navigation bar name - %s' % self.mark)
        self.make()
    def make(self):
        import os
        scr = os.environ['SCRIPT_FILENAME']
        scr = scr[scr.find(RA_S)+len(RA_S):]
        pymark = img(src=self.icon, alt='source').nohead()
        navigate = (
            ('HOME', self.home),
            (pymark, '/cat?'+scr),
            ('lineBBS', '/shirakawa_st/'),
            ('mandarin', '/_mandarin/'),
            ('crm', '/betto-cho/'),
            ('css tank', '/css/'),
            ('image tank', '/images/'),
            ('a-box', '/a-box/test.py'),
            ('site map', '/sitemap.py'),
            ('mandarin forge', '/_mandarin/?forge'),
            ('crm forge', '/betto-cho/?forge'),
            ('Twice Board', '/twice/'),
            ('&#36899;&#32097;BBS', '/ren/'),
            ('shallow','/shallow'),
            ('',''),
        )
        navigate = [navigate[i] for i in self.rule]
        for i, j in navigate:
            self.nav.additem(i, j)
    def __str__(self):
        return str(self.nav)

class title_bar(lamone):
    def __init__(self, ti, pre='', post='', sub=''):
        self.lamone = div()['title']
        if pre:
            x = span(pre)(id='pretitle')['pretitle']
            self.lamone(x)
        if ti:
            x = span(ti)(id='title')['title']
            self.lamone(x)
        if post:
            x = span(post)(id='posttitle')['posttitle']
            self.lamone(x)
        if sub:
            y = br()
            x = span(sub)['transgressing']
            self.lamone(y)(x)

class head(lamone):
    def __init__(self, ti, css, js, charset):
        self.lamone = EL('head')
        meta1 = EL('meta')(**{'http-equiv':'Content-Type','content':'text/html ; charset=%s' % charset})
        self.lamone(meta1)
        ti = EL('title')(ti)
        self.lamone(ti)
        if isinstance(css, tuple) or isinstance(css, list):
            for x in css:
                sheet = link(rel='stylesheet', href=x)
                self.lamone(sheet)
        elif isinstance(css, str):
            sheet = link(rel='stylesheet', href=css)
            self.lamone(sheet)
        if isinstance(js, tuple) or isinstance(js, list):
            for x in js:
                scr = script(src=x)(type='text/javascript')('')
                self.lamone(scr)
        elif isinstance(js, str):
            scr = script(src=js)(type='text/javascript')('')
            self.lamone(scr)
            

class body(lamone):
    def __init__(self, main, home, bar, icon, title, pretitle, posttitle,
                 subtitle, separate, precontent, postcontent, sig_off, onload=''):
        self.lamone = EL('body')(id='body')
        nav = appbar(home=home, mark=bar, icon=icon)
        title = title_bar(ti=title, pre=pretitle, post=posttitle,
                          sub=subtitle)
        outdiv = div(br())
        indiv = div(hr())
        sepdiv = separate and div(hr()) or div(br())
        self.lamone(outdiv)(nav)(indiv)(title)(sepdiv)
        self.lamone(precontent)
        self.lamone(main)
        self.lamone(postcontent)
        self.lamone(indiv)(nav)(outdiv)
        if not sig_off:
            self.lamone(signature())
        if onload:
            self.lamone(onload=onload)

class html(lamone):
    def __init__(self, head, body):
        self.lamone = EL('html')(lang='ja')
        self.lamone(head)(body)

class doc(lamone):
    def __init__(self, html, charset):
        self.lamone = EL()
        n = '\n'
        self.lamone('content-type: text/html; charset=%s' % charset)(n)
        self.lamone('content-style-type: text/css')(n)
        self.lamone('content-script-type: text/javascript')(n)
        #dt = '!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'
        dt = '!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"'
        self.lamone(EL(dt))
        self.lamone(html)

class Sandwich(object):
    def __init__(self, text='', posttext='',
                 title='', subtitle='', pretitle='', posttitle='',
                 css='/css/main', separate=1,
                 content='', precontent='', postcontent='',
                 bar='default', pymark='/images/py6', js=(), onload='', charset='shift_jis', sig_off=0):
        self.main = EL('div')['main'](id='main')('')
        self.home = '/'
        self.icon = pymark
        self.charset = charset
        self.text = str(text)
        self.posttext = str(posttext)
        self.title = title
        self.subtitle = subtitle
        self.pretitle = pretitle
        self.posttitle = posttitle
        self.css = css
        self.separate = separate
        self.content = content
        self.precontent = precontent
        self.postcontent = postcontent
        self.bar = bar
        self.js = js
        self.sig_off = sig_off
        self.onload = onload
    def __str__(self):
        if self.text:
            pre = EL('pre')('%@F$&y')
            self.main(pre)
        if self.content:
            self.main(self.content)
        if self.posttext:
            pre = EL('pre')('xx$#@*')
            self.main(pre)
        hd = head(self.title, self.css, self.js, self.charset)
        bd = body(
            main = self.main,
            home = self.home,
            bar = self.bar,
            icon = self.icon,
            title = self.title,
            pretitle = self.pretitle,
            posttitle = self.posttitle,
            subtitle = self.subtitle,
            separate = self.separate,
            precontent = self.precontent,
            postcontent = self.postcontent,
            sig_off = self.sig_off,
            onload = self.onload
        )
        x = doc(html(hd, bd), charset=self.charset)
        xx = str(x)
        if self.text:
            xx = xx.replace('%@F$&y', self.text)
        if self.posttext:
            xx = xx.replace('xx$#@*', self.posttext)
        return xx

class signature(lamone):
    def __init__(self):
        br = EL('br')
        basmala = div('\n&#1576;&#1587;&#1605; &#1575;&#1604;&#1604;&#1607; &#1575;&#1604;&#1585;&#1581;&#1605;&#1606; &#1575;&#1604;&#1585;&#1581;&#1610;&#1605;')
        sakura = a('sakura internet', url='http://www.sakura.ne.jp/')
        python = a('python', url='http://www.python.org/')
        kt3k = a('kt3k', url='http://kt3k.org/')
        image_licenses = a('about image licenses', url='/images/')
        stmp = time_stamp(bracket_style=('"','" JST'))
        self.lamone = div('''
%(br)s%(basmala)s
%(br)s%(stmp)s%(br)s
%(br)s
hosted by%(sakura)s%(br)s
powered by%(python)s%(br)s
%(br)s
Copyright (C) 2005-2012%(kt3k)s
some rights reserved.%(br)s
%(br)s''' % locals())['footer']

if __name__ == '__main__':
    import ppage

    ppage.ciprint(
        title = 'frame.py',
        text = open('frame.py').read(),
        css = '/css/vanfog',
    )
