import discord
import asyncio
import time
import os
import sys
from keepalive import keep_alive
intents = discord.Intents(members=True, messages=True, guilds=True, message_content=True, reactions=True)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("> AFK check, please react to the following message within 30 seconds if you aren’t AFK."):
    checkmessage = await message.channel.send("Please react with a :white_check_mark: to prove you are not AFK.")
    reacted = []
    await checkmessage.add_reaction('\U00002705')
    await asyncio.sleep(30)
    @client.event
    async def on_reaction_add(reaction, user):
      if reaction.message == checkmessage:
        try:
          await checkmessage.channel.send(f'{user} passed the AFK check.')
          reacted.append(user)
        except:
          await message.channel.send(f"{message.author.mention} Issue detected. Please ensure your DMs are on for the Trainings server.")
          await message.channel.send(f'{user} passed the AFK check.')
          reacted.append(user)
      else:
        print('kyle you screwed up you monkey')
    guild = message.author.guild
    reason = "AFK during training."
    for member in guild.members:
      if member in reacted:continue
      try:
        await member.kick(reason=reason)
        kickembed = discord.Embed(title=f"{member} has been kicked.")
        await message.channel.send(kickembed)
        print(f'{member} has been kicked.')
      except Exception as e:
        print(f'{member} is not a Trainee.')
        print(e)
    reacted.clear()
    await checkmessage.delete()
  if message.content.startswith("> That will conclude our lecture; moving with the quiz, you will have 12 minutes to respond to it, react with :white_check_mark: once you have finished. You will be kicked from the server after reacting."):
    await message.add_reaction("\U00002705")
    kicklog = []
    @client.event
    async def on_reaction_add(reaction, user):
      if reaction.message == message:
        kicklog.append(user)
        guild = message.author.guild
        for member in guild.members:
          if member in kicklog:
            await member.kick(reason="Finished training.")
        kicklog.clear()
          
keep_alive()
client.run(os.getenv('TOKEN'))
