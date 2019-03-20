import discord
import os
from threading import Thread


def main():

    token = ""

    client = discord.Client()

    @client.event
    async def on_ready():

        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):

        if message.author == client.user:   # Just need it
            return

        if message.content == "!gc!creator":    # Info about author

            await message.channel.send("My creator is Geneus003")
            await message.channel.send("Email: geneus003@gmail.com")
            await message.channel.send("Qiwi: +79832095427")    # Info about author# Info about author

        if message.content == "!gc!help":   # Info about commands

            await message.channel.send("Some instructions")

        if message.content == "!gc!list":   # Send ID and names of songs

            default_folder = "/home/geneus/Projects/Discord_bots/DiscordBot_GachiMusic"     # Path to project folder

            folder_with_songs = default_folder + "/songs"   # Path to songs folder
            folder_with_songs = os.listdir(folder_with_songs)   # List of songs names

            list_of_music_list = ""  # Message with information about names of available songs, and there ID
            counter_for_music_list = 1      # ID for music list

            for i in folder_with_songs:    # Adding all names and information about available songs from list to message
                list_of_music_list += str(counter_for_music_list) + ") " + str(i[:-4]) + "\n"
                counter_for_music_list += 1

            await message.channel.send(list_of_music_list)

        if message.content == "!gc!play":

            if not message.content.isdigit():

                await message.channel.send("It isn't a number")

    client.run(token)


if __name__ == "__main__":
    main()
