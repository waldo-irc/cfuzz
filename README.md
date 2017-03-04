#Cfuzz
##A C Application fuzzer built in python.
####Current version requires python 2.7.  May work with newer versions, currently untested.

##TOC

1. ["Installation"]: https://github.com/waldo-irc/cfuzz#installation-will-install-to-usrbin-by-default--setupsh-pathtocustom-for-another-path

2. (https://github.com/waldo-irc/cfuzz#usage "Standard usage")

3. (https://github.com/waldo-irc/cfuzz#example-run "Usage on stack based attacks")2. (https://github.com/waldo-irc/cfuzz#usage "Usage on stack based attacks")

4. (https://github.com/waldo-irc/cfuzz#format-string-attacks "Format string attacks")

<br />

Please use responsibly and with permission only. For educational purposes only.

Now works with GDB peda effectively. 

The included "cprogs" are vulnerable programs I found from CTF's/Googling to practice using this application on.  

##INSTALLATION (will install to /usr/bin by default.  ./setup.sh /path/to/custom for another path)
    git clone https://github.com/waldo-irc/cfuzz.git && cd cfuzz
    ./setup.sh
    And you're all set!

###Modules Included in -
/usr/lib/python2.7/dist-packages/

###Logs Included in - 
~/.cfuzz/logs

###Required Repos
msf (msfelfscan, pattern_create, pattern_offset)

gdb (GNU Debugger)

##Usage
    usage: cfuzz [-h] [--host= HOST] [--port= PORT] [--wipe] [-a [AFIELD]]
                 [-ai [AIFIELD]] [-s [SFIELD]] [-si [SIFIELD]] [-wE EXFILENAME]
                 [-eip] [-aslr] [-d DELAY] [-v]
                 execname [execname ...]

    Fuzz C applications for String Format Overflows and Stack Overflows and create
    custom skeletons on findings.

    positional arguments:
      execname        A file to fuzz

    optional arguments:
      -h, --help      show this help message and exit
      --host= HOST    A host to fuzz, either =run to have the program do it itself
                      or =host to have cfuzz do it (coming soon).
      --port= PORT    A port to fuzz (coming soon)
      --wipe          Wipe logs for cfuzz
      -a [AFIELD]     Check for segmentation faults terminal arguments.
      -ai [AIFIELD]   Check for segmentation faults in application input.
      -s [SFIELD]     Check for segmentation faults with string format overflow
                      using terminal arguments.
      -si [SIFIELD]   Check for segmentation faults with string format overflow in
                      application input.
      -wE EXFILENAME  Write an exploit skeleton.
      -eip            Search for EIP as well.
      -aslr           Disable or enable ASLR (Must be root). Will exit after
                      asking.
      -d DELAY        Add a delay.
      -v              Add verbosity.

##Example Run
    root@kali:~# cfuzz vuln -a -eip -wE test
    [*] ASLR is enabled with 2.
    [*] Continue fuzzing file "./vuln"? [y/N]> y
    [*] Starting Fuzz of "./vuln" now!
    [*] Fuzzing with 1 bytes
    [*] Fuzzing with 100 bytes
    [*] Fuzzing with 200 bytes
    [*] Fuzzing with 300 bytes
    [*] [✓✓✓] Seg Fault seems to have occured at 300 bytes!
    [*] Looking for jmp/call eax.
    [*] Looking for jmp/call esp.
    [*] Starting exploit skeleton creation by creating pattern.
    [*] Ensuring we get 41414141 in EIP.
    Overflow me! 
    [*] Seems like we overwrite eip as 41414141 , continuing!
    [*] Overflowing in GDB with msf pattern.
    Overflow me! 
    [*] Finding EIP offset based on overflowed EIP in pattern.
    [*] Writing Exploit with eip offset at 268 bytes.
    [*] Finished! Cleaning up.
    [*] Exploit created in working directory as ./test.py
    [*] Execution completed.

###Skeleton
    root@kali:~# python test.py 
    [*] Running buffer length 300 against ./vuln
    Overflow me! 
    Segmentation fault

##Format string attacks
    root@kali:~/cfuzz/cprogs# cfuzz vuln3 -s
    [*] ASLR is enabled with 2.
    [*] Continue fuzzing file "./vuln3"? [y/N]> y
    [*] Starting Fuzz of "./vuln3" now!
    [*] (%d) -1075513775
    [*] (%s) %s
    [*] (%x) bf97c651
    [*] (%08x) bf94e64f
    [*] (%08d) -1076005297
    [*] (%08s)     %08s
    [*] Scan further? [y/N]> y
    [0] %d
    [1] %s
    [2] %x
    [3] %08x
    [4] %08d
    [5] %08s
    [6] Custom format string
    [*] Which type of format to continue using?> 1
    [*] Are you sure to use %s?> y
    [*] Running with %s!> 
    cfuzz: %s.%s.%s
    Segmentation fault

    [*] Hit enter to Continue with %s, change format with 'c', or enter anything else to quit > 
    cfuzz: %s.%s.%s.%s
    Segmentation fault

    [*] Hit enter to continue with %s, change format with 'c', or enter anything else to quit > c
    [0] %d
    [1] %s
    [2] %x
    [3] %08x
    [4] %08d
    [5] %08s
    [6] Custom format string
    [*] Which type of format to continue using?> 2
    [*] Are you sure to use %x?> y
    cfuzz: %x.%x.%x
    bfa9864b.1ac240.1ad240
    [*] Hit enter to Continue with %x, change format with 'c', or enter anything else to quit > 
    cfuzz: %x.%x.%x.%x
    bfbc0648.1ac240.1ad240.252e7825

###Skeleton
    root@kali:~/cfuzz/cprogs# cfuzz vuln3 -s -wE fire
    [*] ASLR is enabled with 2.
    [*] Continue fuzzing file "./vuln3"? [y/N]> y
    [*] Starting Fuzz of "./vuln3" now!
    [*] (%d) -1081649577
    [*] (%s) %s
    [*] (%x) bfd6c657
    [*] (%08x) bfcab655
    [*] (%08d) -1077344683
    [*] (%08s)     %08s
    [*] Scan further? [y/N]> 
    [*] Create a basic string ovrflw skeleton?> y
    [*] Choose a format string type> 
    [0] %d
    [1] %s
    [2] %x
    [3] %08x
    [4] %08d
    [5] %08s
    [6] Custom format string
    [*] Which type of format to continue using?> 2
    [*] Are you sure to use %x?> y
    [*] Exploit created in working directory as ./fire.py
    [*] Execution completed.

    root@kali:~/cfuzz/cprogs# python fire.py 
    [*] Enter the buffer %x how many times into ./vuln3?> 5
    bf849641.1ac240.1ad240.252e7825.78252e78.2e78252e

#ToDo
Properly setup verbose error output and commenting + full logging of errors into output file

Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location

Find max seg fault limit to find buffer room

Network fuzzing over port, use python Sockets

--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'

--Make sure to check port is open and app is running before continuing

