import telnetlib
import subprocess


episodes = 100000
host = "localhost"

cmd = "cd | rcssserver"

print("start")
subprocess.call(cmd)
print("end")

# for episode in range(episodes):
#     # <サーバーを開く>
#     # 新たにターミナル1を立ち上げる
#
#     # 「rcssserver」と入力する
#
#     # <クライアントを登録する>
#     # 新たにターミナル2を立ち上げる
#
#     # 「cd Zidan/src/ | python3 zidan2.py」と入力する
#
#     # <学習>
#
#     # <ターミナルを削除する>
#
#
#     # サーバーを閉じる
#     tn = telnetlib.Telnet(host, 23, 5)
#     print("session runs")
#     tn.write('\x03')
