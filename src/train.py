import subprocess
import os
import time
import zidan2


episodes = 100000

if __name__ == "__main__":

    print("start")
    for episode in range(episodes):

        # ディレクトリの移動
        os.chdir("../")
        os.chdir("../")

        # サーバの起動
        cmd = \
            "rcssserver server::half_time = -1 server::send_step = 3 server::sense_body_step = 2 server::simulator_step = 2 server::kick_off_wait = 0"
        server = subprocess.Popen(cmd.split())

        # # モニタの起動
        # cmd = "soccerwindow2"
        # window = subprocess.Popen(cmd.split())

        # ディレクトリの移動
        os.chdir("./Zidan/src")
        # クライアントプログラムの実行
        cmd = "python3 zidan2.py {}".format(episode)
        cliant = subprocess.Popen(cmd.split())

        # 学習
        while True:
            if zidan2.episode_finish_flag is True:
                break

        print("episode{} is done ".format(episode))

        # サーバの削除
        server.kill()
        # # ウィンドウの削除
        # window.kill()
        # クライアントの削除
        cliant.kill()

    print("end")
