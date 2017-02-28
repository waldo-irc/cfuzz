#Cfuzz
##A C Application fuzzer built in python.
####Current version requires python 2.7.  May work with newer versions, currently untested.

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
msf (msfvenom, pattern_create, pattern_offset)


##Example Run
    root@kali:~# cfuzz vuln -a -eip -wE test
    [*] ASLR is enabled with 2.
    [*] Continue fuzzing file "./vuln"? [y/N]> y
    [*] Starting Fuzz of "./vuln" now!
    [*] Fuzzing with 1 bytes
    [*] Fuzzing with 100 bytes
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


###ToDo
Properly setup verbose error output and commenting + full logging of errors into output file

Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location

Find max seg fault limit to find buffer room

Network fuzzing over port, use python Sockets

--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'

--Make sure to check port is open and app is running before continuing

