# -*- coding: UTF-8 -*-

#class bcolors:
#     HEADER = '\033[95m'
#     BLUE = '\033[94m'
#     GREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

'''Error messages are defined by [!] || [!!] || [!!!]
[!] Are warnings, the script can still continue with these.
[!!] Means script errors.  These are thrown because the script can't continue without these being resolved.
[!!!] These are system issues, EX: Missing repos or required files.'''
def error( msg, severity, printerr='store' ):
     if severity >= 4:
          severity = 3
     global errmess
     if severity >= 2:
          errmess = FAIL + ('[!]' * severity) + ' ' + msg + ENDC
     else:
          errmess = WARNING + ('[!]' * severity) + ' ' + msg + ENDC
     if 'print' in printerr:
          print errmess
     else:
          pass

'''Handles coloring for output.  Use bcolors class for coloring options.'''
def colortext( msg, color=BLUE, printcolortext='store' ):
     global colormsg
     colormsg = color + '[*] ' + msg + ENDC
     if 'print' in printcolortext:
          print colormsg
     else:
          pass
