import subprocess
import os
import time


print("start")

# ディレクトリの移動
os.chdir("../")
os.chdir("../")

# サーバの起動
cmd = "rcssserver"
server = subprocess.Popen(cmd.split())

time.sleep(10)

# サーバの削除
server.kill()

print("end")
