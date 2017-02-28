#!/bin/bash

if [ ! -d "/usr/lib/python2.7" ]; then
    echo "[x] Python 2.7 required."
    exit 0
fi

if [ ! -d "/usr/lib/python2.7/dist-packages/cfuzz" ]; then
    echo "[-] Setting up python modules in '/usr/lib/python2.7/dist-packages/cfuzz/'."
    mkdir /usr/lib/python2.7/dist-packages/cfuzz/
    cp -R ./cfuzz/* /usr/lib/python2.7/dist-packages/cfuzz/
else
    echo "Required modules already exist"
fi

if [ -z "$1" ]; then
    if [ ! -f "/usr/bin/cfuzz" ]; then
        echo "[-] Moving executable to bin."
        cp ./cfuzz.py /usr/bin/cfuzz
    else
        echo "Executable already exists."
    fi
else
    if [ ! -f "$1" ]; then
        echo "[-] Moving executable to $1."
        cp ./cfuzz.py "$1"/cfuzz
    else
        echo "Executable already exists."
    fi
fi

if [ ! -d "~/.cfuzz" ]; then
    echo "[-] Setting up user logs and directories in '~/.cfuzz'."
    mkdir ~/.cfuzz
    mkdir ~/.cfuzz/logs
    mkdir ~/.cfuzz/modules
else
    echo "Personal directories already setup."
fi

echo "[✓] Installation completed successfully, you can delete this folder now!  Run cfuzz -h to get started."
