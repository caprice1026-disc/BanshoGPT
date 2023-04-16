import discord
import discord.ext.commands
import os
import openai
import oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#認証情報を設定
scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#シートを開く&chatGPTの設定をした部分を読み取る
sheet = client.open("{banshoGPT}").sheet1
#シート名の設定のとこを見直すこと まず設定を変えること　https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet
sheet.get_all_cells()

TOKEN = ("discordbot_TOKEN")
openai.api_key = "YOUR_OPENAI_API_KEY"
#モデルのとこは任意に変更しておく
model_engine = "GPT-3.5-turbo"

intents = discord.Intents.all()
discordclient = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
prefix = "/"

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()



tree.command(name="talk",description="chatGPT-と話すコマンドです。")
@discord.app_commands.describe(text="送りたい文章を書き込んでください。")
async def talk(interaction: discord.Interaction,text: str):
    #返信の内容を取得＆AIの返答を取得 毎回取得してたら遅そうだし先に取得して適応させておきたい。(18行目辺りを参照)
    response = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    await interaction.response.send_message(response.choices[0].text)
    #返信の内容を取得＆AIの返答を取得してシートに書き込む
    
    

discordclient.run(TOKEN)

  
'''参考文献として使用可能なもの
https://www.twilio.com/ja/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp
''' 
