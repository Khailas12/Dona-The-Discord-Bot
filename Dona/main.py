import discord
import os
import wikipedia
import requests
import json
import youtube_dl
import asyncio
from discord.ext import commands
import random
import pyjokes
from replit import db
from dona_server import keep_alive


client = discord.Client()
bot = commands.Bot(command_prefix="$")

def wiki_summary(arg):
    defenition = wikipedia.summary(
        arg, sentences=3, chars=1000, auto_suggest=True, redirect=True)
    return defenition


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def getactivity():
		response = requests.get("https://www.boredapi.com/api/activity")
		data = json.loads(response.content)
		activity = data["activity"]
		typeof = data["type"]
		conclude = f"Random Activity : {activity} \n\nActivity Type : {typeof}"
		return (conclude)

def getmeme():
	  response = requests.get("https://meme-api.herokuapp.com/gimme")
	  meme_data = json.loads(response.text)
	  meme = meme_data["preview"][2]
	  return (meme)


def update_command(dona_msg):
    if "!Dona" in db.keys():
        command = db["!Dona"]
        command.append(dona_msg)
        db["!Dona"] = command
    else:
        db["!Dona"] = [dona_msg]


def delete_command(index):
    command = db["!Dona"]
    if len(command) > index:
        del command[index]
        db["!Dona"] = command


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


hi_dona = ["hi", "hey", "hay", "hola", "hy", "hello", "heyy", "helo"]
hi_reply = [
    "Hey there ", "Wassup ", "How's it goin ", "Oh hey ", "Glad to meet ya "
]

bye_dona = ["bye", "bei", "bie", "cya"]
bye_dona_reply = ["Bye", "Cya around", "Take care", "Stay safe"]

sad_command = ["sad", "bad", "sed"]
starter_command = ["Cheer up", "Chill", "Stay safe"]

good_i = [
    "how's it goin?", "how are you?", "wyd?", "how ya doin?", "hw r u",
    "how are ya", "how r u", "r u", "ru"
]
good_q = ["Chillin", "Never Better", "So far so good", "vibing"]

age = [
    "how old are you", "how old are ya", "how old are u", "how old r u", "age",
    "what's ur age", "old r", "old are"
]
age_r = ["I'd rather not say that lol", "old enough", "I'm younger than you"]

dona_q = ["yes", "yea", "ya" "sure", "okay", "ok", "alr", "alright"]
dona_n = ["nah", "no", "nope", "nop"]

if "responding" not in db.keys():
    db["responding"] = True

info = discord.Embed(
    title="Hello, I'm DONA",
    description=
    "\n`Command for Result from Wiki:`\n**!search <input>**\nExample: **!search ariana**\n\n`Command for Info:`\n**!info**\n\n`Command for an Activity`\n**!activity**\n\n`Command For Fun:`\n**Dona,  Quote,  Joke** \n\nThe rest is all up to your preference often casually asking my age and saying hi, hello etc.\nI'll be replying according to the commands I'm assigned with.\n\n**Ty, with Love DONA** ❤️",
    colour=discord.Colour.red())


@bot.event
@client.event
async def on_message(message):
    if message.author == client.user:
      return
    # {message.channel}: {message.author}: {message.author.name}: {message.content}

    msg3 = message.content.split()
    msg2 = message.content.lower()
    msg = message.content

    imp_word = msg3[0:1000]
    if msg2.startswith("!search "):
        search = discord.Embed(
            title="Result",
            description=wiki_summary(imp_word),
            colour=discord.Colour.purple())
        await message.channel.send(content=f"**Requested by** <@{message.author.id}>", embed=search)


    if msg.startswith('!activity'):
        activity = getactivity()
        await message.channel.send(f"Hey, <@{message.author.id}>\n\n**{activity}**")
			
    if msg.startswith('meme'):
        memelink = getmeme()
        meme = discord.Embed(title=f"Random Meme Requested by {message.author.name}",description=memelink) 
        await message.channel.send(content=None,embed=meme)

    if any(word in msg2 for word in hi_dona):
        await message.channel.send(
            random.choice(hi_reply) + f"<@{message.author.id}>")

    if any(word in msg2 for word in bye_dona):
        await message.channel.send(random.choice(bye_dona_reply) + f" <@{message.author.id}>")

    if any(word in msg2 for word in good_i):
        await message.channel.send(random.choice(good_q))

    if message.content.lower().startswith("dona".lower()):
        channel = message.channel
        await channel.send(
            f'**Dona is here <@{message.author.id}>\nWanna hear a joke?**\n\nPlease reply "Yes"')

        def check(m):
            return m.content.lower() == "yes" and m.channel == channel

        ms = await client.wait_for("message", check=check)
        await channel.send(pyjokes.get_joke().format(ms))


    if any(word in msg2 for word in age):
        await message.channel.send(random.choice(age_r))

    if db["responding"]:
        options = starter_command
        if "!Dona" in db.keys():
            options = options + db["!Dona"]
        if any(word in msg2 for word in sad_command):
            await message.channel.send(random.choice(options))

    if msg.startswith("!add".lower()):
        dona_msg = msg.lower().split("!add", 1)[1]
        update_command(dona_msg)
        await message.channel.send("NEW ADDED")

    if msg.startswith("!del"):
        command = []
        if "!Dona" in db.keys():
            index = int(msg.split("!del", 1)[1])
            delete_command(index)
            command = db["!Dona"]
        await message.channel.send(command)

    if message.content.lower().endswith("quote"):
        quote = get_quote()
        await message.channel.send(f"Here's a Quote for you <@{message.author.id}>\n\n" + f"**{quote}**")

    if message.content.endswith("!online".lower()):
        await message.channel.send(f"Dona is Online <@{message.author.id}>")

    if message.content.lower().endswith("joke"):
      await message.channel.send(pyjokes.get_joke())
	
    if message.content.lower().startswith("!info"):
      await message.channel.send(f"**Requested by** <@{message.author.id}>",embed=info)

    if msg.startswith("!list"):
        command = []
        if "!Dona" in db.keys():
            command = db["!Dona"]
        await message.channel.send(command)

    if msg.startswith("!responding"):
        value = msg.split("!responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Dona is responding")
        else:
            db["responding"] = False
            await message.channel.send("Dona is not responding")

		

keep_alive()
client.run(os.getenv("TOKEN"))
