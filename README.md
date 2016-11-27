#Modules Include - 
/usr/lib/python2.7/dist-packages/textcolors.py
Logs in ~/.cfuzz/logs
Custom Modules in ~/.cfuzz/modules

Create bash install script for quick/easy install
Create README.md
Add to github

###Required Repos###
wine (windows stuff)
msf (msfvenom, pattern_create, pattern_offset)
gdb (debugging to EIP point)
socat

###To Add to script
MAYBE: Full scan check
Finish argument format string scan with -s
Properly setup verbose error output and commenting + full logging of errors into output file
Versatile argument exploitaiton, currently program - arg - ovfrlw or program - ovfrlw, set up so proram - choose arg and ovrfl location
Find max seg fault limit to find buffer room
Network fuzzing over port, use python Sockets
--Localhost hosting scans 'exec /usr/bin/socat tcp4-l:$port,fork,reuseaddr exec:/filename'
--Windows hosting with wine
--Make sure to check port is open and app is running before continuing
Allow only 1 of the 4 args at once
Make a -msf command to create an msfvenom payload
fix -a race condition
add eip option to make finding EIP optional for both writing and plain scanning
Need absolute paths for wine
check if EIP is 41414141 properly
