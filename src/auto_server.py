import subprocess
import os
import time


print("start")
os.chdir("../")
os.chdir("../")
cmd = "rcssserver"
subprocess.Popen(cmd.split())
time.sleep(10)
cmd = "\x03"
subprocess.call(cmd.split())
print("end")
