import os
import math
import random
from tinytag import TinyTag


def delete_server_info():

    if os.path.isfile('./static_texts/server_info.txt'):

        os.remove('./static_texts/server_info.txt')


def check_message_validity(message, prefix):

    if prefix == message[:len(prefix)]:

        message = message[len(prefix):]
        return message

    elif "!gc!" == message[:4]:

        message = message[4:]
        return message

    else:
        return None


def get_list_of_local_songs():

    # Function to get all local song's names

    default_folder = "."  # Path to project folder

    folder_with_songs = default_folder + "/songs"  # Path to songs folder
    folder_with_songs = os.listdir(folder_with_songs)  # List of songs names

    folder_with_songs.sort()

    return folder_with_songs


def check_play_number_validity(parsed_message):

    if not parsed_message[1].isdigit():
        return False, "Second word must be a digit"

    if len(parsed_message) != 2:
        return False, "So mush spaces, not 2"

    if int(parsed_message[1]) <= 0:
        return False, "Are you kidding me, song number " + parsed_message[1] + "?"

    if int(parsed_message[1]) > len(get_list_of_local_songs()):
        return False, "We have less songs than you ask"

    return True, None


def get_information_about_song(path_to_song, song_number):

    song_duration = TinyTag.get(path_to_song).duration
    song_duration = math.ceil(song_duration)

    information_about_song = "Now playing " + str(song_number + 1) + ". "
    information_about_song += get_list_of_local_songs()[song_number][:-4]
    information_about_song += "\nIt have a duration "
    information_about_song += str(int(song_duration // 60)) + " min "
    information_about_song += str(song_duration % 60) + " sec"

    return information_about_song


def check_list_number_validity(parsed_message):

    if len(parsed_message) > 2:
        return False, "Try to write just one number"

    if int(parsed_message[1]) > math.ceil(len(get_list_of_local_songs()) / 5) or int(parsed_message[1]) <= 0:
        return False, "Do number smaller or bigger. We have just " + str(math.ceil(len(get_list_of_local_songs()) / 5)) + " lists"

    return True, None


def path_to_random_meme():

    full_folder = "./Pictures/memes/"

    list_of_local_memes = os.listdir(full_folder)

    meme_image_path = full_folder + list_of_local_memes[random.randint(0, len(list_of_local_memes) - 1)]

    return meme_image_path


def road_to_game_theme_song(member):

    road_to_correct_song = None

    for activities_con in member.activities:

        with open("./static_texts/game_information.txt", "r") as file_act:

            for line in file_act:

                if activities_con.name == line.split(" &&& ")[0]:
                    road_to_correct_song = line.split(" &&& ")[1][:-1]

        if road_to_correct_song is not None:
            break

    return road_to_correct_song
