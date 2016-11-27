#!/bin/bash
echo "[-] Removing home directory."
rm -R ~/.cfuzz
echo "[-] Removing python libraries."
rm -R /usr/lib/python2.7/dist-packages/cfuzz
echo "[-] Removing main executable from /usr/bin."
rm /usr/bin/cfuzz
echo "[✓] Done."
