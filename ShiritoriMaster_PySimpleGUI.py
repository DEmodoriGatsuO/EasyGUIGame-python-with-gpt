# -----------------------------------------------------------------------------
# Script Name: ShiritoriMaster_PySimpleGUI.py
# Description: Japanese Siritori With GPT
# Author: ChatGPT with De'modori Gatsuo
# Created Date: 2023.09.18
# -----------------------------------------------------------------------------
import os
import openai
import PySimpleGUI as sg
import re

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
ENGINE = os.getenv("OPENAI_API_ENGINE")
SYSYEM_RULE = ("あなたはこれからしりとりをしてもらいます。\n"
               "・「ん」で終わる言葉を使ってはいけません。\n"
               "・過去に出た単語を出力してはいけません。\n"
               "もし相手が上記のルールに違反している場合は、下記を伝えてください。\n"
               "「ルール違反です。」\n"
               "上記に該当しない場合は、相手の言葉の最後の文字から始まる単語を述べてください。"
               "出力はひらがなかカタカナでお願いします。")

# 正規表現を使用して、文字列内のカタカナ文字をひらがなに変換する関数
def to_hiragana(word):
    return re.sub(r'[\u30A1-\u30FA]', lambda ch: chr(ord(ch.group(0)) - 0x60), word)

# ルール違反の確認
def check_rule_violation(word, last_char):
    word_hiragana = to_hiragana(word)
    if word_hiragana in used_words:
        return True
    if word[-1] in ['ん', 'ン']:
        return True
    if last_char and to_hiragana(word[0]) != to_hiragana(last_char):
        return True
    return False

# メインウィンドウのレイアウトを設定
sg.theme('Black')

# レイアウトの設定
layout = [
    [sg.Text("Rule Violations: ", text_color="red"), sg.Text('0', key='-VIOLATIONS-', size=(5,1)), sg.Button('Reset')],
    [sg.Multiline(size=(60, 20), key="-DISPLAY-", disabled=True, autoscroll=True)],
    [sg.InputText(key="-INPUT-", size=(50, 1)), sg.Button("Send", key="-SEND-", bind_return_key=True)]
]

window = sg.Window("Word Chain Game", layout, font=('Segoe UI',12), finalize=True)

query_history = [{"role":"system","content":SYSYEM_RULE}]
conversation_history = []
used_words = []
violations = 0
last_word = ''

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Reset":
         # ユーザーの入力を履歴に追加
        query_history = [{"role":"system","content":SYSYEM_RULE}]
        conversation_history = []
        used_words = []
        violations = 0
        last_word = ''
        window["-DISPLAY-"].update('')
        window["-VIOLATIONS-"].update(violations)

    if event == "-SEND-":
        user_input = values["-INPUT-"]
        window["-INPUT-"].update('')
        
        if user_input:
            query_history.append({"role": "user", "content": user_input})
            conversation_history.append(f"user: {user_input}")
            used_words.append(to_hiragana(user_input))
            window["-DISPLAY-"].print("user: " + user_input)
            
            if check_rule_violation(user_input, last_word[-1] if last_word else None):
                violations += 1
                window["-VIOLATIONS-"].update(violations)

            last_word = user_input
            
           #  gpt3.5 turboで懸賞 
            ai_response = openai.ChatCompletion.create(
                engine=ENGINE,
                messages=query_history,
                temperature=0.7,
                max_tokens=100,
                top_p=0.95,
                frequency_penalty=2,
                presence_penalty=0,
                stop=None
            ).choices[0].message.content

            if check_rule_violation(ai_response, user_input[-1]):
                violations += 1
                window["-VIOLATIONS-"].update(violations)
            
            # AIのレスポンスを履歴に追加
            query_history.append({"role": "assistant", "content": ai_response})
            conversation_history.append(f"AI: {ai_response}")
            used_words.append(to_hiragana(ai_response))
            window["-DISPLAY-"].print("AI: " + ai_response)
            last_word = ai_response

window.close()