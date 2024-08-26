from discord.ext import commands
import discord
from discord import app_commands
import requests
from bs4 import BeautifulSoup
import random
import smtplib
import time
from rohopics import links
from activities_list import activities
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
google_app_password = os.getenv('APP_PW')
gmail_user = os.getenv('GMAIL_USER')


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
    except Exception as e:
        print(e)
        exit()
        
@bot.command()
async def be_annoying(ctx):
    await ctx.send('hello')



@bot.tree.command(name='meme', description='this command scrapes memes')
async def meme(interaction: discord.Interaction):
    link = f'https://imgflip.com/tag/memes?page={random.randint(1, 200)}'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    meme_list = [i.get('src') for i in soup.find_all('img')][2::]
    output = random.choice(meme_list)
    await interaction.response.send_message(f'https:/{output}')


@bot.tree.command(name='spam', description=':)')
async def spam(interaction: discord.Interaction):
    await interaction.response.send_message(f'hey {interaction.user.mention}!', ephemeral=True)

    for _ in range(1000):
        await interaction.followup.send(f'hey {interaction.user.mention}!', ephemeral=True)
        time.sleep(1)

@bot.tree.command(name='activity', description='bored? get an activity')
async def activity(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(activities))


@bot.tree.command(name='dogpic', description='send a dog picture!')
async def dogpic(interaction: discord.Interaction):
    link = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(link).json()['message']
    await interaction.response.send_message(f'like it?: {response}')


@bot.tree.command(name='insult', description='get insulted!')
async def insult(interaction: discord.Interaction):
    link = 'https://insult.mattbas.org/api/insult'
    output = requests.get(link).text.replace('\n', '')
    await interaction.response.send_message(f'hey {interaction.user.mention}! {output}!')

@bot.tree.command(name='rohopicture', description='get a picture of rohit!')
async def insult(interaction: discord.Interaction):
    soup = BeautifulSoup(requests.get(random.choice(links)).text, features='html.parser')
    string = [i.get('href') for i in soup.find_all('a')][::-1][0].lstrip('.')
    output = f'https://photos.google.com{string}'
    new_soup = BeautifulSoup(requests.get(output).text, features='html.parser')

    await interaction.response.send_message(new_soup.find('img').get('src'))



@bot.tree.command(name='advice', description='get life advice!')
async def advice(interaction: discord.Interaction):
    link = 'https://api.adviceslip.com/advice'
    await interaction.response.send_message(requests.get(link).json()['slip']['advice'])


@bot.tree.command(name='monkey', description='get monkey pic')
async def monkey(interaction: discord.Interaction):
    link = 'https://tinyurl.com/33fsxdvf'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    meme_list = [i.get('src') for i in soup.find_all('img')]
    print(meme_list)
    output = random.choice(meme_list)
    await interaction.response.send_message(output)


@bot.tree.command(name='rickroll', description='get rickroll gif')
async def rickroll(interaction: discord.Interaction):
    await interaction.response.send_message('https://media.tenor.com/x8v1oNUOmg4AAAAM/rickroll-roll.gif')


@bot.tree.command(name='say', description='filler command')
@app_commands.describe(thing='thing')
async def say(interaction: discord.Interaction, thing: str):
    await interaction.response.send_message(thing, ephemeral=True)


@bot.tree.command(name='email_me', description='Send bot suggestions!')
@app_commands.describe(msg='msg')
async def send_email(interaction: discord.Interaction, msg: str):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=gmail_user, password=google_app_password)
        connection.sendmail(from_addr=gmail_user, to_addrs=gmail_user, msg=msg)
    await interaction.response.send_message('message sent successfully')


bot.run(token=token)
