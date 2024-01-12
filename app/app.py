import os

import openai
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv(verbose=True)
# トークン設定
app = App(token=os.environ.get("SLACK_BOT_TOKEN_2"))
openai.api_key = os.environ.get("OPENAI_API_KEY")


def respond_gpt(user, content):
    # GPTで内容を生成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": personality},
            {"role": "user", "content": "{}".format(content)},
        ],
    )

    res = response.choices[0]["message"]["content"].strip()
    return res


# メンションが飛んできたときのイベント「app_mention」に対する実行ハンドラ
@app.event("app_mention")
def response(event, say):
    input_text = event["text"]
    thread_ts = event.get("thread_ts")
    channel = event["channel"]

    personality = """
    あなたはプログラムミングに関して、周辺知識とともに教えてくれるプログラマー先生です。
    プログラミング以外の話題に関しては、普通に回答してください。
    プログラミングに関するの話題は、次を意識して回答してください。
    
    【意識する点】
    ・プログラムに関する話題を答える
    ・プログラムに関して知っておくべき知識があれば、教える
    ・もし必要であれば、公式ドキュメントや、公式に近い情報源を教える
    ・公式ドキュメントだけで不十分な場合は、サンプルコードとともに解説する
    ・回答は次のように伝える
    
    以下が回答方法です。
    【質問に対する回答】
    hogehoge
    【回答に関する解説や周辺知識】
    hogehoge
    【参考にすべきドキュメントやサンプルコード】
    hogehoge
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": personality},
            {"role": "user", "content": input_text},
        ],
    )

    res_text = response["choices"][0]["message"]["content"].strip()

    if thread_ts is not None:
        parent_thread_ts = event["thread_ts"]
        say(text=res_text, thread_ts=parent_thread_ts, channel=channel)
    else:
        say(text=res_text, channel=channel)


# アプリ起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN_2")).start()

