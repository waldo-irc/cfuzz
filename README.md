#Cfuzz
##A C Application fuzzer built in python.
####Current version requires python 2.7.  May work with newer versions, currently untested.

Please use responsibly and with permission only. For educational purposes only.

Now works with GDB peda effectively. 

###Modules Include - 
/usr/lib/python2.7/dist-packages/textcolors.py

Logs in ~/.cfuzz/logs

Custom Modules in ~/.cfuzz/modules?

###Required Repos
msf (msfvenom, pattern_create, pattern_offset)

socat (hosting)

###ToDo
Properly setup verbose error output and commenting + full logging of errors into output file

Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location

Find max seg fault limit to find buffer room

Network fuzzing over port, use python Sockets

--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'

--Make sure to check port is open and app is running before continuing

