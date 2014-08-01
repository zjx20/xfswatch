xfswatch
========

A tool that run specified command whenever changes of target files was detected

Install
-------

    git clone https://github.com/zjx20/xfswatch.git
    cd xfswatch
    python xfswatch.py --setup

Usage
-----

    usage: xfswatch [-h] [--setup] [--path PATH [PATH ...]] [--cmd CMD]

    optional arguments:
      -h, --help            show this help message and exit
      --setup               link xfswatch.py to /usr/local/bin/xfswatch
      --path PATH [PATH ...]
                            paths for watching
      --cmd CMD             command

Examples
--------

    xfswatch --path ./dir1 ./file1 --cmd "ls -al"
