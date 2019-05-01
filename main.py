import discord
import os
import math
import asyncio
import random

from tinytag import TinyTag


class BotInformation:
    # Class contains information about bot parameters
    def __init__(self, id_server):

        self.server_id = id_server      # Server id witch autorotate a server
        self.music_pl = None        # Music player
        self.bot_voice = None       # Thread with bot voice
        self.playing_games = True   # To play gachi song if user starting playing game
        self.prefix = "!gc!"  


def get_list_of_local_songs():

    # Function to get all local song's names

    default_folder = "."  # Path to project folder

    folder_with_songs = default_folder + "/songs"  # Path to songs folder
    folder_with_songs = os.listdir(folder_with_songs)  # List of songs names

    folder_with_songs.sort()

    return folder_with_songs


def delete_server_info_file():

    if os.path.isfile('./static_texts/server_info.txt'):

        os.remove('./static_texts/server_info.txt')


def main():

    token = ""      # Discord bot token

    status_game = discord.Game("Try !gc!help | V 1.1.1")     # Variable to set status
    client = discord.Client(activity=status_game)       # Discord Client

    servers_list = []       # List with BotInformation classes

    delete_server_info_file()   # Deleting file with id of servers

    async def timing_tasks_of_discord():
        await client.wait_until_ready()

        while not client.is_closed():

            for i_temp in servers_list:

                if i_temp.bot_voice is None:

                    continue

                if len(i_temp.bot_voice.channel.members) == 1:

                    await i_temp.bot_voice.disconnect()
                    i_temp.bot_voice = None
                    i_temp.music_pl = None

            await asyncio.sleep(120)

    def get_information_about_server(server_id):

        # Function which add new server into server list or return existed class

        for i_temp in servers_list:

            if i_temp.server_id == server_id:
                return i_temp

        servers_list.append(BotInformation(server_id))
        f = open("./static_texts/server_info.txt", "a")
        print("Registering a new server: ", server_id, file=f)
        return servers_list[-1]

    client.loop.create_task(timing_tasks_of_discord())

    @client.event
    async def on_ready():

        # Function witch started on bot ready
        # Printing bot information

        print(discord.__version__)
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_member_update(member_before, member_after):

        # This function start playing game related gachi song

        road_to_correct_song = None

        bot_information = get_information_about_server(member_after.guild.id)

        if not bot_information.playing_games:

            return

        for i in member_after.activities:

            if i.name == "Counter-Strike: Global Offensive":

                road_to_correct_song = "./songs/【Gachimuchi】 CS♂GO.mp3"

            elif i.name == "Overwatch":

                road_to_correct_song = "./songs/Gachi Overwatch Victory  Menu Theme ♂RIGHT VERSION♂ gachiGASM.mp3"

            elif i.name == "Grand Theft Auto V" or i.name == "Grand Theft Auto San Andreas":

                road_to_correct_song = "【Gachimuchi】Grand ♂ Theft ♂ Auto.mp3"

        if road_to_correct_song is not None:

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():

                    return

            bot_information.bot_voice = await member_after.voice.channel.connect()

            bot_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(road_to_correct_song))
            bot_information.bot_voice.play(bot_information.music_pl)

    @client.event
    async def on_message(message):

        if message.author == client.user:
            # Bot send a message -> return
            return

        bot_information = get_information_about_server(message.guild.id)    # Getting bot information

        if message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ" or message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ?":
            # Function which send mem

            default_folder = "."

            additional_folder = default_folder + "/Pictures/another/mort.jpg"

            await message.channel.send("Миша, что он на меня орет, да и у меня глобал на основе, а не у него")
            await message.channel.send(file=discord.File(additional_folder))

        if message.content == "!gc!help":

            # Function which send commands info

            help_text = open("./static_texts/help_inst.txt", "r")

            await message.channel.send("All commands and their descriptions have been sent, look in your DM!")

            try:
                await message.author.send(help_text.read())

            except discord.Forbidden:
                return

            return

        if bot_information.prefix == message.content[:len(bot_information.prefix)]:

            message.content = message.content[len(bot_information.prefix):]

        else:
            return

        if message.content == "creator":

            # Function which send creator information

            creator_text_message = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await message.channel.send(creator_text_message)

        if message.content.startswith("prefix"):

            parsed_message = message.content.split(" ")

            if len(parsed_message) != 2 or parsed_message[1] == " ":

                await message.channel.send("Incorrect input")
                return

            bot_information.prefix = str(parsed_message[1])

            await message.channel.send("Prefix '" + str(parsed_message[1]) + "' have been installed")

        if message.content == "help":

            # Function which send commands info

            help_text = open("./static_texts/help_inst.txt", "r")

            await message.channel.send("All commands and their descriptions have been sent, look in your DM!")

            try:
                await message.author.send(help_text.read())

            except discord.Forbidden:
                return

        if message.content.startswith("list"):

            # Function which send list info

            parsed_message = message.content.split(" ")

            if len(parsed_message) == 1:

                parsed_message.append("1")

            list_of_local_songs = get_list_of_local_songs()

            if parsed_message[1].isdigit():

                if len(parsed_message) > 2:
                    await message.channel.send("Incorrect input")
                    return

                if len(parsed_message) == 1:
                    parsed_message.append("1")
                    start_point_to_show_list = 0

                else:
                    if not parsed_message[1].isdigit():
                        await message.channel.send("Incorrect input")
                        return

                    if int(parsed_message[1]) > math.ceil(len(list_of_local_songs) / 5) or int(parsed_message[1]) <= 0:
                        await message.channel.send("Not enough songs, do number smaller or bigger")
                        return

                    start_point_to_show_list = 5 * (int(parsed_message[1]) - 1)

                local_songs_message = ""

                if start_point_to_show_list + 5 > len(list_of_local_songs):
                    start_point_to_show_list -= start_point_to_show_list + 5 - len(list_of_local_songs)

                for i in range(start_point_to_show_list, start_point_to_show_list + 5):
                    local_songs_message += str(i + 1) + ") " + list_of_local_songs[i][:-4] + "\n"

                local_songs_message += "List number " + parsed_message[1]
                local_songs_message += " from " + str(math.ceil(len(list_of_local_songs) / 5))

                await message.channel.send(local_songs_message)

            else:

                local_songs_message = ""
                needful_song_name = ""

                for i in range(1, len(parsed_message)):

                    needful_song_name += parsed_message[i].upper()

                for i in range(len(list_of_local_songs)):

                    if needful_song_name in list_of_local_songs[i].upper():

                        local_songs_message += str(i+1) + ") " + list_of_local_songs[i] + "\n"

                if local_songs_message == "":

                    local_songs_message = "We can't find this music, try again"

                await message.channel.send(local_songs_message)

        if message.content == "game_activity":

            if not bot_information.playing_games:
                bot_information.playing_games = True
                playing_games_text = "Now the bot will play the songs if the person will start playing in correct game"
                await message.channel.send(playing_games_text)

            else:
                bot_information.playing_games = False
                playing_games_text = "Now the bot will not play the songs if the person will start playing in correct game"
                await message.channel.send(playing_games_text)

        if message.content.startswith("play"):

            # Function which play audio from local file

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

            default_folder = "."

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

            song_duration = TinyTag.get(road_to_correct_song).duration
            song_duration = math.ceil(song_duration)

            information_about_song = "Now playing " + parsed_message[1] + ". "
            information_about_song += list_of_local_songs[int(parsed_message[1]) - 1][:-4]
            information_about_song += "\nIt have a duration "
            information_about_song += str(int(song_duration // 60)) + " min "
            information_about_song += str(song_duration % 60) + " sec"

            await message.channel.send(information_about_song)

        if message.content == "stop":

            # Function which stop the music

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():

                    bot_information.bot_voice.stop()

        if message.content == "leave":

            # Function which makes bot leave

            await bot_information.bot_voice.disconnect()
            bot_information.bot_voice = None
            bot_information.music_pl = None

        if message.content == "random":

            # Function which play random of local songs

            if message.author.voice is None:
                return

            list_of_local_songs = get_list_of_local_songs()

            default_folder = "."

            len_of_local_songs = len(list_of_local_songs) - 1

            random_song_number = random.randint(0, len_of_local_songs)

            road_to_correct_song = default_folder + "/songs/" + list_of_local_songs[random_song_number]

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

            song_duration = TinyTag.get(road_to_correct_song).duration
            song_duration = math.ceil(song_duration)

            information_about_song = "Now playing " + str(random_song_number + 1) + ". "
            information_about_song += list_of_local_songs[random_song_number][:-4]
            information_about_song += "\nIt have a duration "
            information_about_song += str(int(song_duration // 60)) + " min "
            information_about_song += str(song_duration % 60) + " sec"

            await message.channel.send(information_about_song)

        if message.content.startswith("yt"):

            if bot_information.bot_voice is None:

                bot_information.bot_voice = await message.author.voice.channel.connect()

            else:

                if bot_information.bot_voice.channel.id != message.author.voice.channel.id:

                    await bot_information.bot_voice.disconnect()

                    bot_information.bot_voice = await message.author.voice.channel.connect()

            if bot_information.bot_voice is not None:

                if bot_information.bot_voice.is_playing():
                    bot_information.bot_voice.stop()

            print(discord.opus)

        if message.content == "memes":

            default_folder = "."

            additional_folder = default_folder + "/Pictures/memes/"

            list_of_local_memes = os.listdir(additional_folder)

            meme_image = additional_folder + list_of_local_memes[random.randint(0, len(list_of_local_memes) - 1)]

            await message.channel.send(file=discord.File(meme_image))

    client.run(token)


if __name__ == "__main__":
    main()
