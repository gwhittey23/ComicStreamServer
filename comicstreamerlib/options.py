"""
CLI options class for comicstreamer app
"""

"""
Copyright 2014  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import getopt
import platform
import os
import traceback

import csversion

try:
    import argparse
except:
    pass

class Options:
    help_text = """ 
Usage: {0} [OPTION]... [FOLDER LIST]

A digital comic media server.

The FOLDER_LIST is a list of folders that will be scanned recursively
for comics to add to the database (persisted)

  -p, --port                 The port the server should listen on. (persisted)
  -r, --reset                Purge the existing database and quit
  -d, --debug                More verbose console output   
  -q, --quiet                No console output   
      --nomonitor            Don't start the folder scanner/monitor 
      --nobrowser            Don't launch a web browser                                            
      --version              Display version                            
  -h, --help                 Display this message
  
    """


    def __init__(self):
        self.port = None
        self.folder_list = None
        self.reset = False
        self.no_monitor = False
        self.debug = False
        self.quiet = False
        self.launch_browser = True
        self.reset_and_run = False
        
    def display_msg_and_quit( self, msg, code, show_help=False ):
        appname = os.path.basename(sys.argv[0])
        if msg is not None:
            print( msg )
        if show_help:
            print self.help_text.format(appname)
        else:
            print "For more help, run with '--help'"
        sys.exit(code)  

    def parseCmdLineArgs(self):
        
        if platform.system() == "Darwin" and hasattr(sys, "frozen") and sys.frozen == 1:
            # remove the PSN ("process serial number") argument from OS/X
            input_args = [a for a in sys.argv[1:] if "-psn_0_" not in  a ]
        else:
            input_args = sys.argv[1:]
            
        # parse command line options
        try:
            opts, args = getopt.getopt( input_args, 
                       "dp:hrq", 
                       [ "help", "port=", "version", "reset", "debug", "quiet",
                    "nomonitor", "nobrowser",
                    "_resetdb_and_run", #private
                    ] )

        except getopt.GetoptError as err:
            self.display_msg_and_quit( str(err), 2 )
        
        # process options
        for o, a in opts:
            if o in ("-r", "--reset"):
                self.reset = True
            if o in ("-d", "--debug"):
                self.debug = True                
            if o in ("-q", "--quiet"):
                self.quiet = True                
            if o in ("-h", "--help"):
                self.display_msg_and_quit( None, 0, show_help=True )
            if o in ("-p", "--port"):
                try:
                    self.port = int(a)
                except:
                    pass
            if o  == "--nomonitor":
                self.no_monitor = True
            if o  == "--nobrowser":
                self.launch_browser = False                
            if o  == "--version":
                print "ComicStreamer {0}:  Copyright (c) 2014 Anthony Beville".format(csversion.version)
                print "Distributed under Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)"
                sys.exit(0)
            if o == "--_resetdb_and_run":
                self.reset_and_run = True
                
                
        filename_encoding = sys.getfilesystemencoding()
        if len(args) > 0:
            #self.folder_list = [os.path.normpath(a.decode(filename_encoding)) for a in args]
            self.folder_list = [os.path.abspath(os.path.normpath(unicode(a.decode(filename_encoding)))) for a in args]
        
        # remove certain private flags from args
        try:
            sys.argv.remove("--_resetdb_and_run")
        except:
            pass
