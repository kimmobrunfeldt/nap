#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: python make-release.py [bump]

bump parameter is optional, default is patch. Valid values are patch, minor, major.

Copied from: https://raw.githubusercontent.com/mitsuhiko/flask/master/scripts/make-release.py

make-release
~~~~~~~~~~~~

Helper script that performs a release.  Does pretty much everything
automatically for us.

:copyright: (c) 2014 by Armin Ronacher.
:license: BSD, see LICENSE for more details.
"""
import sys
import os
import re
from subprocess import Popen, PIPE


def bump_version(version, bump='patch'):
    """patch: patch, minor, major"""
    try:
        parts = map(int, version.split('.'))
    except ValueError:
        fail('Current version is not numeric')

    if bump == 'patch':
        parts[2] += 1
    elif bump == 'minor':
        parts[1] += 1
        parts[2] = 0
    elif bump == 'major':
        parts[0] +=1
        parts[1] = 0
        parts[2] = 0

    return '.'.join(map(str, parts))


def set_filename_version(filename, version_number, pattern):
    changed = []
    def inject_version(match):
        before, old, after = match.groups()
        changed.append(True)
        return before + version_number + after
    with open(filename) as f:
        contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
                          inject_version, f.read())

    if not changed:
        fail('Could not find %s in %s', pattern, filename)

    with open(filename, 'w') as f:
        f.write(contents)


def set_init_version(version):
    info('Setting __init__.py version to %s', version)
    set_filename_version('nap/__init__.py', version, '__version__')


def set_setup_version(version):
    info('Setting setup.py version to %s', version)
    set_filename_version('setup.py', version, 'version')


def build_and_upload():
    Popen([sys.executable, 'setup.py', 'release', 'sdist', 'upload']).wait()


def fail(message, *args):
    print('Error: %s' % (message % args))
    sys.exit(1)


def info(message, *args):
    print('-> %s' % (message % args))


def get_git_tags():
    return set(Popen(['git', 'tag'], stdout=PIPE).communicate()[0].splitlines())


def git_is_clean():
    return Popen(['git', 'diff', '--quiet']).wait() == 0


def git_push():
    info('git push')
    return Popen(['git', 'push']).wait()


def git_push_tags():
    info('git push --tags')
    return Popen(['git', 'push', '--tags']).wait()


def make_git_commit(message, *args):
    message = message % args
    Popen(['git', 'commit', '-am', message]).wait()


def make_git_tag(tag):
    info('Tagging "%s"', tag)
    Popen(['git', 'tag', tag]).wait()


def main():
    bump = 'patch'
    # If bump parameter is specified
    if len(sys.argv) > 1:
        bump = sys.argv[1]
        if bump not in ['patch', 'minor', 'major']:
            print('bump parameter is incorrect')
            print('possible values: patch, minor major')
            sys.exit(1)

    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    import nap

    current_version_dev = nap.__version__
    if current_version_dev.endswith('-dev'):
        current_version = current_version_dev[:-len('-dev')]
    else:
        fail('Current version is not dev, %s' % current_version_dev)

    new_version = bump_version(current_version, bump=bump)
    dev_version = new_version + '-dev'

    info('Releasing %s', new_version)
    tags = get_git_tags()

    if new_version in tags:
        fail('Version "%s" is already tagged', new_version)

    if not git_is_clean():
        fail('You have uncommitted changes in git')

    set_init_version(new_version)
    set_setup_version(new_version)
    make_git_commit('Bump version number to %s', new_version)
    make_git_tag(new_version)
    git_push()
    git_push_tags()
    set_init_version(dev_version)
    set_setup_version(dev_version)
    make_git_commit('Set development version: %s', dev_version)


if __name__ == '__main__':
    main()
