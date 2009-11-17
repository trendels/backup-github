#!/usr/bin/env python
import sys
import urllib2
import xml.dom.minidom
import os
import os.path
from pipes import quote

if len(sys.argv) != 3:
    print "Usage: %s <username> <directory>" % sys.argv[0]
    sys.exit(2)

(username, backupdir) = sys.argv[1:]

f = urllib2.urlopen('http://github.com/api/v2/xml/repos/show/%s' % username)
doc = xml.dom.minidom.parse(f)

for node in doc.getElementsByTagName('repository'):
    reponame = node.getElementsByTagName('name')[0].childNodes[0].data
    url = 'git://github.com/%s/%s.git' % (username, reponame)
    dir = os.path.join(backupdir, os.path.basename(reponame))
    cwd = os.getcwd()
    if not os.path.exists(dir):
        print "adding new repository: %s" % url
        os.mkdir(dir)
        os.chdir(dir)
        os.system('git --bare init')
        os.system('git remote add --mirror origin %s' % quote(url))
    else:
        os.chdir(dir)

    os.system('git fetch -q')
    os.system('git remote prune origin')
    os.chdir(cwd)

