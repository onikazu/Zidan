import subprocess
import os
import time


episodes = 100000

if __name__ == "__main__":

    print("start")
    for episode in range(episodes):

        # ディレクトリの移動
        os.chdir("../")
        os.chdir("../")

        # サーバの起動
        cmd = \
            "rcssserver server::synch_mode = true server::auto_mode = true server::kick_off_wait = 0"
        server = subprocess.Popen(cmd.split())

        # ディレクトリの移動
        os.chdir("./Zidan/src")
        # クライアントプログラムの実行
        cmd = "python3 zidan2.py {}".format(episode)
        cliant = subprocess.Popen(cmd.split())

        time.sleep(10)

        print("episode{} is done ".format(episode))

        # サーバの削除
        server.kill()
        # クライアントの削除
        cliant.kill()

    print("end")
