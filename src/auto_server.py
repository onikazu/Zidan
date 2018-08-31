import subprocess
import time


print("start")
cmd = "cd -"
subprocess.call(cmd.split())
cmd = "rcssserver"
subprocess.Popen(cmd.split())
time.sleep(10)
cmd = "\x03"
subprocess.call(cmd.split())
print("end")
