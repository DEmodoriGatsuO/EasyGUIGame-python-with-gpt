# ShiritoriMaster

「ShiritoriMaster」はOpenAIとPySimpleGUIを使用して、ユーザーとAIがしりとりをするデスクトップアプリケーションです。

## feature

- ユーザーとAIがしりとりで対戦
- ゲームのルール違反数を表示
- ゲームを一からやり直すためのリセット機能

## setup

1. 必要なライブラリをインストール:
    ```
    pip install openai PySimpleGUI
    ```

2. OpenAIのAPIキーを環境変数にセットしてください

3. `ShiritoriMaster.py`を実行してゲームを開始:
    ```
    python ShiritoriMaster.py
    ```

## usage

1. ゲーム開始後、入力欄にしりとりの単語を入力して「Send」ボタンをクリック
2. GPTが続けて単語を出力します
3. ルール違反がある場合、違反数が更新されます
4. ゲームをリセットしたい場合は「Reset」ボタンをクリック

## rule

- 単語の最後の文字を使って次の単語を始める
- 「ん」で終わる言葉を使ってはいけない
- 過去に出た単語を再度使用することはできない