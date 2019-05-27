import discord
import asyncio
import random
import math
import os

import additional_functions
import pictures_collapse


class ServerInformation:
    # Class to store unique server's information

    def __init__(self, server_id):

        self.id = server_id  # Server id witch autorotate a server
        self.music_pl = None  # Music player
        self.bot_voice = None  # Thread with bot voice
        self.playing_games = True  # To play gachi song if user starting playing game
        self.prefix = "!gc!"  # Server prefix


def main():

    token = ""   # Bot's token

    # status_game = discord.Game('Try !gc!help | V 1.2')  # Variable to set status
    client = discord.Client()  # Discord Client

    list_of_servers = []

    additional_functions.delete_server_info()

    async def timing_tasks_of_discord():

        # Function for permanent tasks

        await client.wait_until_ready()

        while not client.is_closed():

            status_game = discord.Game(name="Try !gc!help | V 1.2")
            await client.change_presence(activity=status_game)

            for i_temp in list_of_servers:

                if i_temp.bot_voice is None:
                    continue

                counter_of_bots_in_voice_channel = 0

                for j_temp in i_temp.bot_voice.channel.members:

                    if j_temp.bot:

                        counter_of_bots_in_voice_channel += 1

                if len(i_temp.bot_voice.channel.members) == counter_of_bots_in_voice_channel:
                    await i_temp.bot_voice.disconnect()
                    i_temp.bot_voice = None
                    i_temp.music_pl = None

            await asyncio.sleep(120)

    def get_information_about_server(server_id):

        # Function which add new server into server list or return existed class

        for i_temp in list_of_servers:

            if i_temp.id == server_id:
                return i_temp

        list_of_servers.append(ServerInformation(server_id))
        f = open("./bot_statistics/server_info.txt", "a")
        print("Registering a new server: ", server_id, file=f)
        f.close()
        return list_of_servers[-1]

    client.loop.create_task(timing_tasks_of_discord())  # Start of permanent task

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
    async def on_message(message):

        if message.author == client.user:
            # Bot send a message -> return
            return

        if message.guild is None:
            return

        message.content = message.content.strip()
        message.content = message.content.lower()

        server_information = get_information_about_server(message.guild.id)  # Getting bot information

        if message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ" or message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ?":
            # Function to send a mem

            full_folder = "./Pictures/another/mort.jpg"

            await message.channel.send("Миша, что он на меня орет, да и у меня глобал на основе, а не у него")
            await message.channel.send(file=discord.File(full_folder))

            return

        message.content = additional_functions.check_message_validity(message.content, server_information.prefix)

        if message.content is None:
            return

        # Core functions

        if message.content.startswith("list"):

            parsed_message = message.content.split(" ")

            list_of_local_songs = additional_functions.get_list_of_local_songs()

            if len(parsed_message) == 1:

                parsed_message.append("1")

            if parsed_message[1].isdigit():

                list_number_validity = additional_functions.check_list_number_validity(parsed_message)

                if not list_number_validity[0]:

                    await message.channel.send(list_number_validity[1])
                    return

                start_point_to_show_list = 5 * (int(parsed_message[1]) - 1)
                songs_list_message = ""

                if start_point_to_show_list + 5 > len(list_of_local_songs):
                    start_point_to_show_list -= start_point_to_show_list + 5 - len(list_of_local_songs)

                for song_con in range(start_point_to_show_list, start_point_to_show_list + 5):

                    songs_list_message += str(song_con + 1) + ") " + list_of_local_songs[song_con][:-4] + "\n"

                songs_list_message += "List number " + parsed_message[1]
                songs_list_message += " from " + str(math.ceil(len(list_of_local_songs) / 5))

                await message.channel.send(songs_list_message)
                return

            else:

                local_songs_message = ""
                needful_song_name = ""

                for i in range(1, len(parsed_message)):
                    needful_song_name += parsed_message[i].upper()

                for i in range(len(list_of_local_songs)):

                    if needful_song_name in list_of_local_songs[i][:-4].upper():
                        local_songs_message += str(i + 1) + ") " + list_of_local_songs[i][:-4] + "\n"

                if local_songs_message == "":
                    local_songs_message = "We can't find this music, try again"

                await message.channel.send(local_songs_message)
                return

        if message.content.startswith("play"):

            # Function which play audio from local file

            if message.author.voice is None:
                await message.channel.send("Try to connect to the voice channel")
                return

            parsed_message = message.content.split(" ")

            validity_play_number = additional_functions.check_play_number_validity(parsed_message)

            if not validity_play_number[0]:

                await message.channel.send(validity_play_number[1])
                return

            full_folder = "./songs/" + additional_functions.get_list_of_local_songs()[int(parsed_message[1]) - 1]

            if server_information.bot_voice is None:

                server_information.bot_voice = await message.author.voice.channel.connect()

            else:

                if server_information.bot_voice.channel.id != message.author.voice.channel.id:

                    await server_information.bot_voice.disconnect()
                    server_information.bot_voice = await message.author.voice.channel.connect()

                elif server_information.bot_voice.is_playing():

                    server_information.bot_voice.stop()

            server_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(full_folder))
            server_information.bot_voice.play(server_information.music_pl)

            await message.channel.send(additional_functions.get_information_about_song(full_folder, int(parsed_message[1]) - 1))

            return

        if message.content == "random":

            # Function to play random music

            if message.author.voice is None:
                await message.channel.send("Try to connect to the voice channel")
                return

            random_song_number = random.randint(0, len(additional_functions.get_list_of_local_songs()) - 1)

            full_folder = "./songs/" + additional_functions.get_list_of_local_songs()[random_song_number]

            if server_information.bot_voice is None:

                server_information.bot_voice = await message.author.voice.channel.connect()

            else:

                if server_information.bot_voice.channel.id != message.author.voice.channel.id:

                    await server_information.bot_voice.disconnect()
                    server_information.bot_voice = await message.author.voice.channel.connect()

                elif server_information.bot_voice.is_playing():

                    server_information.bot_voice.stop()

            server_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(full_folder))
            server_information.bot_voice.play(server_information.music_pl)

            await message.channel.send(additional_functions.get_information_about_song(full_folder, random_song_number))

            return

        if message.content == "stop":

            # Function to stop music

            if server_information.bot_voice is not None:

                if server_information.bot_voice.is_playing():

                    server_information.bot_voice.stop()

            return

        if message.content == "leave":

            # Functions to make bot leave

            if server_information.bot_voice is not None:

                await server_information.bot_voice.disconnect()
                server_information.bot_voice = None
                server_information.music_pl = None

            return

        if message.content == "playing_games":

            # Function to activate special function(@client.member_update)

            if not server_information.playing_games:
                server_information.playing_games = True
                playing_games_text = "Now the bot will play the songs if the person will start playing in correct game"
                await message.channel.send(playing_games_text)

            else:
                server_information.playing_games = False
                playing_games_text = "Now the bot will not play the songs if the person will start playing in correct game"
                await message.channel.send(playing_games_text)

        if message.content.startswith("help"):

            if len(message.content.split(" ")) != 2:

                # Function which send commands info in dm

                help_text_dm, help_text_server = additional_functions.text_of_basic_information(server_information.prefix)

                await message.channel.send(help_text_server)

                try:
                    await message.author.send(help_text_dm)

                except discord.Forbidden:
                    return

                return

            else:

                parsed_message = message.content.split(" ")

                full_command_description = additional_functions.get_command_description(parsed_message[1], server_information.prefix)

                if full_command_description is None:

                    await message.channel.send("This command doesn't find, please try again")
                    return

                await message.channel.send(full_command_description)

        # Information functions

        if message.content == "creator":

            # Function which send creator information

            creator_text_message = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await message.channel.send(creator_text_message)

            return

        if message.content == "github":

            github_info_message = "If you want to help me with a code, come here: https://github.com/Geneus003/DiscordBot_GachiMusic"

            await message.channel.send(github_info_message)

        if message.content.startswith("update"):

            information_about_update_text = additional_functions.get_update_text()

            await message.channel.send(information_about_update_text)

        # Server's configuration functions

        if message.content.startswith("prefix"):

            # Function to set up server's prefix

            parsed_message = message.content.split(" ")

            if len(parsed_message) != 2 or parsed_message[1] == " ":

                await message.channel.send("Incorrect prefix input")
                return

            server_information.prefix = str(parsed_message[1])

            await message.channel.send("Prefix '" + str(parsed_message[1]) + "' have been installed")

        # Fun functions

        if message.content == "memes":

            # Function to send meme

            await message.channel.send(file=discord.File(additional_functions.path_to_random_meme()))

            return

        if message.content == "meme":

            if os.path.isfile('./Pictures/meme_in_image/in.jpg'):
                os.remove('./Pictures/meme_in_image/in.jpg')

            await message.author.avatar_url_as(static_format="jpg", size=128).save("./Pictures/meme_in_image/in.jpg")

            if os.path.isfile('./Pictures/meme_in_image/in.jpg'):

                pictures_collapse.collapse_image("./Pictures/another/ass_command.jpg", "./Pictures/meme_in_image/in.jpg", (130, 115))

                await message.channel.send(file=discord.File("./Pictures/meme_out_image/out.jpg"))

            else:

                await message.channel.send("Sorry we got an error, please report us about it:(")

    @client.event
    async def on_member_update(member_before, member_after):

        # This function start playing game related gachi song

        server_information = get_information_about_server(member_after.guild.id)

        if not server_information.playing_games:
            return

        if member_after.voice is None:
            return None

        road_to_correct_song = additional_functions.road_to_game_theme_song(member_after)

        if road_to_correct_song is None:
            return

        if server_information.bot_voice is not None:

            if server_information.bot_voice.is_playing():

                return

            if server_information.bot_voice.channel.id != member_after.voice.channel.id:
                await server_information.bot_voice.disconnect()
                server_information.bot_voice = await member_after.voice.channel.connect()

        else:

            server_information.bot_voice = await member_after.voice.channel.connect()

        server_information.music_pl = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(road_to_correct_song))
        server_information.bot_voice.play(server_information.music_pl)

    client.run(token)


if __name__ == "__main__":
    main()
