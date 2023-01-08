import discord
import requests
from secrets import app_id, app_key, discord_id


async def getJsonDict(word_id):
    language = "en-us"
    url = (
        "https://od-api.oxforddictionaries.com:443/api/v2/entries/"
        + language
        + "/"
        + word_id.lower()
    )
    r = requests.get(
        url,
        headers={"app_id": app_id, "app_key": app_key},
        params={"fields": "definitions", "strictMatch": "false"},
    )
    return r.json()


async def printRdictDefinitions(rdict):
    returnlist = ["__***Definitions:***__\n\n"]
    LexEntries = []
    for a in rdict["results"][0]["lexicalEntries"]:
        LexEntries.append(a)

    senses = []
    for b in LexEntries:
        if b is not LexEntries[0]:
            returnlist.append("\n\n-------------------------------\n")
        returnlist.append("__**" + b["lexicalCategory"]["text"] + "**__\n")
        senses.clear()
        senses += b["entries"][0]["senses"]
        count = 1
        for sense in senses:
            if sense is not senses[0]:
                returnlist.append("\n***ˣˣˣˣˣ***\n")
            for definition in sense["definitions"]:
                returnlist.append(f"*Def{count}:*  " + definition)
                count += 1
    returnstring = "".join(returnlist)
    return returnstring


Client = discord.Client()


@Client.event
async def on_ready():
    print(f"We have logged in as {Client.user}")


@Client.event
async def on_message(message):
    if message.author == Client.user:
        return
    if message.content.startswith("Bot1"):
        word_to_define = message.content[5:]
        try:
            await message.channel.send(
                await printRdictDefinitions(await getJsonDict(word_to_define))
            )
        except KeyError:
            await message.channel.send("Error. please try again with a valid word.")


Client.run(discord_id)
