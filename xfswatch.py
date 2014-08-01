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

"""

import os, datetime, time
import sys, argparse, json
import watchdog.events, watchdog.observers

class CmdHandler(watchdog.events.PatternMatchingEventHandler):

    def __init__(self, name, cmd):
        watchdog.events.PatternMatchingEventHandler.__init__(self, ["*/"+name])
        self.cmd = cmd

    def on_created(self, event):
        filename = event.src_path
        display("File \"%s\" created." % filename)
        display("Going to execute cmd \"%s\":" % self.cmd)
        os.system(self.cmd)
        print ""

    def on_deleted(self, event):
        filename = event.src_path
        display("File \"%s\" deleted." % filename)
        display("Going to execute cmd \"%s\":" % self.cmd)
        os.system(self.cmd)
        print ""

    def on_modified(self, event):
        filename = event.src_path
        display("File \"%s\" modified." % filename)
        display("Going to execute cmd \"%s\":" % self.cmd)
        os.system(self.cmd)
        print ""

    def on_moved(self, event):
        filename = event.src_path
        display("File \"%s\" moved." % filename)
        display("Going to execute cmd \"%s\":" % self.cmd)
        os.system(self.cmd)
        print ""



def display(str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "[{0}] {1}".format(now, str)


def parse_opt():
    parser = argparse.ArgumentParser(prog='xfswatch')
    parser.add_argument('--setup', action='store_true',
            help='link xfswatch.py to /usr/local/bin/xfswatch')
    parser.add_argument('--path', action='store', nargs="+",
            help='paths for watching')
    parser.add_argument('--cmd', action='store',
            help='command')
    return parser.parse_args()

def watch(file_list, cmd):
    observer = watchdog.observers.Observer()

    for file_path in file_list:
        dir_path = os.path.dirname(file_path)
        if len(dir_path) == 0:
            dir_path = '.'
        filename = os.path.basename(file_path)
        observer.schedule(CmdHandler(filename, cmd),
                dir_path, recursive=False)
        display('Watching for path "%s".' % os.path.join(dir_path, filename))

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def setup():
    script = os.path.abspath(sys.argv[0])
    dest = '/usr/local/bin/xfswatch'
    display('Link "%s" to %s' % (script, dest))
    cmd = 'chmod +x %s && ln -s -f "%s" %s' % (script, script, dest)
    os.system(cmd)

def main():
    args = parse_opt()

    if args.setup:
        setup()
        return

    if args.cmd == None:
        display("Error: please specify command via --cmd.")
        return

    if len(args.path) == 0:
        display("Error: empty watch list")
        return

    watch(args.path, args.cmd)


if __name__ == '__main__':
    main()
