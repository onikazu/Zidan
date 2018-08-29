from socket import *
import threading
import sys


class MainPlayer(threading.Thread):
    def __init__(self):
        # 通信用の変数
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

        # プレイヤーの詳細
        self.m_strPlayMode = ""
        self.m_iNumber = 0
        self.m_strTeamName = ""
        self.m_strHostName = ""
        self.m_strSide = ""
        self.m_debugLv01 = False


    def send(self, command):
        """
        サーバーへコマンドを送信する
        :param command: 送信コマンド
        :return: none
        """
        if len(command) == 0:
            return
        # ヌル終端文字列の欠損による警告を防ぐ
        command = command + "\0"
        try:
            to_byte_command = command.encode(encoding='utf_8')
            self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
        except OSError:
            print("送信失敗")
            sys.exit()

    def receive(self):
        """
        サーバーからメッセージを受信する。
        またポート番号を初期状態から変更する
        :return message: メッセージ
        """
        try:
            message, arr = self.socket.recvfrom(4096)
            message = message.decode("UTF-8")
            # ポート番号をｉｎｉｔに用いてモノから専用ソケットのものに変え無くてはならない！！！（重要）
            self.PORT = arr[1]
            # print("メッセージ（サーバーから", self.m_iNumber, "番）：", message)
            return message
        except OSError:
            print("受信失敗")
            sys.exit()
            return ""


    def initialize(self, number, team_name, server_name, server_port):
        """
        選手の初期登録
        :param number:
        :param team_name:
        :param server_name:
        :param server_port:
        :return:
        """
        self.m_iNumber = number
        self.m_strTeamName = team_name
        self.m_strHostName = server_name
        self.PORT = server_port
        # バージョンを指定しないと自動でバージョン３のプロトコルが動作する。
        if self.m_iNumber == 1:
            command = "(init " + self.m_strTeamName + "(goalie)(version 15.40))"
        else:
            command = "(init " + self.m_strTeamName + "(version 15.40))"
        self.send(command)

    def run(self):
        """
        threadでメッセージを受信し続ける、そして解析を行う
        :return:
        """
        while True:
            message = self.receive()
            # print(message)
            self.analyzeMessage(message)

    def analyzeInitialMessage(self, message):
        """
        選手の登録、詳細の入力を行う
        :param message:
        :return:
        """
        index0 = message.index(" ")
        index1 = message.index(" ", index0 + 1)
        index2 = message.index(" ", index1 + 1)
        index3 = message.index(")", index2 + 1)

        self.m_strSide = message[index0+1:index1]
        self.m_iNumber = int(message[index1+1:index2])
        self.m_strPlayMode = message[index2+1:index3]

    def analyzeMessage(self, message):
        """
        messageの解析を行う
        :param message:
        :return:
        """
        # 初期メッセージの処理
        # print("p11:message:", message)
        if message.startswith("(init "):
            self.analyzeInitialMessage(message)
        # 視覚メッセージの処理
        elif message.startswith("(see "):
            self.analyzeVisualMessage(message)
        # 体調メッセージの処理
        elif message.startswith("(sense_body "):
            self.analyzePhysicalMessage(message)
            if self.m_iVisualTime < self.m_iTime:
                self.predict(self.m_iVisualTime, self.m_iTime)
            self.play_0()
            self.send(self.m_strCommand[self.m_iTime])
        # 聴覚メッセージの処理
        elif message.startswith("(hear "):
            self.analyzeAuralMessage(message)
        # サーバパラメータの処理
        elif message.startswith("(server_param"):
            self.analyzeServerParam(message)
        # プレーヤーパラメータの処理
        elif message.startswith("(player_param"):
            self.analyzePlayerParam(message)
        # プレーヤータイプの処理
        elif message.startswith("(player_type"):
            self.analyzePlayerType(message)
            # print("player_type_message", message)
        # エラーの処理
        else:
            print("p11 サーバーからエラーが伝えられた:", message)
            print("p11 エラー発生原因のコマンドは右記の通り :", self.m_strCommand[self.m_iTime])


if __name__ == "__main__":
    players = []
    for i in range(11):
        p = Player1()
        players.append(p)
        players[i].initialize(i+1, "kazu", "localhost", 6000)
        players[i].start()

    players[0].m_debugLv01 = True
    print("試合登録完了")