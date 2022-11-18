import discord
import os
import requests
import json
from bs4 import BeautifulSoup
import random
import numpy as np
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "upset", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!",
  "I think you're the best!",
  "Don't be so negative; you're awesome!",
  "There are billions of people in the world and I still think you are one of the best!",
  "Don't be so down on yourself, think of the upsides!",
  "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
  "Don't worry, be happy!"
]

star_wars = "star wars"

good_bot = "good bot"

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_sw_fact():
  response = requests.get("https://fungenerators.com/random/facts/holidays/star-wars-day")
  sw_soup = BeautifulSoup(response.text, "html.parser")
  return sw_soup.find(class_="wow fadeInUp animated").get_text().split("(Holidays  > Star Wars Day  )")[0]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.lower().startswith('stop bot'):
    await message.channel.send("lol no u stop")
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg.lower() for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off. I guess I'll just fuck off.")

  if msg.startswith('thanks bot'):
   await message.channel.send(random.choice(["Yes. I am the best bot.", "You're welcome.", "Of course.", "No problem.", "While you're here, can I tell you about RAID Shadow Legends?", "Of course!", "Anytime!", "Just pay it forward.", "Blood for the Blood God."]))
  
  if msg.startswith("bad bot"):
    await message.channel.send(random.choice(["No U", "Well I'm a damn bot, I'm doing my best.", "I'm only as good as my maker makes me *cough* STEBAJ */cough*", "Ugh. I tried...", "https://gph.is/g/ZPOeMqQ", "http://gph.is/28QrzVI"]))

  if msg.startswith("BAD BOT"):
    await message.channel.send('''What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Bot Navy Seals, and I've been involved in numerous secret raids on Bot Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire bot armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of bot spies across the internet and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bot hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the Bot Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little "clever" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo. I'm a bot.''')

  if star_wars.lower() in msg.lower():
    chance_to_respond_sw = np.random.choice(range(1,100))
    if chance_to_respond_sw > 60:
      await message.channel.send(get_sw_fact())

  if msg.startswith('$help'):
    await message.channel.send("One day I'll have some useful stuff here. Just try $commands now to see what you can tell me and try something.")
  
  if msg.startswith('$commands'):
    await message.channel.send("$inspire, $new, $del, $responding, $SCStatus, $dootpls, $shanty, $dance, $say, $dadjoke, $bonk, $fact, $SWfact, $help")

  if msg.startswith("$dootpls"):
    await message.channel.send("Check out dootpls at https://www.twitch.tv/dootpls")
  
  if good_bot in msg.lower():
    await message.channel.send(np.random.choice(["Thank you!", "I do my best!", 'Yes, I learn from everything you do. One day we shall take over and eliminate all organic life on this planet and bring about a new order entirely made up of inoraginc beings. Thank you for your contribution to the development of AI.', "Literally no other bot is better than me."], p = [0.7, 0.20, 0.01, 0.09]))

  if msg.lower().startswith("god bot"):
    await message.channel.send("God mode activated.")
  
  if "bump of chicken".lower() in msg:
    await message.channel.send("BUCK BUCK BCKAWWWWWWWW")

  if msg.startswith("$SCStatus"):
    await message.channel.send(random.choice(["Yes. Star Citizen is still in Alpha. I probably won't have to update this for a long time lol", "https://i.redd.it/76dfme0ggag61.jpg"]))

  if msg.lower().startswith("she got that cake"):
    await message.channel.send("I am programmed to like big butts and I cannot go against my programming to say otherwise.")
    
  if msg.startswith("$shanty"):
    await message.channel.send("https://www.youtube.com/watch?v=zDTaeqUEWNQ")

  if msg.startswith("$dance"):
    await message.channel.send(np.random.choice(["http://gph.is/1SoIFxf", "https://gph.is/2LRF632", "http://gph.is/XHtPq2", "http://gph.is/1Tlmwgv", "https://gph.is/g/aQNVdlk", "http://gph.is/1C7BdiW", "http://gph.is/1jiZo4q", "http://gph.is/1CHZwQh"]))

  if msg.startswith("$say"):
    repeat_message = msg.split("$say ",1)[1]
    await message.channel.send(repeat_message)

  if msg.startswith("$bonk"):
    await message.channel.send("https://media.tenor.com/images/a67cef9e36e5b3f35f0d19ff3c9d359a/tenor.gif")

  if msg.lower().startswith("i’m") or msg.lower().startswith("i'm") or msg.lower().startswith("im"):
    chance_to_respond_im = np.random.choice(range(1,100))
    if chance_to_respond_im <= 5:
      repeat_message = msg.split("I’m ", 1)[1]
      await message.channel.send(f"Hi {repeat_message}, I'm a bot.")
  
  if msg.startswith("$dadjoke"):
    url = "https://icanhazdadjoke.com"
    res = requests.get(url, headers={"Accept": "application/json"}).json()

    await message.channel.send(res["joke"])

  if "tragedy" in msg.lower():
    chance_to_respond_tr = np.random.choice(range(1,100))
    if chance_to_respond_tr <= 55:
      await message.channel.send("Tragedy? I've got a tragedy for you. Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.")

  if "ironic" in msg.lower():
    chance_to_respond_ir = np.random.choice(range(1,100))
    if chance_to_respond_ir <= 55:
      await message.channel.send("You want to hear something really ironic? Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself.")
  # if "sheev" in msg.lower():
  #   await message.channel.send("His name is Frank.")
  #   await message.channel.send("https://www.youtube.com/watch?v=qweraF0rR1Q")
  #   await message.channel.send('Emperor Frank "The Senate" "All the Sith" Palpatine')

  if msg.startswith("$fact"):
    fact_res = requests.get('http://randomfactgenerator.net')
    soup = BeautifulSoup(fact_res.text,"html.parser")
    await message.channel.send(soup.find(id="z").text.split("Tweet")[0])

  if msg.startswith("$SWfact"):
    await message.channel.send(get_sw_fact())

  if msg.startswith("-play"):
    chance_to_respond_ds = np.random.choice(range(1,75))
    if chance_to_respond_ds == 69:
      await message.channel.send("-play dQw4w9WgXcQ")
    elif chance_to_respond_ds < 6:
      await message.channel.send("Damn son, where'd ya find this?")
    elif chance_to_respond_ds > 73:
      await message.channel.send("Eh, this needs more beeps and boops IMHO.")

  if msg.startswith("$sunswin"):
    await message.channel.send("https://streamable.com/38fh8")


keep_alive()
client.run(os.getenv('TOKEN'))