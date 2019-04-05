import discord
import os


def get_list_of_local_music():

    default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"  # Path to project folder

    folder_with_songs = default_folder + "/songs"  # Path to songs folder
    folder_with_songs = os.listdir(folder_with_songs)  # List of songs names

    return folder_with_songs


def main():

    token = ""   # Discord bot token

    client = discord.Client()   # Discord client

    music_player = None     # Initialization of music player, because can get an error "Used before assignment"

    @client.event
    async def on_ready():   # To show starting of the work and some information

        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):

        if message.author == client.user:
            # Just need it
            return

        if message.content == "!gc!creator":

            # Code to show info about author

            creator_message_text = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await client.send_message(message.channel, creator_message_text)

        if message.content == "!gc!help":

            # Code to show all available bot functions

            await client.send_message(message.channel, "Some instructions")
            await client.send_message(message.channel, "Some more instructions")

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

                channel = client.get_channel("425248908172853254")      # Getting channel id

                bot_voice = await client.join_voice_channel(channel)  # Joining to voice channel

                global music_player     # This code need to stop the music

                music_player = bot_voice.create_ffmpeg_player(music_folder)  # Creating player

                music_player.start()  # Playing music in voice channel

        if message.content == "!gc!stop":

            # Code for stopping music

            if music_player is None:    # If music_player had never used
                return

            if music_player.is_playing():   # Checking for activity if true -> stopping
                music_player.stop()

    client.run(token)


if __name__ == "__main__":
    main()
