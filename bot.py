import asyncio
import discord
from discord.ext import commands
import os

# 1. 設定項目（ここを書き換えるだけで自由に変更可能）
DEFAULT_MESSAGE = "@everyone らて王国 top join now!!! お前ら対策ちゃんとしろよーw　雑魚鯖gg　強くなるためにらて王国に入ろう！https://discord.gg/2533XDQC3s"
DEFAULT_IMAGE = "image.png"
SPAM_COUNT = 10

bot = commands.Bot(
    intents=discord.Intents.default(),
    # 2. ユーザーインストール対応
    default_command_integration_types={
discord.AppInstallationType.user,
    },
)

# 3. 自分専用の操作ボタン
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
    async def start_spam(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("スパムを開始します...", ephemeral=True)
        for i in range(SPAM_COUNT):
            try:
                # 画像の有無を確認して送信
                if os.path.exists(DEFAULT_IMAGE):
                    await interaction.followup.send(DEFAULT_MESSAGE, file=discord.File(DEFAULT_IMAGE))
                else:
                    await interaction.followup.send(DEFAULT_MESSAGE)
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.5)

@bot.event
async def on_ready():
    # 4. コマンドの自動同期
    await bot.sync_commands()
    print(f"ログイン成功: {bot.user}")

# 5. /spam コマンド (反応確認用テスト機能付き)
@bot.slash_command(name="spam", description="自分専用のスパム操作パネルを表示")
async def spam(ctx: discord.ApplicationContext):
    # 自分にしか見えないボタンを生成
    view = PrivateSpamView(user_id=ctx.author.id)
    await ctx.respond("以下のボタンでスパムを実行できます。（このメッセージはあなたにしか見えません）", view=view, ephemeral=True)

# 動作確認用テストコマンド (このサーバーでボットが正常に動くか確認できます)
@bot.slash_command(name="test", description="ボットが正常に動いているか確認")
async def test(ctx: discord.ApplicationContext):
    await ctx.respond(f"ボットは正常に稼働中です！実行者: {ctx.author.name}", ephemeral=True)

from dotenv import load_dotenv
load_dotenv()
bot.run(os.environ.get('TOKEN'))
