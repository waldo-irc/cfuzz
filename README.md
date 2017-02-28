#Cfuzz
##A C Application fuzzer built in python.
####Current version requires python 2.7.  May work with newer versions, currently untested.

Please use responsibly and with permission only. For educational purposes only.

Now works with GDB peda effectively. 

##INSTALLTION (will install to /usr/bin by default.  ./setup.sh /path/to/custom for another path)
    git clone https://github.com/waldo-irc/cfuzz.git && cd cfuzz
    ./setup.sh
    And you're all set!

###Modules Included in -
/usr/lib/python2.7/dist-packages/

Logs in ~/.cfuzz/logs

###Required Repos
msf (msfvenom, pattern_create, pattern_offset)

###ToDo
Properly setup verbose error output and commenting + full logging of errors into output file

Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location

Find max seg fault limit to find buffer room

Network fuzzing over port, use python Sockets

--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'

--Make sure to check port is open and app is running before continuing

