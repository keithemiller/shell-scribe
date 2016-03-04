"""
Shell-Scribe run.py

@author: Keith E. Miller <keithmiller@umass.edu>

Expected issues:
- cd command is shell-scribe specific so commands that use cd in a non-trivial
way might break the cd command
"""


import cmd
import os
import sys
import argparse as ap

class Shell_Scribe(cmd.Cmd):
    """
    Shell_Scribe is a commandline interface that automatically saves a history
    of what commands were typed to a text file as well as creating a shell
    script for them.
    """

    ## Return value for each command (None == 0)
    return_value = None
    ## The prompt to the user
    prompt = "Shell-Scribe>"
    ## Set to True for Working Directory as prompt"
    location_prompt = False
    ## This is a list of commands that will not be stored by Shell-Scribe
    storage_blacklist = ["ls", "pwd"]



    ## Explicit Shell-Scribe Commands
    def do_cd(self, line):
        os.chdir(line)

    def do_exit(self, line):
        sys.exit()

    def do_quit(self, line):
        sys.exit()
    



    ## CMD Overloads
    def do_EOF(self, line):
        return True
    
    def precmd(self, line):
        return line

    def postcmd(self, stop, line):

        if self.location_prompt:
            self.prompt = os.getcwd() + " >"
        
        if self.return_value == None:
            if line not in self.storage_blacklist:
                print "Store!"

    def default(self, line):
        cmd_file = os.popen(line)
        output = cmd_file.read()
        self.return_value = cmd_file.close()
        print output
    
    def preloop(self):
        if self.location_prompt:
            self.prompt = os.getcwd() + " >"
    



if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Documents Shell-Commands")
    parser.add_argument('--location-prompt', action='store_true')
    args = parser.parse_args()
    Shell_Scribe.location_prompt = args.location_prompt
    print args
    Shell_Scribe().cmdloop()
