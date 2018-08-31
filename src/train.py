import telnetlib


episodes = 100000
host = "localhost"

for episode in range(episodes):
    # サーバーを開く

    # クライアントを登録する


    # サーバーを閉じる
    tn = telnetlib.Telnet(host, 23, 5)
    print("session runs")
    tn.write('\x03')
