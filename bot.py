import discord
from discord.ext.commands import Bot
import requests
from PIL import Image
from io import BytesIO
import random

BOT_PREFIX = ('?', '!')
TOKEN = 'XXXXXXXXXXXXXXXXXXXXX'
# make a list of links of it in the future to choose random site
TRUMP_QUOTE_URL = """https://www.tronalddump.io/random/quote"""
REDDIT_URLS = [
    """https://www.reddit.com/r/MemesOfTheGreatWar/.json""",
    """https://www.reddit.com/r/Dank/.json""",
    """https://www.reddit.com/r/dank_meme/.json"""
    """https://www.reddit.com/r/cursedimages/.json""",
    """https://www.reddit.com/r/Memes_Of_The_Dank/.json"""
    """https://www.reddit.com/r/cursedmemes/.json""",
    """https://www.reddit.com/r/memes/.json""",
    """https://www.reddit.com/r/Memes_Of_The_Dank/.json"""
]

client = discord.Client()
bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        channel = message.channel
        await channel.send(msg)

    await bot.process_commands(message) # enables commands

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_connect():
    channels = list(bot.get_all_channels())
    main_channel = None;
    for channel in channels:
        if (channel.name == "general") or (channel.name =="ogólny"):
            main_channel = channel
    await main_channel.send("""Hello there""")

@bot.command(name='meme',
             brief='Returns a random meme from reddit',
             alias=['MEME', 'Meme'])
async def meme(ctx):
    """
        Command for sending a random meme from Reddit
    """
    rand_subreddit = random.randint(0, len(REDDIT_URLS) - 1)
    rand_image = random.randint(0, 25)
    print(rand_subreddit)
    print(rand_image)

    subreddit = REDDIT_URLS[rand_subreddit]
    image = reddit_image(index=rand_image, json_link=subreddit)
    image.save('the_image.png', format='PNG')
    image_r = discord.File(open('the_image.png', 'rb'))
    channel = ctx.channel
    await channel.send(file=image_r)

@bot.command(name='trump',
             brief='Get random quote from Donald Trump',
             alias=['Trump', 'TRUMP', 'CHINA', 'china', 'China', 'Chyna', 'chyna', 'CHYNA'])
async def trump(ctx):
    quote = get_quote()
    channel = ctx.channel
    await channel.send(f"No one: \nAbsolutely no one: \nTronald Dump: {quote}")

""" Custom methods to handle all external stuff """

def get_quote():
    """
        Retrieve a random Donald Trump's quote
    """
    headers = {"accept": "application/json"}
    response = requests.get(TRUMP_QUOTE_URL, headers = headers)
    data = response.json()
    print(data)
    quote = data['value']
    return quote

def reddit_image(index=0, json_link=REDDIT_URLS[0]):
    """
        Retrieve a reddit image on index-th position
        Use cursed images subreddit as default
    """
    # get the list json of the subreddit
    headers = {'User-agent': 'Seqrous BOT'}

    response = requests.get(json_link, headers = headers)
    data = response.json()
    # permalinks is for all permalinks entries on the subreddit 
    permalinks = []
    for i in range(0, len(data['data']['children'])):
        # make proper links out of permalinks
        permalinks.append(('http://reddit.com' + data['data']['children'][i]['data']['permalink']) + '.json')
    
    # get the json of the selected post
    response_post = requests.get(permalinks[index], headers = headers)
    data_post = response_post.json()
    
    # get the url of the image and clean it up
    image_url = data_post[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url'].replace('amp;', '')
    response_image = requests.get(image_url, headers = headers)
    # get the image itself
    img = Image.open(BytesIO(response_image.content))
    return img

bot.run(TOKEN)
