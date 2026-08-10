# Name: Jeff Ananias
# Course: CS 361
# Due Date: 2026-08-10
# Description: This file provides a command-line interface for a user to
#              create, manage, and display local music playlists.
#
#              Playlists are .m3u8 files and store songs of .mp3, .wav,
#              .flac, .aac, and .ogg format.

import os
import re
import time
import shutil
from datetime import datetime


PATH = os.getcwd()


def prompt() -> str:
    """
    Prompt user with instructions.
    """
    print("Commands:")
    print("create | select | add | remove | reorder | display")
    print("shuffle | duplicate | delete | batch | stale | exit")
    return input("Type a command and press ENTER: ")


def route_cmd(cmd: str, sel_playlist: str) -> None:
    """
    Route user input command to intended function with selected playlist.
    """
    excluded_from_check = ["create", "select", "delete", "stale", "exit"]
    if cmd not in excluded_from_check and sel_playlist == None:
        print("")
        print("Remember to first select a playlist. Reloading main menu...\n")
        time.sleep(3)
    else:
        match cmd:
            case "create":
                return create(sel_playlist)
            case "select":
                return select()
            case "add":
                return add(sel_playlist)
            case "remove":
                return remove(sel_playlist)
            case "reorder":
                return reorder(sel_playlist)
            case "display":
                return display(sel_playlist)
            case "shuffle":
                return shuffle(sel_playlist)
            case "duplicate":
                return duplicate(sel_playlist)
            case "delete":
                return delete(sel_playlist)
            case "batch":
                return batch_add(sel_playlist)
            case "stale":
                return find_stale_playlists(sel_playlist)
            case 'exit':
                exit()
            case _:
                print("Invalid command.")


def create(sel_playlist: str) -> None:
    os.system("clear")

    greet_create()

    playlist_name = input("What will be your playlist name? ")
    print(f"You named your playlist '{playlist_name}'.")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        with open(playlist_name + ".m3u8", "w") as f:
            f.write("")
        print("")
        with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("Creation of playlist.")
        time.sleep(2)
        with open("ascii_confirmation_generator.txt", "r") as f:
            print(f.read())
        print("Playlist created! Returning to main menu.")

        # Clean microservice text file
        with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("")

        time.sleep(3)
        return sel_playlist
    else:
        print("Playlist not created. Returning to main menu.")
        time.sleep(3)
        return sel_playlist


def select() -> str or None:
    """
    Show menu to user for selection of playlist.
    """
    os.system("clear")

    greet_select()

    # Create list of sorted .m3u8 files in current path
    files = sorted(os.listdir(PATH))
    playlists = [f[:-5] for f in files if f.endswith('.m3u8')]

    playlist_count = len(playlists)
    if playlist_count == 0:
        print("At least one playlist must exist in this directory.")
        print("Please create a playlist.")
        print("Returning to main menu.")
        time.sleep(3)
        return

    # Print enumerated playlist file names
    for i in range(playlist_count):
        print(f"({i + 1}) {playlists[i]}")
    print("")
    print("Any commands issued for this playlist will permanently overwrite")
    print("its contents. Some commands permit an undo feature, but not all.")
    print("")

    # Validate user input and return selection
    sel_playlist = validate_selection(playlists, playlist_count)
    while sel_playlist is None:
        sel_playlist = validate_selection(playlists, playlist_count)
    return sel_playlist


def validate_selection(files: list, count: int) -> str:
    """
    Validate user input for playlist selection or deletion.
    """
    # Ensure input is number within range of options
    choice = input("Enter number to select: ")
    if choice.isnumeric() is False or int(choice) < 1 or int(choice) > count:
        print("Invalid choice.")
        return
    choice = int(choice)

    print("")
    print(f"You chose {files[choice - 1]}.")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("")
        return files[choice - 1]
    else:
        print("Choice not confirmed.")


def get_local_songs() -> list:
    """
    Create list of sorted music files in current path.
    """
    files = sorted(os.listdir(PATH))
    music_exts = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
    local_songs = [f for f in files if f.endswith(music_exts)]
    return local_songs


def get_pl_songs(sel_playlist: str) -> list:
    """
    Create list of songs in the selected playlist.
    """
    pl_songs = []

    with open(sel_playlist + ".m3u8", "r") as f:
        song_paths = f.read().splitlines()
        for i in range(len(song_paths)):
            song = re.search(r'[^\/]+$', song_paths[i])
            pl_songs.append(song.group(0))

    return pl_songs


def print_song_list(menu: str, sel_playlist: str, songs: list = []) -> None:
    """
    Print enumerated music file names either from the local directory or the
    selected playlist.
    """
    match menu:
        case "local":
            with open(sel_playlist + ".m3u8", "r") as f:
                playlist_contents = f.read()
                for i in range(len(songs)):
                    # If song already in selected playlist, prepend asterisk
                    if songs[i] in playlist_contents:
                        print(f"({i + 1}) * {songs[i]}")
                    else:
                        print(f"({i + 1}) {songs[i]}")
            print("")
        case "playlist":
            pl_songs = get_pl_songs(sel_playlist)
            for i in range(len(pl_songs)):
                print(f"({i + 1}) {pl_songs[i]}")
            print("")


def add(sel_playlist: str) -> None:
    """
    Show menu to user for addition of one or more songs to selected playlist.
    """
    os.system("clear")

    greet_add()

    songs = get_local_songs()
    print_song_list("local", sel_playlist, songs)

    # Validate and confirm user input and store additions
    choice_list = None
    additions = None
    while choice_list is None:
        choice_str = input("Enter number(s) to choose song(s): ")
        choice_list = validate_choice(choice_str, songs, len(songs))
        if choice_list is not None:
            additions = confirm_choice(choice_list, songs)
    add_count = len(additions)
    
    # Write additions to selected playlist
    print("Adding song(s) to playlist...")
    with open(sel_playlist + ".m3u8", "a") as f:
        for addition in additions:
            f.write(PATH + "/" + addition + "\n")
    print("Done!")
    print("")
    time.sleep(3)
    return sel_playlist


def remove(sel_playlist: str) -> None:
    """
    Show menu to user for removal of one or more songs to selected playlist.
    """
    os.system("clear")

    greet_remove()

    print_song_list("playlist", sel_playlist)
    pl_songs = get_pl_songs(sel_playlist)
    if len(pl_songs) == 0:
        print("This playlist must contain songs before you can remove any.\n")
        time.sleep(3)
        return sel_playlist

    # Validate and confirm user input and store removals
    choice_list = None
    removals = None
    while choice_list is None:
        choice_str = input("Enter number(s) to choose song(s): ")
        choice_list = validate_choice(choice_str, pl_songs, len(pl_songs))
        if choice_list is not None:
            removals = confirm_choice(choice_list, pl_songs)
    remove_count = len(removals)
    
    # Write additions to selected playlist
    print("Removing song(s) from playlist...")
    with open(sel_playlist + ".m3u8", "w") as f:
        for pl_song in pl_songs:
            if pl_song not in removals:
                f.write(PATH + "/" + pl_song + "\n")
    print("Done!")
    print("")
    time.sleep(3)
    return sel_playlist


def validate_choice(choice_str: str, files: list, count: int) -> list:
    """
    Validate user input for choice of one or more songs.
    """
    # Ensure string input is series of comma-delimited integers
    pattern = re.compile(r'^\s*\d+\s*(?:,\s*\d+\s*)*$')
    if pattern.match(choice_str) is None:
        print("Invalid syntax.")
        return False

    # Ensure list of input integers is within range of options
    choice_list = [int(choice) for choice in choice_str.split(",")]
    for choice_item in choice_list:
        if choice_item < 1 or choice_item > count:
            print("Invalid choice(s). Only use available numbers.")
            return False

    return choice_list


def confirm_choice(choice_list: list, files: list) -> list:
    """
    Confirm user input for choice or one or more songs.
    """
    print("")
    print("You chose the following song(s):")
    for choice_item in choice_list:
        print(f"{files[choice_item - 1]}")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("")
        confirmed_choices = []
        for choice_item in choice_list:
            confirmed_choices.append(files[choice_item - 1])
        return confirmed_choices
    else:
        print("Choice not confirmed.")


def reorder(sel_playlist: str) -> None:
    """
    Swap items in the playlist to reorder them.
    """
    os.system("clear")

    greet_reorder()

    pl_songs = get_pl_songs(sel_playlist)

    if len(pl_songs) == 0:
        print("This playlist must contain songs before you can reorder them.\n")
        time.sleep(3)
        return sel_playlist

    choice_str = ""
    while True:
        print_song_list("playlist", sel_playlist)
        choice_str = input("Enter the numbers of two songs to swap: ")
        if choice_str == "done":
            break
        choice_list = validate_choice(choice_str, pl_songs, len(pl_songs))
        if len(choice_list) != 2:
            print("You must select two songs to swap. Try again.\n")
        else:
            [first_song, second_song] = confirm_choice(choice_list, pl_songs)
            pl_songs[choice_list[0] - 1] = second_song
            pl_songs[choice_list[1] - 1] = first_song
            with open(sel_playlist + ".m3u8", "w") as f:
                for pl_song in pl_songs:
                    f.write(PATH + "/" + pl_song + "\n")

    print("")
    print("Reorder complete! Returning to main menu.")
    time.sleep(3)

    return sel_playlist


def display(sel_playlist: str) -> None:
    """
    Show contents of selected playlist to user.
    """
    os.system("clear")

    greet_display(sel_playlist)

    print_song_list("playlist", sel_playlist)
    print("")

    go_back = input("Press ENTER to go back.")
    return sel_playlist


def shuffle(sel_playlist: str) -> None:
    """
    Write randomized order of songs in selected playlist.
    """
    os.system("clear")
    greet_shuffle()
    print("Pre-shuffle order:\n")

    pl_songs = get_pl_songs(sel_playlist)
    
    if len(pl_songs) == 0:
        print("This playlist must contain songs before you can reorder them.\n")
        time.sleep(3)
        return sel_playlist

    print_song_list("playlist", sel_playlist)

    preshuffle_order = None
    postshuffle_order = None

    with open(sel_playlist + ".m3u8", "r") as f:
        preshuffle_order = f.read()

    with open("list_randomizer.txt", "w") as f:
        f.write(preshuffle_order)

    time.sleep(2)

    with open("list_randomizer.txt", "r") as f:
        postshuffle_order = f.read()

    with open(sel_playlist + ".m3u8", "w") as f:
        f.write(postshuffle_order)

    print("")
    print("Post-shuffle order:")

    print_song_list("playlist", sel_playlist)

    with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("Shuffle of playlist.")
    time.sleep(2)
    with open("ascii_confirmation_generator.txt", "r") as f:
        print(f.read())

    print("Shuffle complete! Returning to main menu.")

    # Clean microservice text files
    with open("ascii_confirmation_generator.txt", "w") as f:
        f.write("")
    with open("list_randomizer.txt", "w") as f:
        f.write("")

    time.sleep(3)
    return sel_playlist


def duplicate(sel_playlist: str) -> None:
    """
    Write a new playlist file identical to the selected playlist.
    """
    os.system("clear")
    greet_duplicate(sel_playlist)

    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("Starting duplication...")
    else:
        print("Duplication not confirmed. Returning to main menu.")
        time.sleep(3)
        return sel_playlist

    pl_file = PATH + "/" + sel_playlist
    i = 1
    ext = ".m3u8"
    while os.path.exists(pl_file + " " + str(i) + ".m3u8"):
        i += 1
    shutil.copy2(pl_file + ".m3u8", pl_file + " " + str(i) + ".m3u8")

    print("Duplication complete! Returning to main menu.")
    time.sleep(3)

    return sel_playlist


def delete(sel_playlist) -> str or None:
    """
    Delete the selected playlist from the local directory.
    """
    os.system("clear")
    greet_delete()

    files = sorted(os.listdir(PATH))
    playlists = [f[:-5] for f in files if f.endswith('.m3u8')]
    playlist_count = len(playlists)

    for i in range(playlist_count):
        print(f"({i + 1}) {playlists[i]}")
    
    print("")

    pl_to_del = input("Enter number to select: ")
    while pl_to_del.isnumeric() is False or \
        int(pl_to_del) < 1 or \
        int(pl_to_del) > playlist_count:
        print("Invalid choice.")
        pl_to_del = input("Enter number to select: ")
    pl_to_del = int(pl_to_del)

    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("Starting deletion...")
    else:
        print("Deletion not confirmed. Returning to main menu.")
        time.sleep(3)
        return sel_playlist

    os.remove(PATH + "/" + playlists[pl_to_del - 1] + ".m3u8")

    print("Deletion complete! Returning to main menu.")
    time.sleep(3)

    if playlists[pl_to_del - 1] == sel_playlist:
        return None
    else:
        return sel_playlist


def batch_add(sel_playlist: str) -> None:
    """
    Write to the selected playlist all songs that match a metadata search.
    """
    os.system("clear")
    greet_batch_add()

    songs = get_local_songs()

    with open("music_metadata.txt", "w") as f:
        f.write("\n".join(songs))

    time.sleep(2)

    print("Metadata types: 'artist', 'album', 'year'")
    while True:
        acceptable_inputs = ["artist", "album", "year"]
        metadata_type = input("Choose the type you want to search: ")
        if metadata_type not in acceptable_inputs:
            print("Invalid type.")
        else:
            break

    metadata = []
    with open("music_metadata.txt", "r") as f:
        list_of_tags = f.read().splitlines()
        i = 0
        if metadata_type == "album":
            i = 1
        elif metadata_type == "year":
            i = 3
        while i < len(list_of_tags):
            if list_of_tags[i] not in metadata:
                metadata.append(list_of_tags[i])
            i += 4

    print(f"\nThese {metadata_type}s are available to add:\n")
    for i in range(len(metadata)):
        print(f"({i + 1}) {metadata[i]}")
    print("")

    while True:
        acceptable_inputs = range(len(metadata))
        metadata_idx = input(f"Choose the {metadata_type} you want to add: ")
        if (int(metadata_idx) - 1) not in acceptable_inputs:
            print(f"Invalid {metadata_type}.")
        else:
            metadata_tag = metadata[int(int(metadata_idx) - 1)]
            break

    print(f"You chose to add all songs of the {metadata_type} {metadata_tag}.")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("Adding this batch of songs...")
    else:
        print("Batch addition not confirmed. Returning to main menu.")
        time.sleep(3)
        return sel_playlist

    songs_to_add = []
    with open("music_metadata.txt", "r") as f:
        list_of_tags = f.read().splitlines()
        i = 0
        if metadata_type == "album":
            i = 1
        elif metadata_type == "year":
            i = 3
        j = 0
        while i < len(list_of_tags):
            if list_of_tags[i] == metadata_tag:
                songs_to_add.append(j)
            i += 4
            j += 1

    with open(sel_playlist + ".m3u8", "a") as f:
        for song_to_add in songs_to_add:
            f.write(PATH + "/" + songs[song_to_add] + "\n")

    with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("Batch addition to playlist.")
    time.sleep(2)
    with open("ascii_confirmation_generator.txt", "r") as f:
        print(f.read())
    
    # Clean microservice text files
    with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("")
    with open("music_metadata.txt", "w") as f:
            f.write("")

    print("Batch addition complete! Returning to main menu.")
    time.sleep(3)

    return sel_playlist


def find_stale_playlists(sel_playlist: str) -> None:
    """
    Print stale playlists that have not been updated in more than 7 days.
    """
    os.system("clear")
    greet_find_stale_playlists()

    # Create list of sorted .m3u8 files in current path
    files = sorted(os.listdir(PATH))
    playlists = [f[:-5] for f in files if f.endswith('.m3u8')]

    for playlist in playlists:
        last_mod_timestamp = os.path.getmtime(PATH + "/" + playlist + ".m3u8")
        last_mod_datetime = datetime.fromtimestamp(last_mod_timestamp)
        last_modified = last_mod_datetime.strftime("%Y-%m-%d")
        with open("date_diff.txt", "w") as f:
            f.write(last_modified)
        time.sleep(2)
        with open("date_diff.txt", "r") as f:
            response = f.read().split()
            status = response[0]
            days = int(response[1])
            if status == "OVERDUE:" and days > 7:
                print(playlist) 

    # Clean microservice text file
    with open("date_diff.txt", "w") as f:
        f.write("")

    print("")
    go_back = input("Press ENTER to go back.")
    return sel_playlist


def main() -> None:
    """
    Provide command-line interface to user.
    """
    sel_playlist = None

    while True:
        os.system("clear")
        greet_main()
        if sel_playlist == None:
            print("First select a playlist.\n")
        else:
            print(f"Your selected playlist is {sel_playlist}.\n")
        cmd = prompt()
        sel_playlist = route_cmd(cmd, sel_playlist)


# ----------------------------------------------------------------------------
#                        All greet functions are below
# ----------------------------------------------------------------------------


def greet_main() -> None:
    """
    Show informative greeting for user at the main menu.
    """
    print("")
    print("           ____ ____ ____ ____ ____ ____ ____ ____ ")
    print("          ||P |||L |||A |||Y |||L |||I |||S |||T ||")
    print("          ||__|||__|||__|||__|||__|||__|||__|||__||")
    print("          |/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|")
    print("                ____ ____ ____ ____ ____ ____ ")
    print("               ||E |||D |||I |||T |||O |||R ||")
    print("               ||__|||__|||__|||__|||__|||__||")
    print("               |/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|")
    print("")
    print("                 Welcome to Playlist Editor!")
    print("")
    print("This program creates, manages, and displays local music playlists.")
    print("Users must send commands in the local directory that contains the")
    print("playlists and songs they want to work with.")
    print("")
    print("To exit the program from a submenu, press Ctrl+C.")
    print("")


def greet_create() -> None:
    """
    Show informative greeting for user at the create menu.
    """
    print("* * *                   CREATE PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you create a playlist file.                  *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_select() -> None:
    """
    Show informative greeting for user at the select menu.
    """
    print("* * *                   SELECT PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you select a playlist to then edit to        *")
    print("* contain any songs you want in any order that you specify.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_add() -> None:
    """
    Show informative greeting for user at the add menu.
    """
    print("* * *                ADD SONG TO PLAYLIST                 * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you add one or more songs to the selected    *")
    print("* playlist. To add more than one song, enter multiple         *")
    print("* numbers separated by commas. Stars indicate that the song   *")
    print("* is already in the playlist.                                 *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_remove() -> None:
    """
    Show informative greeting for user at the remove menu.
    """
    print("* * *              REMOVE SONG FROM PLAYLIST              * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you remove one or more songs from the        *")
    print("* selected playlist. To remove more than one song, enter      *")
    print("* multiple numbers separated by commas.                       *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_reorder() -> None:
    """
    Show informative greeting for user at the reorder menu.
    """
    print("* * *                   REORDER SONGS                     * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you reorder songs in the selected playlist.  *")
    print("* Enter two number separated by a comma to swap the songs     *")
    print("* next to those numbers. Enter 'done' to go to the main menu. *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_display(sel_playlist: str) -> None:
    """
    Show informative greeting for user at the display menu.
    """
    print("* * *                   DISPLAY PLAYLIST                  * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This page displays the contents of the selected playlist.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")
    print(f"{sel_playlist} Playlist:")
    print("")


def greet_shuffle() -> None:
    """
    Show informative greeting for user at the shuffle menu.
    """
    print("* * *                  SHUFFLE SONGS                      * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you shuffle songs in the selected playlist.  *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_duplicate(sel_playlist: str) -> None:
    """
    Show informative greeting for user at the duplicate menu.
    """
    print("* * *                DUPLICATE PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu confirms whether you want to duplicate your       *")
    print("* selected playlist.                                          *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")
    print(f"Selected playlist: {sel_playlist}")
    print("")


def greet_delete() -> None:
    """
    Show informative greeting for user at the delete menu.
    """
    print("* * *                  DELETE PLAYLIST                    * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you delete one of your playlists.            *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_batch_add() -> None:
    """
    Show informative greeting for user at the batch menu.
    """
    print("* * *             BATCH ADD SONGS TO PLAYLIST             * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you add a batch of songs to the selected     *")
    print("* playlist. Choose the metadata tag and then type your        *")
    print("* desired tag contents to automatically add all songs whose   *")
    print("* metadata tag matches the string you entered.                *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


def greet_find_stale_playlists() -> None:
    """
    Show informative greeting for user at the sort menu.
    """
    print("* * *                FIND STALE PLAYLISTS                 * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you find stale playlists that have not been  *")
    print("* modified in more than 7 days. The process is automatic.     *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")


if __name__ == '__main__':
    main()
