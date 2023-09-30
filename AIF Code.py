#Импорты/Imports
import discord
from discord.ext import commands
import os
import random
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import ffmpeg
def get_class(path):
    global confidence_score
    global aboba
    np.set_printoptions(suppress=True)
    model = load_model("keras_model.h5", compile=False)
    class_names = open("labels.txt", "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    aboba = class_name[2:-1]
    return class_name[2:-1]
#Настройки бота/Bot settings
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#Команды бота и токен/Bot commands and token
@bot.command()
async def hello(ctx):
    await ctx.send(f'Heello bro! Im {bot.user}!')
@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f'images/{file_name}')
            await ctx.send(f'In image(not 100%): {get_class(f"images/{file_name}")}')
            await ctx.send(f'Image url: {file_url}!')
            os.remove(f'images/{file_name}')
            if confidence_score <= 0.50:
                await ctx.send('I dont know what in image!')

            voice_channel = ctx.author.voice
            if voice_channel:
                voice_channel = voice_channel.channel
                if aboba == 'Happy':
                    music_folder = 'happy'
                elif aboba == 'Sad':
                    music_folder = 'sad'
                else:
                    return

                music_files = os.listdir(music_folder)
                random_music = random.choice(music_files)
                print(music_files)
                print(random_music)
                print(music_folder)

                voice_client = await voice_channel.connect()
                voice_client.play(discord.FFmpegPCMAudio(f'{music_folder}/{random_music}'))
            else:
                await ctx.send('Вы не в голосовом канале')



    else:
        await ctx.send('Image not find:(')
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
bot.run("")