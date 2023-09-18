# -----------------------------------------------------------------------------
# Script Name: ShiritoriMaster_PyQt5.py
# Description: Japanese Siritori With GPT
# Author: ChatGPT with De'modori Gatsuo
# Created Date: 2023.09.18
# -----------------------------------------------------------------------------
import os
import openai
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

# global variant
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
ENGINE = os.getenv("OPENAI_API_ENGINE")
SYSYEM_RULE = "あなたはこれからしりとりをしてもらいます。\n・「ん」で終わる言葉を使ってはいけません。\n・過去に出た単語を出力してはいけません。\nもし相手が上記のルールに違反している場合は、下記を伝えてください。\n「ルール違反です。」\n上記に該当しない場合は、相手の言葉の最後の文字から始まる単語を述べてください。出力はひらがなかカタカナでお願いします。"

class ShiritoriGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("しりとりゲーム")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)

        self.send_button = QPushButton("送信")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.conversation_history = []
        self.query_history = [{"role":"system","content":SYSYEM_RULE}]
        self.current_word = ""

    def send_message(self):
        user_input = self.user_input.text()
        if user_input:
            self.conversation_history.append(f"user: {user_input}")
            self.query_history.append({"role":"user","content":user_input})
            self.update_chat_display()

            if len(self.conversation_history) >= 100:
                self.conversation_history.append("AI: 会話が終了しました。")
                self.update_chat_display()
                self.user_input.setReadOnly(True)
                self.send_button.setDisabled(True)
                return

            ai_response = self.get_openai_response()
            self.conversation_history.append(f"AI: {ai_response}")
            self.query_history.append({"role":"assistant","content":ai_response})
            self.update_chat_display()

    def get_openai_response(self):
        response = openai.ChatCompletion.create(
            engine=ENGINE,
            messages = self.query_history,
            temperature=0.7,
            max_tokens=100,
            top_p=0.95,
            frequency_penalty=2,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content

    def update_chat_display(self):
        conversation_text = "\n".join(self.conversation_history)
        self.chat_display.setPlainText(conversation_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shiritori_app = ShiritoriGame()
    shiritori_app.show()
    sys.exit(app.exec_())