#!/usr/bin/env python
"""
xfswatch.py by zjx20
http://github.com/zjx20/xfswatch/

This script will watch a set of local path and on change will
run specified command. The script can be easily modified
to do whatever you want on a change event.

requires: pip install watchdog

  about watchdog:
    # project site: http://github.com/gorakhargosh/watchdog
    # api document: https://pythonhosted.org/watchdog/index.html

TODO: support "{file}" place holder of parameter in cmd string,
    replace with the path of the changed file
"""

import os
import datetime
import time
import sys
import argparse
import json
import watchdog.events
import watchdog.observers


try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


class CmdHandler(watchdog.events.PatternMatchingEventHandler):

    def __init__(self, name, cmd):
        pattern = ['*'] if name == '' else ['*/' + name]
        watchdog.events.PatternMatchingEventHandler.__init__(self, pattern)
        self.cmd = cmd

    def on_created(self, event):
        display('File "%s" was created.' % event.src_path)
        display('Going to execute cmd "%s": ' % self.cmd)
        os.system(self.cmd)
        print ''

    def on_deleted(self, event):
        display('File "%s" was deleted.' % event.src_path)
        display('Going to execute cmd "%s": ' % self.cmd)
        os.system(self.cmd)
        print ''

    def on_modified(self, event):
        display('File "%s" was modified.' % event.src_path)
        display('Going to execute cmd "%s": ' % self.cmd)
        os.system(self.cmd)
        print ''

    def on_moved(self, event):
        display('File "%s" was moved to %s.' % (event.src_path,
                                                event.dest_path))
        display('Going to execute cmd "%s": ' % self.cmd)
        os.system(self.cmd)
        print ''


def display(str):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '[{0}] {1}'.format(now, str)


def parse_opt():
    parser = argparse.ArgumentParser(prog='xfswatch')
    parser.add_argument('--setup', action=SetupAction, nargs=0,
                        help='link xfswatch.py to /usr/local/bin/xfswatch')
    parser.add_argument('path', action='store', nargs='+',
                        help='path to be monitored, dir or file')
    parser.add_argument('--cmd', action='store', required=True,
                        help='command')
    return parser.parse_args()


def watch(file_list, cmd):
    observer = watchdog.observers.Observer()

    for file_path in file_list:
        if file_path == '.' or file_path == '..':
            file_path = file_path + '/'
        dir_path = os.path.dirname(file_path)
        if len(dir_path) == 0:
            dir_path = '.'
        filename = os.path.basename(file_path)
        observer.schedule(CmdHandler(filename, cmd),
                          dir_path, recursive=False)
        display('Monitoring path "%s".' % os.path.join(dir_path, filename))

    observer.start()
    try:
        print 'Press "space" to execute command manually.'
        while True:
            ch = getch()
            if ord(ch) == 3:
                # ctrl-c
                break
            elif ch == ' ':
                os.system(cmd)
    finally:
        observer.stop()
    observer.join()


class SetupAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        script = os.path.abspath(sys.argv[0])
        dest = '/usr/local/bin/xfswatch'
        display('Link "%s" to %s' % (script, dest))
        cmd = 'chmod +x %s && ln -s -f "%s" %s' % (script, script, dest)
        ret = os.system(cmd)
        if ret != 0:
            parser.error('Failed.')
        else:
            parser.exit()


def main():
    args = parse_opt()
    watch(args.path, args.cmd)


if __name__ == '__main__':
    main()
