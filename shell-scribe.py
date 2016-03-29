#!/usr/bin/python
"""
.. module:: shellscribe
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
import datetime
import json
from twilio.rest import TwilioRestClient


## Set to false to get rid of debug print statements
DEBUG = False

### PASTE FUNCTION DEFINITIONS HERE
                                                                       
def bashinator_9000(filename):

    dic={}
    inc=1
    title = ''
    author = ''
    date = datetime.datetime.now()
    title  = raw_input("What is the title: ")
    author = raw_input("Who is the author: ")
    dic['welcome']= raw_input("Input a description for the lesson: ")
    date   = datetime.datetime.now()
    if title =="": title = 'lesson'
    if author=="": author = 'N/A'

    dic["title"] = title
    dic["author"] = author

    with open(filename,'r') as file:
              for row in file:
                    print '\033[91m' + "\nCode for the row: " + '\033[96m' + row + '\033[92m'
                    comment=raw_input('- ')
                    tempDic = {'comment':comment,'command':row}
                    dic.update({inc:tempDic})
                    inc+=1
    
    print('\033[0m')
    dic['command_count'] = inc - 1

    with open(title+'.json','w') as file:
              json.dump(dic,file)

def bashinator_10000(filename): #need sleeeeeep
    #fname = filename.readFile() #attempting to have json file read-in 
    with open(filename, 'r') as f:
        json_dict = json.load(f)
    print json_dict
    inc=1

    # Welcomes them to Hell
    print json_dict["welcome"], "\n"

    for x in range(json_dict["command_count"]):
        x = x + 1
        print '\033[91m' +"Line: ", x,'\n'
        print '\033[92m'+ "Comment: ", json_dict[str(x)]["comment"],'\n'
        print '\033[96m' + "Input: ", json_dict[str(x)]["command"][:-1]
        outfile = os.popen(json_dict[str(x)]["command"])
        output = outfile.read()
        return_val = outfile.close()
        if return_val != None:
            shell-scribe().send_call()
        print '\033[93m' + "Output: ", os.popen(json_dict[str(x)]["command"]).read() + '\033[0m'
        raw_input("-Press Enter-\n")
    #not sure what to do with the rest of this code. whether or not it is even necessary
    #with open('test.sh','r') as file:
    #          for row in file:
    #                print '\033[91m' + "\nCode for the row: " + '\033[96m' + row + '\033[92m'
    #                comment=raw_input('- ')
    #                tempDic = {'comment':comment,'command':row}
    #                dic.update({inc:tempDic})
    #                inc+=1
    #dic['welcome']="""This is a welcome message"""
    #print('\033[0m')

    #with open(title+'.json','w') as file:
     #         json.dump(dic,file)




class Shell_Scribe(cmd.Cmd):
    """
    Shell_Scribe is a commandline interface that automatically saves a history
    of what commands were typed to a text file as well as creating a shell
    script for them.
    """

    ## Return value for each command (None == 0)
    return_value = None
    ## The prompt to the user
    prompt = '\033[96m'+'S'+'\033[33m'+'hell-'+'\033[96m'+'S'+'\033[33m'+ \
             'cribe>'+'\033[0m'
    ## Set to True for Working Directory as prompt"
    location_prompt = False
    ## This is a list of commands that will not be stored by Shell-Scribe
    storage_blacklist = ["ls", "pwd", ""]
    ## Config File Name
    config_filename = "config.json"
    ## Twilio Attributes
    TWILIO = False
    ACCOUNT_SID = None
    AUTH_TOKEN = None
    message_recipient = None
    message_sender = None
    call_url = None
    alert_type = None
    ## Properties
    script_filename = "shell-scribe.sh"
    script = None






    def bashinator_9000(self, filename):

        dic={}
        inc=1
        title = ''
        author = ''
        date = datetime.datetime.now()
        title  = raw_input("What is the title: ")
        author = raw_input("Who is the author: ")
        dic['welcome']= raw_input("Input a description for the lesson: ")
        date   = datetime.datetime.now()
        if title =="": title = 'lesson'
        if author=="": author = 'N/A'

        dic["title"] = title
        dic["author"] = author

        with open(filename,'r') as file:
                  for row in file:
                        print '\033[91m' + "\nCode for the row: " + '\033[96m' + row + '\033[92m'
                        comment=raw_input('- ')
                        tempDic = {'comment':comment,'command':row}
                        dic.update({inc:tempDic})
                        inc+=1
        
        print('\033[0m')
        dic['command_count'] = inc - 1

        with open(title+'.json','w') as file:
                  json.dump(dic,file)







    def bashinator_10000(self, filename): #need sleeeeeep
        #fname = filename.readFile() #attempting to have json file read-in 
        with open(filename, 'r') as f:
            json_dict = json.load(f)
        print json_dict
        inc=1

        # Welcomes them to Hell
        print json_dict["welcome"], "\n"

        for x in range(json_dict["command_count"]):
            x = x + 1
            print '\033[91m' +"Line: ", x,'\n'
            print '\033[92m'+ "Comment: ", json_dict[str(x)]["comment"],'\n'
            print '\033[96m' + "Input: ", json_dict[str(x)]["command"][:-1]
            outfile = os.popen(json_dict[str(x)]["command"])
            output = outfile.read()
            return_val = outfile.close()
            if return_val != None:
                self.send_call()
            print '\033[93m' + "Output: ", os.popen(json_dict[str(x)]["command"]).read() + '\033[0m'
            raw_input("-Press Enter-\n")





    ## File Editing Methods
    def store_to_script(self, line):
        """
        Stores the shell command to the script
        """
        self.script.write(line + "\n")

    def load_config_json(self):
        """
        Configures Shell-Scribe based on the JSON configuration file 
        """
        with open(self.config_filename, 'r') as f:
            json_dict = json.load(f)
        #print "Dict from Json:", json_dict
        self.TWILIO = (1 == json_dict["twilio"]["TWILIO"])
        if self.TWILIO:
            self.ACCOUNT_SID = json_dict["twilio"]["ACCOUNT_SID"]
            self.AUTH_TOKEN = json_dict["twilio"]["AUTH_TOKEN"]
            self.message_recipient = json_dict["twilio"]["TO"]
            self.message_sender = json_dict["twilio"]["FROM"]
            if json_dict["twilio"]["ALERT_TYPE"].lower() == "call":
                self.alert_type = json_dict["twilio"]["ALERT_TYPE"].lower()
                self.call_url = json_dict["twilio"]["CALL_URL"]
        
        if json_dict["appearance"]["prompt"].lower() == 'location':
            self.location_prompt = True

    def no_config_subroutine(self):
        """
        Method that is called when there is no config found
        """
        gen_config = input("Generate Default Config File? (Y/n)")
        if gen_config == "": gen_conifg = "Y"
        if gen_config.lower() == 'y':
            self.generate_config() 
            self.load_config_json
        else:
            "No Configuration File. Running basic mode"

    ## Send text via Twilio
    def send_text(self, line):
        """
        Sends a text message via Twilio
        """
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)

        client.messages.create(to=self.message_recipient,
                               from_=self.message_sender, 
                               body="Failed on command: " + line)
    
    def send_call(self):
        """
        Sends said call via Twilio
        """
        print "Calling"
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        call = client.calls.create(to=self.message_recipient,
                                   from_=self.message_sender,
                                   url=self.call_url,
                                   method="GET",
                                   fallback_method="GET",
                                   status_callback_method="GET",
                                   record="false")
        print call.sid

    ## Explicit Shell-Scribe Commands
    def do_cd(self, line):
        """
        Runs the cd equivalent
        """
        if os.path.isdir(line):
            os.chdir(line)
        else:
            print "Directory ", line, " does not exist"

    def do_exit(self, line):
        """
        Exits Shell-Scribe
        """
        os.system("chmod +x %s" % self.script_filename)
        sys.exit()

    def do_quit(self, line):
        """
        Exits Shell Scribe
        """
        os.system("chmod +x %s" % self.script_filename)
        sys.exit()


    ## Misc. Functions
    def command_not_blank(self, line):
        """
        Checks to make sure the command is not all space characters
        """
        print "line:",line
        for char in line:
            if char != " ":
                return True
        return False

    ## CMD Overloads
    def do_EOF(self, line):
        """
        Method that is called at the end of a batch job.
        """
        return True
    
    def precmd(self, line):
        """
        Method that is run just before the shell command is run
        """ 
        return line 

    def emptyline(self):
        """
        Controls what happens if the user enters an empty line. This is addded
        to because without overloading this method it defaults to rerunning
        the command which is not what we are looking for.
        """
        return ""

    def postcmd(self, stop, line):
        """
        Method that is called after each of command is run
        """
        if self.location_prompt:
            self.prompt = os.getcwd() + " >"
        
        if self.return_value == None:
            if (line not in self.storage_blacklist) and self.command_not_blank(line):
                self.store_to_script(line)
                print "Stored!"

    def default(self, line):
        """
        This is the default method that is called if the shell command is not
        a specific shell command (a do_ method_)
        """
        cmd_file = os.popen(line)
        output = cmd_file.read()
        self.return_value = cmd_file.close()
        if self.return_value != None:
            if self.alert_type == 'text':
                self.send_text(line)
            if self.alert_type == 'call':
                self.send_call()
        if self.command_not_blank(line):
            print output
    
    def preloop(self):
        """
        Method that is called before the CMD loop begins
        """
        if self.location_prompt:
            self.prompt = os.getcwd() + " >"
        if os.path.isfile(self.script_filename):
            pass 
        self.script = open(self.script_filename, 'a')
    
if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Documents Shell-Commands")
    parser.add_argument('--location-prompt', action='store_true')
    parser.add_argument('-config', 
                        help="The name of the configuration JSON file")
    parser.add_argument('-create-lesson',
                        help="The name of the script that we are building \
                        a lesson for")
    parser.add_argument('-run-lesson',
                        help="The name of the lesson (JSON file) that we are \
                        running in shell-scribe")
    args = parser.parse_args()

    ss = Shell_Scribe()

    ss.location_prompt = args.location_prompt
    if args.config is not None:
        if os.path.isfile(args.config):
            print "Using configuration from file ", args.config
            ss.config_filename = args.config
            ss.load_config_json() 
        else:
            print "Config does not exist"
            self.no_config_subroutine()
    elif os.path.isfile("config.json"):
        print "Found config.json"
        ss.load_config_json()
    else:
        ss.no_config_subroutine()

    if DEBUG: print args



    if args.create_lesson != None:
        ss.bashinator_9000(args.create_lesson)
        print "RUNNING CREATE LESSON BLOCK"


    elif args.run_lesson != None:
        # Run Lesson Function
        ss.bashinator_10000(args.run_lesson)



    else:
        ss.cmdloop()
