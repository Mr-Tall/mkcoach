"""
Optional: Simple Discord bot that forwards messages to the Coach.
Requires creating a Discord bot token and setting DISCORD_TOKEN in .env.

pip install discord.py python-dotenv
python integrations/discord_bot.py
"""
import os
import discord
from dotenv import load_dotenv
from app.coach import Coach
from app.llm_local import OllamaLLM

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intent = discord.Intents.default()
intent.message_content = True
client = discord.Client(intents=intent)
coach = Coach(llm=OllamaLLM(), character="Johnny Cage")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("/combo") or message.content.startswith("/punish"):
        text = message.content.replace("/combo", "").replace("/punish", "").strip()
        reply, _ = coach.respond(text)
        await message.channel.send(reply[:1800])

if __name__ == "__main__":
    if not TOKEN:
        print("Set DISCORD_TOKEN in .env")
    else:
        client.run(TOKEN)
