import discord
from discord import app_commands
import sox
from string import ascii_uppercase
import d_token
import os
import nacl

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    base_dir = os.getcwd()
    try:
        os.chdir('./voice')
    except:
        os.mkdir('./voice')

    os.chdir(base_dir)
    print(' ready ! ')

def generate_animalese(message: str):
    audio_dir = 'audio'
    l_message = []
    text_to_speech = [f'{audio_dir}/space.wav']

    for letter in message:
        if letter in ',. ':
            text_to_speech.append(f'{audio_dir}/space.wav')
            l_message.append('_')
        elif letter.upper() not in ascii_uppercase:
            pass
        else:
            text_to_speech.append(f'{audio_dir}/{letter.upper()}.wav')
            l_message.append(letter)
    text_to_speech.append(f'{audio_dir}/space.wav')
    generated_sound = f"voice/{''.join(l_message)}.wav"
    sox.Combiner().build(text_to_speech, generated_sound, 'concatenate')
    return generated_sound

@tree.command(name='animalese', description='generate animalese like animal crossing !')
@app_commands.describe(message=' the message you want spoken in animalese ! ')
async def animalese(interaction: discord.Interaction, message: str):
    spoken_animalese = generate_animalese(message)

    if interaction.user.voice is None:
        await interaction.response.send_message(file=discord.File(spoken_animalese))
    else:
        sound_file = discord.FFmpegPCMAudio(spoken_animalese)
        interaction.guild.voice_client.play(source=sound_file, after=None)
        await interaction.response.send_message(file=discord.File(spoken_animalese))

@tree.command(name='join', description='join a voice channel !')
async def join(interaction: discord.Interaction):
    channel = discord.utils.get(interaction.guild.voice_channels, name=interaction.user.voice.channel.name, bitrate=64000)
    await discord.VoiceChannel.connect(channel)
    await interaction.response.send_message('joined voice !')

@tree.command(name='leave', description='leave voice channel !')
async def leave(interaction: discord.Interaction):
    await discord.VoiceClient.disconnect(interaction.guild.voice_client)
    await interaction.response.send_message('left voice !')

token = d_token.d_token()
client.run(token)
