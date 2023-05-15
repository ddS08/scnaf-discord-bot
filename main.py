import os
import discord
from discord.ext import commands
import musicyt
from keepalive import keepalive
cogs=[musicyt]

client=commands.Bot(command_prefix='-',intents=discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)

keepalive()
client.run(os.getenv('token'))
