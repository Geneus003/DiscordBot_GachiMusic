import discord
import os


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

        if message.author == client.user:   # Just need it
            return

        if message.content == "!gc!creator":

            # Code to show info about author

            creator_message_text = "My creator is Geneus003 \n Email: geneus003@gmail.com"

            await client.send_message(message.channel, creator_message_text)

        if message.content == "!gc!help":

            # Code to show all available bot functions

            await client.send_message(message.channel, "Some instructions")
            await client.send_message(message.channel, "Some more instuctions")

        if message.content == "!gc!list":

            # Code to send ID and names of songs in chat

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"     # Path to project folder

            folder_with_songs = default_folder + "/songs"   # Path to songs folder
            folder_with_songs = os.listdir(folder_with_songs)   # List of songs names

            list_of_music_list = ""  # Message with information about names of available songs, and there ID
            counter_for_music_list = 1      # ID for music list

            for i in folder_with_songs:    # Adding all names and information about available songs from list to message
                list_of_music_list += str(counter_for_music_list) + ") " + str(i[:-4]) + "\n"
                counter_for_music_list += 1

            await client.send_message(message.channel, list_of_music_list)

        if message.content == "!gc!play":

            # Code for playing music

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic/songs"   # Path to all music
            music_folder = default_folder + "/Fairy_Tail_main_theme.mp3"    # Path to correct music

            print("Starting playing music")
            # music_thread = Thread(target=play_music(music_folder, client))
            # music_thread.start()

            channel = client.get_channel("425248908172853254")      # Id of voice channel

            bot_voice = await client.join_voice_channel(channel)       # Joining to voice channel

            global music_player

            music_player = bot_voice.create_ffmpeg_player(music_folder)     # Creating player

            music_player.start()    # Playing music in voice channel

        if message.content == "!gc!stop":

            # Code for stopping music

            if music_player is None:    # If music_player had never used
                return

            if music_player.is_playing():   # Checking for activity if true -> stopping
                music_player.stop()

    client.run(token)


if __name__ == "__main__":
    main()
