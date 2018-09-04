import subprocess
import os
import time

episodes = 100000
exe_program = "zidan3.py"

if __name__ == "__main__":
    start_episode = 0
    # ログが残っていればその続きのエピソードとして学習を開始する。
    if os.path.isfile("./logs/Zidan2left_1_reward.log"):
        with open("./logs/Zidan2left_1_reward.log", "r") as file:
            lines = file.readlines()
            last_episode = lines[-1].split(",")[0]
            start_episode = last_episode

    print("start")
    for episode in range(int(start_episode), episodes):
        # ディレクトリの移動
        os.chdir("../")
        os.chdir("../")

        # サーバの起動
        cmd = \
            "rcssserver server::send_step = 3 server::sense_body_step = 2 server::simulator_step = 2 server::auto_mode = true server::kick_off_wait = 20000"
        server = subprocess.Popen(cmd.split())

        # モニタの起動
        cmd = "soccerwindow2"
        window = subprocess.Popen(cmd.split())

        # ディレクトリの移動
        os.chdir("./Zidan/src")

        if not os.path.isdir("./npy"):
            os.mkdir("./npy")

        if not os.path.isdir("./logs"):
            os.mkdir("./logs")

        # クライアントプログラムの実行
        cmd = "python3 {} {}".format(exe_program, episode)
        cliant = subprocess.Popen(cmd.split())

        # 学習
        # while True:
        #     if zidan2.episode_finish_flag is True:
        #         break


        time.sleep(6.7)


        print("episode{} is done ".format(episode))

        # サーバの削除
        server.kill()
        # ウィンドウの削除
        window.kill()
        # クライアントの削除
        cliant.kill()

    print("end")
