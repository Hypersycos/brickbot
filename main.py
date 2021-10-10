import discord
import os
import random
import re
import json
#import brickbot_arg

from dotenv import load_dotenv

# Brickbot invite link
# https://discord.com/api/oauth2/authorize?client_id=819688841527033927&permissions=265280&scope=bot

# dotenv variable grabbing
load_dotenv()
token = os.getenv("discord_token")
excluded_channels = json.loads(os.getenv("excluded_channels"))
commands_channels = json.loads(os.getenv("commands_channels"))
promoted_channels = json.loads(os.getenv("promoted_channels"))


#Discord client connection
client = discord.Client(activity=discord.Game(name="Brick"))

#Brick counting
client.brickcount = 0

#Emojis
#Brick-type (non-flag)
client.brick = str(os.getenv("brick"))
client.pickle_brick = str(os.getenv("pickle_brick"))
client.brick_beer = str(os.getenv("brick_beer"))
client.brick_sign = str(os.getenv("brick_sign"))
#Flags
client.brick_lesbian = str(os.getenv("brick_lesbian"))
client.brick_ace = str(os.getenv("brick_ace"))
client.brick_bi = str(os.getenv("brick_bi"))
client.brick_lgbt = str(os.getenv("brick_lgbt"))
client.brick_nb = str(os.getenv("brick_nb"))
client.brick_trans = str(os.getenv("brick_trans"))
#Others
client.thank_you = str(os.getenv("thank_you"))
client.extreme_sadness = str(os.getenv("extreme_sadness"))

#Flag list (for random calling)
client.all_flags = [client.brick_ace,client.brick_bi,client.brick_lesbian,client.brick_lgbt,client.brick_nb,client.brick_trans]

#Regular expression looking for bricks
client.regex = re.compile('[b8]+r+[i1!]*c+[ck]')

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

@client.event
async def on_message(message):

    #Don't react to your own messages
    if message.author == client.user:
        return
    
    #Don't interact with excluded channels
    if message.channel.id in excluded_channels:
        return
    
    #The commands channel in brickbot's server
    if message.channel.id in commands_channels:
    
        #Return list of channels that brickbot is in
        if message.content.lower() == "!channels":
            for guild in client.guilds:
                responsetext = "Guild -- **" + str(guild) + "**: " + str(guild.id) + "\n"
                for channel in guild.text_channels:
                    responsetext += "\n**" + str(channel) + "**: " + str(channel.id)
                await message.channel.send(responsetext)
                
        #Returns the name and guild of a particular channel id
        elif message.content.lower()[0:12] == "!channelname":
            channel = client.get_channel(int(message.content[13:31]))
            await message.channel.send("Channel is `" + str(channel) + "`, id=`" + str(channel.id) + "` in guild `" + str(channel.guild) + "`.")
            
        #Sends a message to the channel id (syntax: !sendmessage CHANNELID message)
        elif message.content.lower()[0:12] == "!sendmessage":
            channel = client.get_channel(int(message.content[13:31]))
            await channel.send(message.content[32:len(message.content)])
            await message.channel.send("Sent message '" + message.content[32:len(message.content)] + "' to channel '" + str(channel) + "'")
        
        #Deletes a message based on its id (syntax: !deletemessage MESSAGEID CHANNELID)
        elif message.content.lower()[0:14] == "!deletemessage":
            channel = client.get_channel(int(message.content[34:52]))
            msg = await channel.fetch_message(int(message.content[15:33]))
            await msg.delete()
            await message.channel.send("Deleted message '" + msg.content + "' from channel '" + str(channel) + "'")
        
        #Echoes a message in print
        elif message.content.lower()[0:5] == "!echo":
            await message.channel.send("Echoing message!")
            print(message.content[6:len(message.content)])
        
        #Brick reacts a maessage (syntax: !brickreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:11] == "!brickreact":
            channel = client.get_channel(int(message.content[31:49]))
            msg = await channel.fetch_message(int(message.content[12:30]))
            await msg.add_reaction(client.brick)
            await message.channel.send("Reacted to message '" + msg.content + "' with " + client.brick)
        
        #Brick_beer reacts a maessage (syntax: !brickbeerreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:15] == "!brickbeerreact":
            channel = client.get_channel(int(message.content[35:54]))
            msg = await channel.fetch_message(int(message.content[16:34]))
            await msg.add_reaction(client.brick_beer)
            await message.channel.send("Reacted to message '" + msg.content + "' with " + client.brick_beer)
        
        #Experimental DM feature
        elif message.content.lower() == "!dmme":
            await message.author.send("Hi!")
        
        #No known command
        else:
            await message.channel.send("Command failed")
    
    #Flag reactions
    if "asexual" in message.content.lower() or "ace" in message.content.lower():
        await message.add_reaction(client.brick_ace)
        print("Asexual reacted in " + str(message.channel))
    if "bisexual" in message.content.lower():
        await message.add_reaction(client.brick_bi)
        print("Bisexual reacted in " + str(message.channel))
    if "lesbian" in message.content.lower():
        await message.add_reaction(client.brick_lesbian)
        print("Lesbian reacted in " + str(message.channel))
    if "gay" in message.content.lower() or "lgbt" in message.content.lower() or "queer" in message.content.lower():
        await message.add_reaction(client.brick_lgbt)
        print("LGBT reacted in " + str(message.channel))
    if "non-binary" in message.content.lower() or "nonbinary" in message.content.lower() or "non binary" in message.content.lower():
        await message.add_reaction(client.brick_nb)
        print("Nonbinary reacted in " + str(message.channel))
    if "trans" in message.content.lower():
        await message.add_reaction(client.brick_trans)
        print("Trans reacted in " + str(message.channel))
    # if "aro" in message.content.lower():
        # await message.add_reaction(client.brick_aro)
        # print("Aro reacted in " + str(message.channel))
    
    #!bb-help command
    if message.content.lower() == "!bb-help":
        await message.author.send("Current brickbot commands are:\n•`!bb-help`\tThat's this command! The command list is sent as a DM.\n•`!bb-help-here`\tI'll send this list to the channel, rather than as a DM\n•`!areyoutherebb`\tI'll respond with 'Yes' (if I'm online)\n•`!brickbot`\tApproximate explanation of who I am\n•`!brickrepo`\tI'll link my GitHub repository!")
        await message.channel.send("Command list sent as a direct message!")
        print("!bb-help command in channel " + str(message.channel))
    
    #!bb-help-here command
    elif message.content.lower() == "!bb-help-here":
        await message.channel.send("Current brickbot commands are:\n•`!bb-help`\tSends my command list as a DM.\n•`!bb-help-here`\tThat's this command! I send my command list to the channel\n•`!areyoutherebb`\tI'll respond with 'Yes' (if I'm online)\n•`!brickbot`\tApproximate explanation of who I am\n•`!brickrepo`\tI'll link my GitHub repository!")
        print("!bb-help-here command in channel " + str(message.channel))
    
    #Is brickbot online command
    elif message.content.lower() == "!areyoutherebb":
        await message.channel.send("Yes! " + client.brick)
        
    # #Brickcount command
    # elif message.content.lower() == "!brickcount":
        # if client.brickcount == 0:
            # await message.channel.send("There have been no bricks since the last count! " + client.brick)
        # elif client.brickcount == 1:
            # await message.channel.send("There has been 1 brick since the last count! " + client.brick)
        # else:
            # await message.channel.send("There have been " + str(client.brickcount) + " bricks since the last count! " + client.brick)
        # print("Brickcount for " + str(client.brickcount) + " bricks in channel " + str(message.channel))
        # client.brickcount = 0
        
    #Who is brickbot command
    elif message.content.lower() == "!brickbot":
        await message.channel.send("Brickbot is a bot that reacts to any messages containing the word brick with a " + client.brick + "! For a full list of commands, type '!bb-help'.")
        print("!brickbot in channel " + str(message.channel))
    
    #Brickbot repository command
    elif message.content.lower() == "!brickrepo":
        await message.channel.send("You can find the repository of my code at https://github.com/calliope1/brickbot")
        print("Brickrepo command activated in channel " + str(message.channel))
    
    #Pickle brick
    elif "pickle brick" in message.content.lower():
        await message.add_reaction(client.pickle_brick)
        await message.channel.send("I'm Pickle Brick!! " + client.pickle_brick)
        print("Pickle brick in channel " + str(message.channel))
        
    #Brickbot yes command
    elif "brickbot yes" in message.content.lower():
        await message.add_reaction(client.thank_you)
        await message.channel.send(client.thank_you)
        print("Brickbot yes in channel " + str(message.channel))
    
    #Brickbot no command
    elif "brickbot no" in message.content.lower():
        await message.add_reaction(client.extreme_sadness)
        await message.channel.send(client.extreme_sadness)
        print("Brickbot no in channel " + str(message.channel))
    
    #No fun command
    elif "no fun" in message.content.lower() or "nofun" in message.content.lower():
        await message.add_reaction(client.brick_sign)
        print("No fun reacted in channel " + str(message.channel))
    
        #React to pub messages from promoted channels with :brick_beer:
    elif message.channel.id in promoted_channels:
        if "pub" in message.content.lower():
            await message.channel.send(client.brick_beer)
            await message.add_reaction(client.brick_beer)
            print("Pub reacted to an announcement")
        elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))) or bool(client.regex.search("".join(filter(isregular,message.content.lower()[::-1])))) or "🧱" in message.content.lower():
            if not random.randint(0,99):
                emoji = client.all_flags[random.randint(0,len(client.all_flags))]
                await message.channel.send(emoji)
                await message.add_reaction(emoji)
            else:
                await message.channel.send(client.brick)
                await message.add_reaction(client.brick)
            print("Brick found in channel " + str(message.channel))
        elif not random.randint(0,19):
            await message.add_reaction(client.brick)
            print("Brick reacted to an announcement")

    #Regex syntax matching and brick finding
    elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))) or bool(client.regex.search("".join(filter(isregular,message.content.lower()[::-1])))) or "🧱" in message.content.lower():
        if not random.randint(0,99):
            emoji = client.all_flags[random.randint(0,len(client.all_flags))]
            await message.channel.send(emoji)
            await message.add_reaction(emoji)
        else:
            await message.channel.send(client.brick)
            await message.add_reaction(client.brick)
        print("Brick found in channel " + str(message.channel))
    
    #React to every hundredth (randomly) message with :brick:
    elif not random.randint(0,99):
        if not random.randint(0,99):
            emoji = client.all_flags[random.randint(0,len(client.all_flags))]
            await message.add_reaction(emoji)
        else:
            await message.add_reaction(client.brick)
        print("Brick reacted in channel " + str(message.channel))

#Logs in to the bot
client.run(token)
