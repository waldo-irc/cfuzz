#Modules Include - 
/usr/lib/python2.7/dist-packages/textcolors.py
Logs in ~/.cfuzz/logs
Custom Modules in ~/.cfuzz/modules

Create bash install script for quick/easy install
Create README.md
Add to github

###Required Repos###
gdb (debugging to EIP point)
msf (msfvenom, pattern_create, pattern_offset)
socat (hosting)

###To Add to script
MAYBE: Full scan check
Properly setup verbose error output and commenting + full logging of errors into output file
Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location
Find max seg fault limit to find buffer room
Network fuzzing over port, use python Sockets
--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'
--Make sure to check port is open and app is running before continuing
Make a -msf command to create an msfvenom payload
