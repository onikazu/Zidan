# 引数にエピソード数入れる

# catchgame と　train を複合させて作成している

import player11
import threading
import numpy as np
import sys
import os
import time

from collections import deque


# episode_finish_flag = False

class Zidan2(player11.Player11, threading.Thread):
    def __init__(self):
        super(Zidan2, self).__init__()
        self.name = "Zidan"
        self.m_strCommand = ""

        # =============command log ===============
        self.kick_num = 0
        self.turn_num = 0
        self.dash_num = 0

        # =============for reinforcement learning=================
        # situation分割数
        self.num_digitized = 6
        self.situation_num = 6
        # actionについて
        self.action = 0
        self.actions = ("(turn 60)", "(turn -60)", "(dash 100)", "(dash -100)", "(kick 100 0)", "(kick 50 0)")
        self.action_num = len(self.actions)

        # reward(エピソードごと、ステップごと)
        self.episode_reward = 0
        self.reward = 0
        # 1試行のstep数
        self.max_number_of_steps = 600
        # 総試行回数
        # self.num_episodes = 100000
        self.num_this_episode = int(sys.argv[1])
        # 学習完了評価に使用する平均試行回数
        self.num_consecutive_iterations = 100
        # この報酬を超えると学習終了（中心への制御なし）
        self.goal_average_reward = 600
        # Qテーブルの作成
        if os.path.isfile("./npy/{0}_{1}_result_table.npy".format(self.m_strTeamName, self.m_iNumber)):
            self.q_table = np.load("./npy/{0}_{1}_result_table.npy".format(self.m_strTeamName, self.m_iNumber))
        else:
            # 初期のエピソードでなければ引き継ぎ行う。ここのsizeが大きいとエラーに。。。
            self.q_table = np.random.uniform(low=-1, high=1,
                                             size=(self.num_digitized ** self.situation_num, self.action_num))
        # 各試行の報酬を格納するベクトル（当然初期値は０で長さは評価数分）
        self.total_reward_vec = np.zeros(self.num_consecutive_iterations)

        self.state = 0
        self.next_state = 0

        # cartpoll のときのみ必要な変数（ただ出力するだけなのでそもそもいらない）
        # self.final_x = np.zeros((self.num_episodes, 1))  # 学習後、各試行のt=200でのｘの位置を格納
        self.islearned = 0  # 学習が終わったフラグ
        self.isrender = 0  # 描画フラグ
        self.sum_reward = 0  # 報酬の総量

    def analyzeMessage(self, message):
        """
        メッセージの解析
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
            self.initalize_and_learn()
            self.play_0()
            self.send(self.m_strCommand)
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
        # elif message.startswith("(player_type"):
        #     self.analyzePlayerType(message)
        #     # print("player_type_message", message)
        # think 処理
        elif message.startswith("(think"):
            self.send("(done)")
        # エラーの処理
        else:
            print("p11 サーバーからエラーが伝えられた:", message)
            print("p11 エラー発生原因のコマンドは右記の通り :", self.m_strCommand)

    # 実行
    def play_0(self):
        """
        コマンドの決定
        :return:
        """
        if self.checkInitialMode():
            if self.checkInitialMode():
                self.setKickOffPosition()
                command = \
                    "(move " + str(self.m_dKickOffX) + " " + str(self.m_dKickOffY) + ")"
                self.m_strCommand = command
        else:
            self.check_episode_end()
            # (コマンド生成)===================
            self.learn_and_play()
            # ==================================

    def check_episode_end(self):
        """
        1エピソードが終わったかどうか判定し終わっていたら報酬をリセットし、次のエピソードを始める準備をする
        :return:
        """

        # stepが規定step(600step) に達したか？
        if self.m_iTime % self.max_number_of_steps == 0 and self.m_iTime != 0:
            print("{}episode finished".format(self.num_this_episode))
            self.total_reward_vec = np.hstack((self.total_reward_vec[1:], self.episode_reward))  # 報酬を記録
            # ログの保存
            with open("./logs/{0}_{1}_reward.log".format(self.m_strTeamName, self.m_iNumber), "a") as the_file:
                the_file.write("{0},{1}\n".format(self.num_this_episode, self.episode_reward))

            # コマンドログの保存
            with open("./logs/{0}_{1}_command.log".format(self.m_strTeamName, self.m_iNumber), "a") as the_file:
                the_file.write(
                    "{0},{1},{2},{3}\n".format(self.num_this_episode, self.kick_num, self.turn_num, self.dash_num))

            # Qtable の保存
            np.save("./npy/{0}_{1}_result_table.npy".format(self.m_strTeamName, self.m_iNumber), self.q_table)
            time.sleep(100)

    def learn_and_play(self):
        # a_t実行によるs_t+1
        t = self.m_iTime
        observation = (self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY, self.m_dNeck, self.m_dStamina)
        if self.m_iNumber == 10:
            if t % 30 == 0:
                print("obsertvation:", observation)
        self.state = self.digitize_state(observation)
        self.reward = 0

        # (報酬の設定)==================================================-
        # 右チーム
        if self.m_strSide.startswith("r"):
            # ゴールすれば
            if self.m_strPlayMode == "(goal_r)":
                self.reward += 1000

        # 左チーム
        if self.m_strSide.startswith("l"):
            # ゴールすれば
            if self.m_strPlayMode == "(goal_l)":
                self.reward += 1000

        # 共通
        # ボールをキックできれば
        if self.getDistance(self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY) <= 0.7 and \
                self.m_strCommand.startswith("(kick"):
            self.reward += 1
        # ==================================================-

        self.episode_reward += self.reward
        self.m_strCommand = self.actions[self.action]
        if self.m_strCommand.startswith("(turn"):
            self.turn_num += 1
        if self.m_strCommand.startswith("(dash"):
            self.dash_num += 1
        if self.m_strCommand.startswith("(kick"):
            self.kick_num += 1

    def initalize_and_learn(self):
        t = self.m_iTime
        obserbvation = (self.m_dX, self.m_dY, self.m_dBallX, self.m_dBallY, self.m_dNeck, self.m_dStamina)
        self.state = self.digitize_state(obserbvation)
        self.action = np.argmax(self.q_table[self.state])
        # 開始直後でなければ学習
        if self.m_iTime % 300 != 0:
            self.next_state = self.digitize_state(obserbvation)
            self.q_table = self.update_Qtable(self.q_table, self.state, self.action, self.reward, self.next_state)
            self.action = self.get_action(self.next_state, self.num_this_episode)
            self.state = self.next_state

    # [1]Q関数を離散化して定義する関数　------------
    # 観測した状態を離散値にデジタル変換する
    def bins(self, clip_min, clip_max, num):
        return np.linspace(clip_min, clip_max, num + 1)[1:-1]

    # 各値を離散値に変換
    def digitize_state(self, observation):
        dX, dY, dBallX, dBallY, dNeck, dStamina = observation
        # 観測値がどのひだりからかぞえてどのビンに相当するかarrayを返す
        digitized = [
            np.digitize(dX, bins=self.bins(-52.5, 52.5, self.num_digitized)),  # dX
            np.digitize(dY, bins=self.bins(-34.0, 34.0, self.num_digitized)),  # dY
            np.digitize(dBallX, bins=self.bins(-52.5, 52.5, self.num_digitized)),  # dBallX
            np.digitize(dBallY, bins=self.bins(-34.0, 34.0, self.num_digitized)),  # dBallY
            np.digitize(dNeck, bins=self.bins(-90.0, 90.0, self.num_digitized)),  # dNeck
            np.digitize(dStamina, bins=self.bins(0, 8000, self.num_digitized)),  # dStamina
        ]

        # リスト内包表記
        # enumerateはインデックスと要素を返す
        return sum([x * (self.num_digitized ** i) for i, x in enumerate(digitized)])

    # [2]行動a(t)を求める関数 -------------------------------------
    def get_action(self, next_state, episode):
        # 徐々に最適行動のみをとる、ε-greedy法
        epsilon = 0.5 * (1 / (episode + 1))
        if epsilon <= np.random.uniform(0, 1):
            next_action = np.argmax(self.q_table[next_state][:])
        else:
            # action数は7個
            next_action = np.random.choice([i for i in range(self.action_num)])
        return next_action

    # [3]Qテーブルを更新する関数 -------------------------------------
    def update_Qtable(self, q_table, state, action, reward, next_state):
        gamma = 0.99
        alpha = 0.5
        next_Max_Q = max(q_table[next_state][:])
        q_table[state, action] = (1 - alpha) * q_table[state, action] + \
                                 alpha * (reward + gamma * next_Max_Q)
        return q_table


if __name__ == "__main__":
    plays = []
    for i in range(22):
        p = Zidan2()
        plays.append(p)
        teamname = str(p.__class__.__name__)
        if i < 11:
            teamname += "left"
        else:
            teamname += "right"
        plays[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        plays[i].start()

# 離散化させなくてはならない？(6分割**5変数の状態が生み出される)
# 状態s一覧
#
# self.m_dX
# self.m_dY
# self.m_dNeck
# self.m_dBallX
# self.m_dBallY
#
# 行動a一覧
# (turn 60)
# (turn -60)
# (dash 100)
# (dash -100)
# (kick 100 0)
# (kick 50 0)
