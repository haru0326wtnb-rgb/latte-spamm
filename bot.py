import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# インテント（権限）の定義
intents = discord.Intents.default()
intents.message_content = True

# ボットの設定
bot = commands.Bot(
    intents=intents,
    command_prefix="!",
    # ユーザーインストール対応（指定された設定）
    default_command_integration_types={
        discord.AppInstallationType.user: True,
    },
)

# スパム操作用のビュー（ボタン）
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
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.5)

@bot.event
async def on_ready():
    # コマンドの同期
    try:
        await bot.tree.sync()
        print(f"ログイン成功: {bot.user} | 同期完了。")
    except Exception as e:
        print(f"同期エラー: {e}")

# スラッシュコマンド：スパムパネルの表示
@bot.tree.command(name="spam", description="スパム操作パネルを表示")
async def spam(interaction: discord.Interaction):
    view = PrivateSpamView(user_id=interaction.user.id)
    await interaction.response.send_message("以下のボタンで操作してください:", view=view, ephemeral=True)

# スラッシュコマンド：動作確認
@bot.tree.command(name="test", description="ボットの状態確認")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("ボットは正常に稼働中です。", ephemeral=True)

# ボットの起動（Renderの環境変数TOKENを読み込み）
bot.run(os.environ.get('TOKEN'))
