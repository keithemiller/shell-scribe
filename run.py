"""
Shell-Scribe run.py

@author: Keith E. Miller <keithmiller@umass.edu>

"""


import cmd
import os
import sys

class ShellEnabled(cmd.Cmd):
    
    """
    def do_shell(self, line):
        "Run a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output
    """

    def do_exit(self, line):
        sys.exit()

    def do_quit(self, line):
        sys.exit()
    
    def do_EOF(self, line):
        return True
    
    def default(self, line):
        print "DEFAULT"
        output = os.popen(line).read()
        print output

if __name__ == '__main__':
    ShellEnabled().cmdloop()
