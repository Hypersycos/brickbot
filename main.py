import discord
import os
import random
import re

#Discord client connection
client = discord.Client()

#Custom character strip for regex testing
def isregular(character):
    if character.isalpha():
        return True
    elif character in ['8','1','!']:
        return True
    else:
        return False

@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))
    
    #Brick counting
    client.brickcount = 0
    
    #Emojis
    client.brick = BrickEmojiGoesHere
    
    #Regular expression looking for bricks
    client.regex = re.compile('\w*[b8][b8\s]*[r\s]+[i1!\s]*[c\s]*[k\s]*[ck]')

@client.event
async def on_message(message):

    #Don't react to your own messages
    if message.author == client.user:
        return
        
    #Brickcount command
    elif message.content.lower() == "!brickcount":
        if client.brickcount == 0:
            await message.channel.send("There have been no bricks since the last count! " + client.brick)
        elif client.brickcount == 1:
            await message.channel.send("There has been 1 brick since the last count! " + client.brick)
        else:
            await message.channel.send("There have been " + str(client.brickcount) + " bricks since the last count! " + client.brick)
        client.brickcount = 0
        
    #Who is brickbot command
    elif message.content.lower() == "!brickbot":
        await message.channel.send("Brickbot is a bot that reacts to any messages containing the word brick with a " + client.brick + "!")
        
    #Experimental regex syntax matching
    elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))):
        await message.channel.send(client.brick)
        await message.add_reaction(client.brick)        
    
    #Did someone say brick??
    elif "brick" in "".join(filter(str.isalpha,message.content.lower())) or "🧱" in message.content.lower() or client.brick in message.content.lower():
        await message.channel.send(client.brick)
        await message.add_reaction(client.brick)
        client.brickcount += 1

#Logs in to the bot
client.run(TOKEN)