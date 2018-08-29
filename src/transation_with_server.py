import sys
from socket import *


def send(socket, address, port, command):
    if len(command) == 0:
        return
    # v8 以降は専用ソケットが必要なので作成
    # if command.startswith("(init "):
    # print("p1command No", self.m_iNumber, command)

    # ヌル終端文字列の欠損による警告を防ぐ
    command = command + "\0"

    try:
        to_byte_command = command.encode(encoding='utf_8')
        socket.sendto(to_byte_command, (address, port))
        # print("sending ", command, " is done")
        # else:
        #     to_byte_command = command.encode(encoding='utf_8')
        #     self.socket2.sendto(to_byte_command, (self.ADDRESS, self.PORT))
    except OSError:
        print("送信失敗")
        sys.exit()


def receive(socket, port):
    try:
        message, arr = socket.recvfrom(4096)
        message = message.decode("UTF-8")
        # ポート番号をｉｎｉｔに用いてモノから専用ソケットのものに変え無くてはならない！！！（重要）
        port = arr[1]
        # print("メッセージ（サーバーから", self.m_iNumber, "番）：", message)
        return message
    except OSError:
        print("受信失敗")
        sys.exit()
