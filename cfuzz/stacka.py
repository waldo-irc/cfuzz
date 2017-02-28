# -*- coding: UTF-8 -*-
import textcolors, os, sys, exskele, socket, commands
from os.path import expanduser
from subprocess import Popen, PIPE, STDOUT
from time import sleep

def stackeipcheckA( fpath, buff ):
     textcolors.colortext( "--- Searching for EIP.", textcolors.HEADER, 'print' )

     textcolors.colortext( "Ensuring we get 41414141 in EIP.", textcolors.HEADER, 'print')
     with open('./tmp.py', 'w+') as myfile:
          myfile.write("buffer = 'A' * %s \n" % buff)
          myfile.write("gdb.execute(\"set pagination off\")\n")
          myfile.write("gdb.execute(\"set confirm off\")\n")
          myfile.write("gdb.execute(\"set logging overwrite on\")\n")
          myfile.write("gdb.execute(\"set logging redirect on\")\n")
          myfile.write("gdb.execute(\"set logging on\")\n")
          myfile.write("gdb.execute(\"file %s\")\n" % fpath)
          myfile.write("gdb.execute(\"run %s\" % buffer)\n")
          myfile.write("gdb.execute(\"quit\")")

     peda = commands.getoutput( "cat ~/.gdbinit" )
     if "source ~/peda/peda.py" in peda:
          os.system("sed -i -e 's/source ~\/peda\/peda.py/#source ~\/peda\/peda.py/g' ~/.gdbinit")

     os.system('gdb -q -x ./tmp.py')

     exskele.eipcheck()

     try:
          if exskele.eip == '41414141 ':
               textcolors.colortext( 'Seems like we overwrite eip as %s, continuing!' % exskele.eip, textcolors.GREEN, 'print' )
          else:
               textcolors.colortext( 'Doesn\'t seem like we got EIP control!', textcolors.FAIL, 'print' )
               os.system('rm ./tmp.py')
               exit(0)
     except AttributeError:
          textcolors.error( "Something went wrong, can't get EIP for this binary through input." , 3, 'print' )
          exit(0)

     textcolors.colortext( "Overflowing in GDB with MSF pattern.", textcolors.HEADER, 'print')
     pattern = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %s' % buff).read()
     patternf = pattern.split('\n')[0]
     with open('./tmp.py', 'w+') as myfile:
          myfile.write("buffer = '%s' \n" % patternf)
          myfile.write("gdb.execute(\"set pagination off\")\n")
          myfile.write("gdb.execute(\"set confirm off\")\n")
          myfile.write("gdb.execute(\"set logging overwrite on\")\n")
          myfile.write("gdb.execute(\"set logging redirect on\")\n")
          myfile.write("gdb.execute(\"set logging on\")\n")
          myfile.write("gdb.execute(\"file %s\")\n" % fpath)
          myfile.write("gdb.execute(\"run %s\" % buffer)\n")
          myfile.write("gdb.execute(\"quit\")")

     os.system('gdb -q -x ./tmp.py')

     textcolors.colortext( "Finding EIP offset based on overflowed EIP in pattern.", textcolors.HEADER, 'print')
     exskele.eipcheck()
     eipamt = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q %s -l %s | cut -d\' \' -f6' % (exskele.eip, buff)).read()
     eipamtf = int(eipamt.split('\n')[0])
     textcolors.colortext( "Offset at %s bytes." % eipamtf, textcolors.BLUE, 'print' )
     os.system('rm ./gdb.txt ./tmp.py')
     peda = commands.getoutput( "cat ~/.gdbinit" )
     if "#source ~/peda/peda.py" in peda:
          os.system("sed -i -e 's/#source ~\/peda\/peda.py/source ~\/peda\/peda.py/g' ~/.gdbinit")

def stackeipcheckB( fpath, buff ):
     textcolors.colortext( "--- Searching for EIP.", textcolors.HEADER, 'print' )

     textcolors.colortext( "Ensuring we get 41414141 in EIP.", textcolors.HEADER, 'print')
     with open('./tmp.py', 'w+') as myfile:
          myfile.write("buffer = 'A' * %s \n" % buff)
          myfile.write("gdb.execute(\"set pagination off\")\n")
          myfile.write("gdb.execute(\"set confirm off\")\n")
          myfile.write("gdb.execute(\"set logging overwrite on\")\n")
          myfile.write("gdb.execute(\"set logging redirect on\")\n")
          myfile.write("gdb.execute(\"set logging on\")\n")
          myfile.write("gdb.execute(\"file %s\")\n" % fpath)
          myfile.write("gdb.execute(\"shell echo '%s' > tmp.txt\")\n" % ("A"*buff))
          myfile.write("gdb.execute(\"run < tmp.txt\")\n")
          myfile.write("gdb.execute(\"quit\")")

     peda = commands.getoutput( "cat ~/.gdbinit" )
     if "source ~/peda/peda.py" in peda:
          os.system("sed -i -e 's/source ~\/peda\/peda.py/#source ~\/peda\/peda.py/g' ~/.gdbinit")

     os.system('gdb -q -x ./tmp.py')

     exskele.eipcheck()

     try:
          if exskele.eip == '41414141 ':
               textcolors.colortext( 'Seems like we overwrite eip as %s, continuing!' % exskele.eip, textcolors.GREEN, 'print' )
          else:
               textcolors.colortext( 'Doesn\'t seem like we got EIP control!', textcolors.FAIL, 'print' )
               os.system('rm ./tmp.py ./tmp.txt')
               exit(0)
     except AttributeError:
          textcolors.error( "Something went wrong, can't get EIP for this binary through input." , 3, 'print' )
          exit(0)

     textcolors.colortext( "Overflowing in GDB with MSF pattern.", textcolors.HEADER, 'print')
     pattern = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %s' % buff).read()
     patternf = pattern.split('\n')[0]
     with open('./tmp.py', 'w+') as myfile:
          myfile.write("buffer = '%s' \n" % patternf)
          myfile.write("gdb.execute(\"set pagination off\")\n")
          myfile.write("gdb.execute(\"set confirm off\")\n")
          myfile.write("gdb.execute(\"set logging overwrite on\")\n")
          myfile.write("gdb.execute(\"set logging redirect on\")\n")
          myfile.write("gdb.execute(\"set logging on\")\n")
          myfile.write("gdb.execute(\"file %s\")\n" % fpath)
          myfile.write("gdb.execute(\"shell echo '%s' > tmp.txt\")\n" % patternf)
          myfile.write("gdb.execute(\"run < tmp.txt\")\n")
          myfile.write("gdb.execute(\"quit\")")

     os.system('gdb -q -x ./tmp.py')

     textcolors.colortext( "Finding EIP offset based on overflowed EIP in pattern.", textcolors.HEADER, 'print')
     exskele.eipcheck()
     eipamt = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q %s -l %s | cut -d\' \' -f6' % (exskele.eip, buff)).read()
     eipamtf = int(eipamt.split('\n')[0])
     textcolors.colortext( "Offset at %s bytes." % eipamtf, textcolors.BLUE, 'print' )
     os.system('rm ./gdb.txt ./tmp.py ./tmp.txt')
     peda = commands.getoutput( "cat ~/.gdbinit" )
     if "#source ~/peda/peda.py" in peda:
          os.system("sed -i -e 's/#source ~\/peda\/peda.py/source ~\/peda\/peda.py/g' ~/.gdbinit")

def mainstack( fpath, args, string, waittime ):
     textcolors.colortext( "Fuzzing with %s bytes" % len(string), textcolors.BLUE, 'print' )
     if args is None:
          run = Popen("%s %s >> ~/.cfuzz/logs/latest-log.txt 2>&1" % (fpath, string), shell=True, stderr=STDOUT, stdin=PIPE, stdout=PIPE)
     else:
          run = Popen("%s %s %s >> ~/.cfuzz/logs/latest-log.txt 2>&1" % (fpath, args, string), shell=True, stderr=STDOUT, stdin=PIPE, stdout=PIPE)
     if waittime is False:
          sleep(.1)
     else:
          sleep(waittime)

def altstack( fpath, args, string, waittime, host, port ):
#def altstack( fpath, args, string, waittime ):
     if host is not False:
          print 'True!'
          exit(0)
     else:
          textcolors.colortext( "Fuzzing with %s bytes" % len(string), textcolors.BLUE, 'print' )
          p = Popen(fpath, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)

          if waittime is not False:
               sleep(waittime)

          if args is None:
               grep_stdout = p.communicate(input=string)[0]
          else:
               grep_stdout = p.communicate(input='%s %s' % (args,string))[0]

#     print(grep_stdout.decode())

          with open(os.path.join(os.path.expanduser('~'),'.cfuzz/logs/latest-log.txt'), 'w+') as myfile:
               myfile.write(grep_stdout.decode())
