#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse, os, sys, re, commands
from cfuzz import stringf, stacka, exskele, textcolors
from os.path import expanduser

#Directory checks
if not os.path.isdir(os.path.join(os.path.expanduser('~'),'.cfuzz')):
     os.system("mkdir ~/.cfuzz")
if not os.path.isdir(os.path.join(os.path.expanduser('~'),'.cfuzz/logs')):
     os.system("mkdir ~/.cfuzz/logs")

#Here we set up logging
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(os.path.join(os.path.expanduser('~'),'.cfuzz/logs/log.txt'), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()

#Just a function that returns completion '''
def completion():
     #Signal Completion
     textcolors.colortext( "Execution completed.", textcolors.GREEN, 'print' )

#Start argument parsing
parser = argparse.ArgumentParser(description='Fuzz C applications for String Format Overflows and Stack Overflows and create custom skeletons on findings.')
parser.add_argument('progname', metavar='execname', type=str, nargs='+', help='A file to fuzz')
parser.add_argument('--host=', dest='host', type=str, default=False, help='A host to fuzz, either =run to have the program do it itself, =host to have cfuzz do it, =remote to fuzzer remotely (coming soon)', action="store")
parser.add_argument('--port=', dest='port', type=int, default=False, help='A port to fuzz (coming soon)', action="store")
parser.add_argument("--wipe", help="Wipe logs for %(prog)s", default=False, action="store_true", dest='wipe')
parser.add_argument("-a", help="Check for segmentation faults terminal arguments.", nargs='?', type=str, default=False, action="store", dest="afield")
parser.add_argument("-ai", help="Check for segmentation faults in application input.", nargs='?', type=str, default=False, action="store", dest="aifield")
parser.add_argument("-s", help="Check for segmentation faults with string format overflow using terminal arguments.", nargs='?', type=str, default=False, action="store", dest="sfield")
parser.add_argument("-si", help="Check for segmentation faults with string format overflow in application input.", nargs='?', type=str, default=False, action="store", dest="sifield")
parser.add_argument("-wE", help="Write an exploit skeleton.", type=str, default=False, action="store", dest="exfilename")
parser.add_argument("-eip", help="Search for EIP as well.", default=False, action="store_true", dest="eip")
parser.add_argument("-aslr", help="Disable or enable ASLR (Must be root). Will exit after asking.", default=False, action="store_true", dest="aslrcheck")
parser.add_argument("-d", help="Add a delay.", type=float, default=False, action="store", dest="delay")
parser.add_argument("-v", help="Add verbosity.", default=False, action="store_true", dest="verbose")
args = parser.parse_args()

#UNAVAILABLE TILL LATER
if args.host or args.port:
    textcolors.colortext("Host fuzzing not available yet.", textcolors.FAIL, 'print')
    exit(0)
if args.verbose:
    textcolors.colortext("Verbosity only works with stack based BOF currently.", textcolors.WARNING, 'print')

#Check for ASLR
aslr1 = commands.getoutput("ldd %s | grep libc | cut -d'(' -f2 | cut -d')' -f1" % args.progname[0])
aslr2 = commands.getoutput("ldd %s | grep libc | cut -d'(' -f2 | cut -d')' -f1" % args.progname[0])
aslr3 = commands.getoutput("cat /proc/sys/kernel/randomize_va_space")
if args.aslrcheck:
    if aslr1 == aslr2 or aslr3 == 0:
        textcolors.colortext("ASLR is disabled with %s" % aslr3, textcolors.GREEN, 'print')
        textcolors.colortext("Enable ASLR? [y/N]: ", textcolors.GREEN)
        ask = raw_input(textcolors.colormsg)
        if ask.lower() == "yes" or ask.lower() == "y":
            os.system("echo 2 | sudo tee /proc/sys/kernel/randomize_va_space")
        else:
            textcolors.colortext("Leaving ASLR disbled.", textcolors.GREEN, 'print')
    else:
        textcolors.colortext("ASLR is enabled with %s" % aslr3, textcolors.WARNING, 'print')
        textcolors.colortext("Disable ASLR? [y/N]: ", textcolors.GREEN)
        ask = raw_input(textcolors.colormsg)
        if '%s' % ask.lower() == "yes" or '%s' % ask.lower() == "y":
            os.system("echo 0 | sudo tee /proc/sys/kernel/randomize_va_space")
        else:
            textcolors.colortext("Leaving ASLR enabled.", textcolors.GREEN, 'print')
    exit(0)
else:
    if aslr1 == aslr2 or aslr3 == 0:
        textcolors.colortext( "ASLR is disabled with %s." % aslr3, textcolors.GREEN, 'print' )
    else:
        textcolors.colortext( "ASLR is enabled with %s." % aslr3, textcolors.WARNING, 'print' )

if args.wipe:
     textcolors.colortext( "Wipings logs located at '~/.cfuzz/logs'", textcolors.HEADER, 'print' )
     os.system("echo '' > ~/.cfuzz/logs/log.txt; echo '' > ~/.cfuzz/logs/latest-log.txt; echo '' >  ~/.cfuzz/logs/verbose.txt")

if args.delay is not False and args.afield is False and args.aifield is False and args.sfield is False and args.sifield is False:
     textcolors.error( "Delay requires an argument of -a, -ai, -s, or -si." ,1,'print' )
     exit(0)

if args.afield is False and args.aifield is False and args.sfield is False and args.sifield is False:
     textcolors.error('Must supply a scan type of -a, -ai, -s, or -si.',2,'print')
     exit(0)

#Set only 1 arg at a time
if args.afield is not False and (args.aifield is not False or args.sfield is not False or args.sifield is not False):
    textcolors.error('Can only do 1 scan type at a time.', 2, 'print' )
    exit(0)
if args.aifield is not False and (args.afield is not False or args.sfield is not False or args.sifield is not False):
    textcolors.error('Can only do 1 scan type at a time.', 2, 'print' )
    exit(0)
if args.sfield is not False and (args.afield is not False or args.aifield is not False or args.sifield is not False):
    textcolors.error('Can only do 1 scan type at a time.', 2, 'print' )
    exit(0)
if args.sifield is not False and (args.afield is not False or args.aifield is not False or args.sfield is not False):
    textcolors.error('Can only do 1 scan type at a time.', 2, 'print' )
    exit(0)
#End Arg limiting

if args.port and (args.port > 65535 or args.port <= 0):
     textcolors.error( "Error, port chosen out of range!", 3, 'print' )
     exit(0)

if args.host is not False:
     if args.host.lower() == 'run' or args.host.lower() == 'host' or args.host.lower() == 'remote':
          pass
     else:
          textcolors.error( "Host argument must be =run, =host, or =remote.", 2, 'print' )
          exit(0)

if args.host is not False and args.port is False:
     textcolors.error( "Must specify a port with -port=.", 2, 'print' )
     exit(0)

if (args.host is not False and args.afield is not False) or (args.host is not False and args.sfield is not False):
     textcolors.error( "Can only use with -ai or -si.", 2, 'print' )
     exit(0)

if (args.eip is not False and args.sfield is not False) or (args.eip is not False and args.sifield is not False):
     textcolors.error( "Can only search for eip with -a or -ai.", 2, 'print' )
     exit(0)

if args.delay is not False:
     textcolors.colortext( "Running with %s second delay." % args.delay, textcolors.WARNING,'print')


#Setting up base variables
progname = args.progname[0]
buffer = ["A"]
counter = 100
segfault = 'False'

#Getting path prepared for execution and checks
if '/' in progname:
     fpath = '%s' % progname
else:
     fpath = './%s' % progname

if not os.path.isfile(fpath):
     textcolors.error( 'File %s doesn\'t seem to exist' % progname, 2, 'print' )
     exit(0)

#Double check before execution and ensure file is an executable
if os.access(fpath, os.X_OK):
     textcolors.colortext( 'Continue fuzzing file "%s"? [y/N]> ' % fpath, textcolors.GREEN )
     conf = raw_input(textcolors.colormsg)
     fconf = conf.lower()
else:
     textcolors.error( 'File "%s" doesn\'t seem like an executable, really continue? [y/N]> ' % progname, 1 )
     conf = raw_input(textcolors.errmess)
     fconf = conf.lower()

if 'y' in fconf:
     pass
else:
     textcolors.colortext( "Exiting %s" % sys.argv[0], textcolors.FAIL, 'print')
     exit(0)

#Fuzz begins here
textcolors.colortext( 'Starting Fuzz of "%s" now!' % fpath, textcolors.HEADER, 'print' )

#Clear latest-log to prepare for new entries - this log is for checking seg faults
with open(os.path.join(os.path.expanduser('~'),'.cfuzz/logs/latest-log.txt'), 'w+') as myfile:
     myfile.write('')

#Preparing fuzzing buffer
while len(buffer) <= 100:
     buffer.append("\x41"*counter)
     counter=counter+100

#Run a scan based on argument supplied.  We use try to output a special message on KeyExit
try:
     if args.sifield is not False:
          stringf.checkstrng( args.sifield, fpath, args.exfilename, args.delay )
     elif args.sfield is not False:
          stringf.checkstrngB( args.sfield, fpath, args.exfilename, args.delay )

     for string in buffer:
          if args.afield is not False:
               stacka.mainstack( fpath, args.afield, string, args.delay, args.verbose )
          elif args.aifield is not False:
               stacka.altstack( fpath, args.aifield, string, args.delay, args.verbose,  args.host, args.port )
          elif args.sfield is not False or args.sifield is not False:
               pass

          #Here we check to see if a segfault was detected
          with open(os.path.join(os.path.expanduser('~'),'.cfuzz/logs/latest-log.txt'), 'r') as myfile:
               for line in myfile:
                    if 'Segmentation fault' in line:
                         textcolors.colortext( "[✓✓✓] Seg Fault seems to have occured at %s bytes!" % len(string), textcolors.BOLD, 'print'  )
                         buff = len(string)
                         segfault = 'True'
                         break
               else:
                    continue
               break

     #Check if -wE argument is true to create the stack based exploit skeleton
     if args.exfilename is not False and args.afield is not False and segfault == 'True':
          exskele.exdev( args.afield,args.exfilename,buff,fpath,args.eip )
     if args.exfilename is not False and args.aifield is not False and segfault == 'True':
          exskele.exdev2( args.aifield,args.exfilename,buff,fpath,args.eip )
     elif args.exfilename is not False and (args.afield is not False or args.aifield is not False ) and segfault == 'False':
          textcolors.error( "No segfault found for exploit creation", 1, 'print')

     if args.eip is not False and segfault == 'True' and args.exfilename is False and args.afield is not False:
          stacka.stackeipcheckA( fpath, buff )
     elif args.eip is not False and segfault == 'True' and args.exfilename is False and args.aifield is not False:
          stacka.stackeipcheckB( fpath, buff )

     if args.verbose is True:
          os.system("echo '' >> ~/.cfuzz/logs/verbose.txt")

     completion()
     exit(0)

except KeyboardInterrupt:
     print '\n'
     textcolors.colortext( "Exit key detected, closing %s." % sys.argv[0],textcolors.FAIL,'print')

