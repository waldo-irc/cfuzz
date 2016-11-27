# -*- coding: UTF-8 -*-
import os, subprocess, textcolors, exskele
from subprocess import Popen, PIPE, STDOUT
from time import sleep

def checkstrng( args, fpath, skeleton, delay ):
     overflws = "%d %s %x %08x %08d %08s"
     lines = []
     out = []
     x = 0

     def checkcallform():
          try:
               textcolors.colortext( "Which type of format to continue using?> ",textcolors.HEADER )
               global wcont
               wcont = input(textcolors.colormsg)
               sure = 'n'
               while wcont not in ops:
                    textcolors.error( "Bad option, try again", 2, 'print' )
                    wcont = input(textcolors.colormsg)

               if wcont == 6:
                    textcolors.colortext( "Enter custom string type> ",textcolors.BLUE )
                    custstr= raw_input(textcolors.colormsg)
                    ops[wcont] = []
                    ops[wcont].append(custstr)

               textcolors.colortext( "Are you sure to use %s?> " % ops[wcont][0], textcolors.WARNING )
               sure = raw_input(textcolors.colormsg)
               if 'y' in sure.lower():
                    wcont = ops[wcont][0]
               else:
                    checkcallform()
          except (ValueError, NameError, SyntaxError):
               textcolors.error( 'Must be an integer value between 0-6', 3, 'print' )
               checkcallform()

     def callform():
          global ops
          ops = {}
          x = 0
          for line in overflws.split():
               ops[x] = []
               ops[x].append(line)
               print textcolors.BLUE + "[%s] %s" % (x,line) + textcolors.ENDC
               x+=1
          ops[6] = []
          ops[6].append('Custom format string')
          print textcolors.BLUE + "[6] Custom format string" + textcolors.ENDC
          checkcallform()

     for line in overflws.split():
          sleep(delay)
          lines.append(line)
          p = Popen(fpath, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
          if args is None:
               grep_stdout = p.communicate(input=line)[0]
          else:
               grep_stdout = p.communicate(input='%s %s' % (args,line))[0]
#          print(grep_stdout.decode())
          out.append(grep_stdout.decode())
     for line in overflws.split():
          textcolors.colortext( '(%s) %s' % (line, out[x]),textcolors.BLUE,'print' )
          x+=1
          if x >= 6:
               pass

     textcolors.colortext( "Scan further? [y/N]> ",textcolors.GREEN )
     cont = raw_input(textcolors.colormsg)
     if 'y' in cont.lower():
          callform()

          textcolors.colortext( "Running with %s!> " % wcont.lower(), textcolors.GREEN, 'print' )
          wconf = 'y'
          if 'y' in wconf.lower():
               wfuzz = (wcont.lower()+'.')*2+wcont.lower()
               p = Popen(fpath, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
               print 'cfuzz: %s' % wfuzz
               if args is None:
                    grep_stdout = p.communicate(input=wfuzz)[0]
                    print(grep_stdout.decode())
               else:
                    grep_stdout = p.communicate(input='%s %s' % (args,wfuzz))[0]
                    print(grep_stdout.decode())
          else:
               callform()

#          for xyz in range(3, 16):
          xyz = 2
          while xyz <= 16:
               textcolors.colortext( "Hit enter to Continue with %s, change format with 'c', or enter anything else to quit > " % wcont.lower(), textcolors.GREEN )
               wconf = raw_input(textcolors.colormsg)

               xyz+=1

               if 'c' in wconf.lower():
                    callform()
                    xyz = 2
                    wconf = 'y'

               if 'y' in wconf.lower() or wconf == '':
                    wfuzz = (wcont.lower()+'.')*xyz+wcont.lower()
                    print 'cfuzz: %s' % wfuzz

                    p = Popen(fpath, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
                    if args is None:
                         grep_stdout = p.communicate(input=wfuzz)[0]
                         print(grep_stdout.decode())
                    else:
                         grep_stdout = p.communicate(input='%s %s' % (args,wfuzz))[0]
                         print(grep_stdout.decode())
               else:
                    break
     else:
          pass

     if skeleton is not False:
          textcolors.colortext( "Create a basic string ovrflw skeleton?> ", textcolors.BLUE )
          excont = raw_input(textcolors.colormsg)
          if 'y' in excont.lower():
               textcolors.colortext( "Choose a format string type> ", textcolors.BLUE, 'print' )
               callform()
               exskele.stringexdev( args,wcont,fpath,skeleton )

def checkstrngB( args, fpath, skeleton, delay ):
     overflws = "%d %s %x %08x %08d %08s"
     lines = []
     out = []
     x = 0

     def checkcallform():
          try:
               textcolors.colortext( "Which type of format to continue using?> ",textcolors.HEADER )
               global wcont
               wcont = input(textcolors.colormsg)
               sure = 'n'
               while wcont not in ops:
                    textcolors.error( "Bad option, try again", 2, 'print' )
                    wcont = input(textcolors.colormsg)

               if wcont == 6:
                    textcolors.colortext( "Enter custom string type> ",textcolors.BLUE )
                    custstr= raw_input(textcolors.colormsg)
                    ops[wcont] = []
                    ops[wcont].append(custstr)

               textcolors.colortext( "Are you sure to use %s?> " % ops[wcont][0], textcolors.WARNING )
               sure = raw_input(textcolors.colormsg)
               if 'y' in sure.lower():
                    wcont = ops[wcont][0]
               else:
                    checkcallform()
          except (ValueError, NameError, SyntaxError):
               textcolors.error( 'Must be an integer value between 0-6', 3, 'print' )
               checkcallform()

     def callform():
          global ops
          ops = {}
          x = 0
          for line in overflws.split():
               ops[x] = []
               ops[x].append(line)
               print textcolors.BLUE + "[%s] %s" % (x,line) + textcolors.ENDC
               x+=1
          ops[6] = []
          ops[6].append('Custom format string')
          print textcolors.BLUE + "[6] Custom format string" + textcolors.ENDC
          checkcallform()

     for line in overflws.split():
          sleep(delay)
          lines.append(line)
          if args is None:
               grep_stdout = os.popen('%s %s' % (fpath,line)).read().split('\n')[0]
          else:
               grep_stdout = os.popen('%s %s %s' % (fpath,args,line)).read().split('\n')[0]
          out.append(grep_stdout)

     for line in overflws.split():
          textcolors.colortext( '(%s) %s' % (line, out[x]),textcolors.BLUE,'print' )
          x+=1
          if x >= 6:
               pass

     textcolors.colortext( "Scan further? [y/N]> ",textcolors.GREEN )
     cont = raw_input(textcolors.colormsg)
     if 'y' in cont.lower():
          callform()

          textcolors.colortext( "Running with %s!> " % wcont.lower(), textcolors.GREEN, 'print' )
          wconf = 'y'
          if 'y' in wconf.lower():
               wfuzz = (wcont.lower()+'.')*2+wcont.lower()
               print 'cfuzz: %s' % wfuzz
               if args is None:
                    grep_stdout = os.popen('%s %s' % (fpath,wfuzz)).read().split('\n')[0]
                    print(grep_stdout)
               else:
                    grep_stdout = os.popen('%s %s %s' % (fpath,args,wfuzz)).read().split('\n')[0]
                    print(grep_stdout)
          else:
               callform()

#          for xyz in range(3, 16):
          xyz = 2
          while xyz <= 16:
               textcolors.colortext( "Hit enter to Continue with %s, change format with 'c', or enter anything else to quit > " % wcont.lower(), textcolors.GREEN )
               wconf = raw_input(textcolors.colormsg)

               xyz+=1

               if 'c' in wconf.lower():
                    callform()
                    xyz = 2
                    wconf = 'y'

               if 'y' in wconf.lower() or wconf == '':
                    wfuzz = (wcont.lower()+'.')*xyz+wcont.lower()
                    print 'cfuzz: %s' % wfuzz

                    if args is None:
                         grep_stdout = os.popen('%s %s' % (fpath,wfuzz)).read().split('\n')[0]
                         print(grep_stdout)
                    else:
                         grep_stdout = os.popen('%s %s %s' % (fpath,args,wfuzz)).read().split('\n')[0]
                         print(grep_stdout)
               else:
                    break
     else:
          pass

     if skeleton is not False:
          textcolors.colortext( "Create a basic string ovrflw skeleton?> ", textcolors.BLUE )
          excont = raw_input(textcolors.colormsg)
          if 'y' in excont.lower():
               textcolors.colortext( "Choose a format string type> ", textcolors.BLUE, 'print' )
               callform()
               exskele.stringexdevB( args,wcont,fpath,skeleton )
