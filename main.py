import discord
import os
from _datetime import datetime

# Version 1.0


class BotInformation:

    def __init__(self, server_id_g):
        self.server_id = server_id_g
        self.music_pl = None
        self.bot_voice = None
        self.bot_last_activity = datetime.now()


def get_list_of_local_music():

    default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"  # Path to project folder

    folder_with_songs = default_folder + "/songs"  # Path to songs folder
    folder_with_songs = os.listdir(folder_with_songs)  # List of songs names

    return folder_with_songs


def main():

    token = ""   # Discord bot token

    client = discord.Client()   # Discord clients

    server_list = []

    @client.event
    async def on_ready():   # To show starting of the work and some information

        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

        game_name = "To show the commands write '!gc!help', Version=1.0"
        await client.change_presence(game=discord.Game(name=game_name))

    @client.event
    async def on_message(message):

        server = message.server

        def getting_information_about_server(discord_server_id):

            for i_temp in server_list:

                if i_temp.server_id == discord_server_id:

                    # print("Server already registered", discord_server_id)

                    return i_temp

            server_list.append(BotInformation(discord_server_id))

            print("Registrations the new server", discord_server_id)

            return server_list[-1]

        bot_information = getting_information_about_server(server.id)

        if message.author == client.user:
            # Just need it
            return

        if message.content == "!gc!creator":

            # Code to show info about author

            creator_message_text = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await client.send_message(message.channel, creator_message_text)

        if message.content == "!gc!help":

            # Code to show all available bot functions

            help_text = open("./static_texts/help_inst.txt", "r")
            await client.send_message(message.channel, help_text.read())

        if message.content == "!gc!list":

            # Code to send ID and names of songs in chat

            folder_with_songs = get_list_of_local_music()

            list_of_music_list = ""  # Message with information about names of available songs, and there ID
            counter_for_music_list = 1      # ID for music list

            for i in folder_with_songs:    # Adding all names and information about available songs from list to message
                list_of_music_list += str(counter_for_music_list) + ") " + str(i[:-4]) + "\n"
                counter_for_music_list += 1

            await client.send_message(message.channel, list_of_music_list)

        if message.content.startswith("!gc!play"):

            # Code to play music in channel

            bot_information.bot_last_activity = datetime.now()

            request_to_play_message = message.content.split(" ")    # Parsing message

            # Checking for validity
            if len(request_to_play_message) != 2 or (not request_to_play_message[1].isdigit()):

                await client.send_message(message.channel, "Incorrect input:(")
                return

            needful_song_number = int(request_to_play_message[1])   # The number of needful song

            # The number mustn't be zero, here is code which checking that needful_song_number isn't zero
            if needful_song_number == 0:
                await client.send_message(message.channel, "Incorrect input:(")
                return

            folder_with_songs = get_list_of_local_music()   # Getting name of local songs

            if len(folder_with_songs) >= needful_song_number:   # If number more than songs we have

                default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic/songs"  # Path to music
                music_folder = default_folder + "/" + folder_with_songs[needful_song_number - 1]    # Path to correct music

                if message.author.voice.voice_channel is None:
                    return

                channel = client.get_channel(message.author.voice.voice_channel.id)     # Getting channel id

                if not client.is_voice_connected(server):

                    bot_information.bot_voice = await client.join_voice_channel(channel)  # Joining to voice channel

                else:

                    if bot_information.bot_voice.channel.id == channel:

                        if bot_information.music_player is None:  # If music_player had never used
                            return

                        if bot_information.music_player.is_playing():  # Checking for activity if true -> stopping
                            bot_information.music_player.stop()

                    else:

                        if bot_information.music_player is None:  # If music_player had never used
                            return

                        if bot_information.music_player.is_playing():  # Checking for activity if true -> stopping
                            bot_information.music_player.stop()

                        await bot_information.bot_voice.disconnect()

                        bot_information.bot_voice = await client.join_voice_channel(channel)

                bot_information.music_player = bot_information.bot_voice.create_ffmpeg_player(music_folder)  # Creating player

                bot_information.music_player.start()  # Playing music in voice channel

        if message.content == "!gc!stop":

            # Code for stopping music

            bot_information.bot_last_activity = datetime.now()

            if bot_information.music_player is None:    # If music_player had never used
                return

            if bot_information.music_player.is_playing():   # Checking for activity if true -> stopping
                bot_information.music_player.stop()

        if message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ" or message.content.upper() == "ПОЧЕМУ РОТ В ВОЛОДЕ?":

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"

            await client.send_message(message.channel, "Глобал на основе")

            await client.send_file(message.channel, default_folder+"/Pictures/mort.jpg")

    client.run(token)


if __name__ == "__main__":
    main()
