import discord
import os
import time
import asyncio
import random
from threading import Thread


class BotInformation:
    def __init__(self, id_server):

        self.server_id = id_server
        self.music_pl = None
        self.bot_voice = None


def get_list_of_local_songs():

    default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"  # Path to project folder

    folder_with_songs = default_folder + "/songs"  # Path to songs folder
    folder_with_songs = os.listdir(folder_with_songs)  # List of songs names

    return folder_with_songs


def main():

    def exit_from_channel():

        while True:
            for i in servers_list:

                async def disconnecting_from_channel():
                    print("here!")
                    i.bot_voice.channel = None
                    i.music_pl = None
                    await i.bot_voice.disconnect()

                if i.bot_voice is None:
                    continue

                if len(i.bot_voice.channel.members) == 1:
                    print("wow")
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(disconnecting_from_channel())
                    print("Gggg")

            time.sleep(6)

    token = ""      # Discord bot token

    client = discord.Client()       # Discord Client

    servers_list = []

    # exit_from_channel_thread = Thread(target=exit_from_channel)
    # exit_from_channel_thread.start()

    @client.event
    async def on_ready():

        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return

        def get_information_about_server(server_id):

            for i_temp in servers_list:

                if i_temp.server_id == server_id:

                    return i_temp

            servers_list.append(BotInformation(server_id))
            print("Registering a new server: ", server_id)
            return servers_list[-1]

        bot_information = get_information_about_server(message.guild.id)

        if message.content == "!gc!creator":

            creator_text_message = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await message.channel.send(creator_text_message)

        if message.content == "!gc!help":

            help_text = open("./static_texts/help_inst.txt", "r")

            await message.channel.send(help_text.read())

        if message.content == "!gc!list":

            list_of_local_songs = get_list_of_local_songs()

            local_songs_message = ""

            con_of_local_songs = 1
            for i in list_of_local_songs:

                local_songs_message += str(con_of_local_songs) + ") " + i[:-4] + "\n"
                con_of_local_songs += 1

            await message.channel.send(local_songs_message)

        if message.content.startswith("!gc!play"):

            if message.author.voice is None:
                return

            parsed_message = message.content.split(" ")

            if not parsed_message[1].isdigit() or (len(parsed_message) != 2 or int(parsed_message[1]) <= 0):

                await message.channel.send("Incorrect input")
                return

            list_of_local_songs = get_list_of_local_songs()

            if int(parsed_message[1]) > len(list_of_local_songs):

                await message.channel.send("Incorrect input")
                return

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"

            road_to_correct_song = default_folder + "/songs/" + list_of_local_songs[int(parsed_message[1]) - 1]

            if bot_information.bot_voice is None:

                bot_information.bot_voice = await message.author.voice.channel.connect()

            else:

                if bot_information.bot_voice.channel.id != message.author.voice.channel.id:

                    await bot_information.bot_voice.disconnect()

                    bot_information.bot_voice = await message.author.voice.channel.connect()

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():

                    bot_information.bot_voice.stop()

            bot_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(road_to_correct_song))
            bot_information.bot_voice.play(bot_information.music_pl)

        if message.content == "!gc!stop":

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():

                    bot_information.bot_voice.stop()

        if message.content == "!gc!leave":

            await bot_information.bot_voice.disconnect()
            bot_information.bot_voice = None
            bot_information.music_pl = None

        if message.content == "!gc!random":

            if message.author.voice is None:
                return

            list_of_local_songs = get_list_of_local_songs()

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"

            len_of_local_songs = len(list_of_local_songs) - 1

            road_to_correct_song = default_folder + "/songs/" + list_of_local_songs[random.randint(0, len_of_local_songs)]

            if bot_information.bot_voice is None:

                bot_information.bot_voice = await message.author.voice.channel.connect()

            else:

                if bot_information.bot_voice.channel.id != message.author.voice.channel.id:

                    await bot_information.bot_voice.disconnect()

                    bot_information.bot_voice = await message.author.voice.channel.connect()

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():

                    bot_information.bot_voice.stop()

            bot_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(road_to_correct_song))
            bot_information.bot_voice.play(bot_information.music_pl)

        if message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ" or message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ?":

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"

            additional_folder = default_folder + "/Pictures/mort.jpg"

            await message.channel.send("Миша, что он на меня орет, да и у меня глобал на основе, а не у него")
            await message.channel.send(file=discord.File(additional_folder))

    client.run(token)


if __name__ == "__main__":
    main()
