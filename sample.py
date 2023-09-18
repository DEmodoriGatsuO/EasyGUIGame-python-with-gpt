# OPENAI_API_BASE
# OPENAI_API_KEY
# OPENAI_API_ENGINE

import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
print(openai.api_base)
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
ENGINE = os.getenv("OPENAI_API_ENGINE")

response = openai.ChatCompletion.create(
  engine=ENGINE,
  messages = [{"role":"system","content":"あなたはこれからしりとりをしてもらいます。\n・「ん」で終わる言葉を使ってはいけません。\n・過去に出た単語を出力してはいけません。\nもし相手が上記のルールに違反している場合は、下記を伝えてください。\n「ルール違反です。」\n上記に該当しない場合は、相手の言葉の最後の文字から始まる単語を述べてください。出力はひらがなかカタカナでお願いします。"},{"role":"user","content":"りんご"}],
  temperature=0.7,
  max_tokens=200,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response["choices"][0]["message"]["content"])