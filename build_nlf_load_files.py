#!/usr/bin/python
import time
import datetime
#!/usr/bin/python
import sys
import os
from subprocess import call

for f in os.listdir("/app-data"):
    if f.endswith(".gz"):
        print f
        no_ext=f[:-3]
        new_filename=no_ext+".jar"
        call('jar cvfM {} {}'.format(new_filename, f), shell=True)
