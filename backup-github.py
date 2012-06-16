#!/usr/bin/env python
import sys
import urllib2
import os
import os.path
from pipes import quote

try:
    import json
except ImportError:
    import simplejson as json

if len(sys.argv) != 3:
    print "Usage: %s <username> <directory>" % sys.argv[0]
    sys.exit(2)

(username, backupdir) = sys.argv[1:]
if not os.path.isdir(backupdir):
    print "Error: '%s' does not exist or is not a directory" % backupdir
    sys.exit(3)

f = urllib2.urlopen('https://api.github.com/users/%s/repos' % username)
repos = json.load(f)

for repo in repos:
    dir = os.path.join(backupdir, os.path.basename(repo['name']))
    cwd = os.getcwd()
    if not os.path.exists(dir):
        print "adding new repository: %s" % repo['git_url']
        os.mkdir(dir)
        os.chdir(dir)
        os.system('git --bare init')
        os.system('git remote add --mirror origin %s' % quote(repo['git_url']))
    else:
        os.chdir(dir)

    os.system('git fetch -q')
    os.system('git remote prune origin')
    os.chdir(cwd)

