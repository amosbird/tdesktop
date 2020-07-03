#!/usr/bin/env python3

import os, sys, re
from subprocess import call, Popen, PIPE
from os.path import expanduser

changelog_file = '../../changelog.txt'
token_file = '../../../DesktopPrivate/github-releases-token.txt'

version = '2.1.11'
def getOutput(command):
  p = Popen(command.split(), stdout=PIPE)
  output, err = p.communicate()
  if err != None or p.returncode != 0:
    print('ERROR!')
    print(err)
    print(p.returncode)
    sys.exit(1)
  return output.decode('utf-8')

def prepareSources():
  os.chdir('Telegram/build')
  workpath = os.getcwd()
  os.chdir('../..')
  rootpath = os.getcwd()
  finalpath = "/home/amos/gentoo/var/cache/distfiles/tdesktop-2.1.11-full.tar"
  if os.path.exists(finalpath):
    os.remove(finalpath)
  if os.path.exists(finalpath + '.gz'):
    os.remove(finalpath + '.gz')
  tmppath = rootpath + '/out/Release/tmp.tar'
  print('Preparing source tarball...')
  if (call(('git archive --prefix=tdesktop-' + version + '-full/ -o ' + finalpath + ' HEAD').split()) != 0):
    os.remove(finalpath)
    sys.exit(1)
  lines = getOutput('git submodule foreach').split('\n')
  for line in lines:
    if len(line) == 0:
      continue
    match = re.match(r"^Entering '([^']+)'$", line)
    if not match:
      print('Bad line: ' + line)
      sys.exit(1)
    path = match.group(1)
    revision = getOutput('git rev-parse HEAD:' + path).split('\n')[0]
    print('Adding submodule ' + path + '...')
    os.chdir(path)
    if (call(('git archive --prefix=tdesktop-' + version + '-full/' + path + '/ ' + revision + ' -o ' + tmppath).split()) != 0):
      os.remove(finalpath)
      os.remove(tmppath)
      sys.exit(1)
    if (call(('gtar --concatenate --file=' + finalpath + ' ' + tmppath).split()) != 0):
      os.remove(finalpath)
      os.remove(tmppath)
      sys.exit(1)
    os.remove(tmppath)
    os.chdir(rootpath)
  print('Compressing...')
  if (call(('gzip -9 ' + finalpath).split()) != 0):
    os.remove(finalpath)
    sys.exit(1)
  os.chdir(workpath)
  return finalpath + '.gz'

prepareSources()
