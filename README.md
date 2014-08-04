xfswatch
========

A tool that run specified command whenever changes of target files was detected.

Install
-------

```bash
sudo yum install libyaml libyaml-devel  # for watchdog
sudo pip install watchdog
git clone https://github.com/zjx20/xfswatch.git
cd xfswatch
sudo python xfswatch.py --setup
```

Usage
-----

    usage: xfswatch [-h] [--setup] --cmd CMD path [path ...]

    positional arguments:
      path        path to be monitored, dir or file

    optional arguments:
      -h, --help  show this help message and exit
      --setup     link xfswatch.py to /usr/local/bin/xfswatch
      --cmd CMD   command

Examples
--------

```bash
xfswatch ./dir1 ./dir2 --cmd "ls -al"

xfswatch ./dir1 ./file1 ./file2 --cmd "echo foo"

xfswatch *.txt --cmd "cat *.txt"

# auto compile and run
xfswatch ./foo.h ./foo.cpp ./bar/def.h --cmd "make && ./t_foobar"
```

Why xfswatch?
-------------

There are many alternates of ```xfswatch``` such as [fswatch](https://github.com/alandipert/fswatch) and
[watchmedo](https://github.com/gorakhargosh/watchdog/blob/master/src/watchdog/watchmedo.py) in ```watchdog```.
Actually, ```xfswatch``` was inspired by ```fswatch```. I don't use ```fswatch``` because I can't compile it
on CentOS 6.5 with the default compiler toolchain. ```watchmedo``` is a wonderful tool that can be used to
 take care of all tasks about file system monitoring. However, it was designed to watch for directories, so
 it is not convenient enough for monitoring files (can be achieved by ```--pattern``` parameter anyway).
