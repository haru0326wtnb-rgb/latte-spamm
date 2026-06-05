import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# 環境変数の読み込み
load_dotenv()

# --- 1. Render用：Webサーバー機能 (タイムアウト対策) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"
def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
Thread(target=run_web, daemon=True).start()
# ----------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    intents=intents,
    command_prefix="!",
    default_command_integration_types={discord.AppInstallationType.user: True},
)

class PrivateSpamView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("実行者本人以外は操作できません。", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="スパム開始", style=discord.ButtonStyle.danger)
    async def start_spam(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("スパムを開始します...", ephemeral=True)
        message = "@everyone らて王国 top join now!!! https://discord.gg/2533XDQC3s"
        
        for i in range(10):
            try:
                if os.path.exists("image.png"):
                    await interaction.followup.send(message, file=discord.File("image.png"))
                else:
                    await interaction.followup.send(message)
                
                # 送信後の安全な待機時間
                await asyncio.sleep(2.0)
                
            except discord.HTTPException as e:
                # --- 2. レートリミット対策：Discordの制限を自動で守る ---
                if e.status == 429:
                    # ヘッダーから再試行可能時間を取得して待機
                    retry_after = float(e.response.headers.get("Retry-After", 5.0))
                    print(f"制限検知: {retry_after}秒待機します")
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    print(f"エラー発生: {e}")
                    break

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"ログイン成功: {bot.user}")

@bot.tree.command(name="spam", description="スパム操作パネルを表示")
async def spam(interaction: discord.Interaction):
    view = PrivateSpamView(user_id=interaction.user.id)
    await interaction.response.send_message("ボタンで操作してください:", view=view, ephemeral=True)

bot.run(os.environ.get('TOKEN'))
