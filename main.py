import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1459911881119502574)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} command(s) to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')



intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # good practice

client = Client(command_prefix="?", intents=intents)

GUILD_ID = discord.Object(id=1459911881119502574)

@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="print", description="Print string.", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="embed", description="Create an embed.", guild=GUILD_ID)
async def embed(interaction: discord.Interaction, titl: str, desc: str):
    embed = discord.Embed(
        title=titl,
        description=desc,
        color=discord.Colour.brand_green()
    )
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="loa", description="File for LOA.", guild=GUILD_ID)
async def loa(
    interaction: discord.Interaction,
    user: discord.Member,
    day: int,
    month: int,
    year: int,
    reason: str
):

    channel2 = interaction.guild.get_channel(1467556173422264452)

    if channel2 is None:
        await interaction.response.send_message("LOA channel not found.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📌 Leave of Absence Request.",
        description=f"{interaction.user.mention} has requested LOA.",
        color=discord.Color.red()
    )

    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="End Date", value=f"{day:02d}/{month:02d}/{year}", inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Filed By", value=interaction.user.mention, inline=False)

    embed.set_footer(text=f"User ID: {user.id}")

    await channel2.send(embed=embed)

    await interaction.response.send_message("LOA submitted successfully.", ephemeral=True)
    await msg.add_reaction("🟢")
    await msg.add_reaction("🔴")

@client.tree.command(name="session", description="Start a session/poll", guild=GUILD_ID)
@app_commands.choices(
    type=[
        app_commands.Choice(name="Start", value="start"),
        app_commands.Choice(name="Poll", value="poll"),
    ]
)
async def session(
    interaction: discord.Interaction,
    type: app_commands.Choice[str]
):
    channel = interaction.guild.get_channel(1467556288677281806)

    if channel is None:
        await interaction.response.send_message("Channel not found.", ephemeral=True)
        return

    if type.value == "start":
        embed = discord.Embed(
            title="🏁 Session Startup 🟢",
            description=f"""\
{interaction.user.mention} has started a session! Join up.

You can find the game link [here.](https://www.roblox.com/games/127209441614859/Our-Campus-V1)

||@everyone||
"""
        )

        await channel.send(embed=embed)
        await interaction.response.send_message("Session started.", ephemeral=True)

    elif type.value == "poll":
        embed = discord.Embed(
            title="🏁 Session Poll 🟢",
            description="""\
A session poll has started.

Press the green tick if you are attending,
the red X if you are NOT attending,
and the yellow circle if you're unsure.

Please check <#1459915331739848915> before joining in-game.

||@everyone||
"""
        )

        msg = await channel.send(embed=embed)

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        await msg.add_reaction("🟡")

        await interaction.response.send_message("Poll started.", ephemeral=True)
# 👇 Render Environment Variable Section
TOKEN = os.environ.get("TOKEN")

if TOKEN is None:
    raise ValueError("No TOKEN found in environment variables")

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

client.run(TOKEN)
