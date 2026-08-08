# Name: Jeff Ananias
# Course: CS 361
# Date: 2026-07-21
# Description: This file provides a command-line interface for a user to
#              select a playlist, add a playlist, display the selected
#              playlist, and exit the interface. Playlists are .m3u8 files
#              and store songs of .mp3, .wav, .flac, .aac, and .ogg format.

import os
import re
import time


def greet() -> None:
    """
    Show informative greeting for user.
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
    print("                       by Jeff Ananias")
    print("")
    print("This is a pre-release program with a limited feature set that")
    print("allows users to select an existent playlist, add a song to it,")
    print("and display it. Users must send commands in the local directory")
    print("that contains the playlists and songs.")
    print("")


def select() -> None:
    """
    Show menu to user for selection of playlist.
    """
    os.system("clear")

    print("* * *                   SELECT PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you select a playlist to then edit to        *")
    print("* contain any songs you want in any order that you specify.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")

    # Create list of sorted .m3u8 files in current path
    path = os.getcwd()
    files = sorted(os.listdir(path))
    playlists = [f[:-5] for f in files if f.endswith('.m3u8')]

    # Print enumerated playlist file names
    playlist_count = len(playlists)
    for i in range(playlist_count):
        print(f"({i + 1}) {playlists[i]}")
    print("")
    print("Any commands issued for this playlist will permanently")
    print("overwrite its contents. Some commands permit an undo")
    print("feature, but not all.")
    print("")

    # Validate user input and return selection
    sel_playlist = validate_selection(playlists, playlist_count)
    while sel_playlist is None:
        sel_playlist = validate_selection(playlists, playlist_count)
    return sel_playlist


def validate_selection(files: list, count: int) -> str:
    """
    Validate user input for playlist selection.
    """
    # Ensure input is number within range of options
    choice = input("Enter number to select: ")
    if choice.isnumeric() is False or int(choice) < 1 or int(choice) > count:
        print("Invalid choice.")
        return
    choice = int(choice)

    print("")
    print(f"You chose {files[choice - 1]}.")
    confirmation = input("Type Y and press ENTER to confirm, or type any other key and press ENTER to choose again: ")
    if confirmation.lower() == "y":
        print("")
        return files[choice - 1]
    else:
        print("Choice not confirmed.")


def add(sel_playlist: str) -> None:
    """
    Show menu to user for addition of one or more songs to selected playlist.
    """
    os.system("clear")

    print("* * *                ADD SONG TO PLAYLIST                 * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you add one or more songs to the selected    *")
    print("* playlist. To add more than one song, enter multiple         *")
    print("* numbers separated by commas. Stars indicate that the song   *")
    print("* is already in the playlist.                                 *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")

    # Create list of sorted music files in current path
    path = os.getcwd()
    files = sorted(os.listdir(path))
    music_exts = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
    songs = [f for f in files if f.endswith(music_exts)]

    # Print enumerated music file names
    song_count = len(songs)
    with open(sel_playlist + ".m3u8") as f:
        playlist_contents = f.read()
        for i in range(song_count):
            # If song already in selected playlist, prepend asterisk
            if songs[i] in playlist_contents:
                print(f"({i + 1}) * {songs[i]}")
            else:
                print(f"({i + 1}) {songs[i]}")
    print("")

    # Validate user input and store additions
    additions = validate_addition(songs, song_count)
    while additions is None:
        additions = validate_addition(songs, song_count)
    add_count = len(additions)
    
    # Write additions to selected playlist
    print("Adding song(s) to playlist...")
    with open(sel_playlist + ".m3u8", "a") as f:
        for addition in additions:
            f.write(path + "/" + addition + "\n")
    print("Done!")
    print("")


def validate_addition(files: list, count: int) -> list:
    """
    Validate user input for addition of one or more songs to selected
    playlist.
    """
    # Ensure string input is series of comma-delimited integers
    choices = input("Enter number(s) to add song(s): ")
    pattern = re.compile(r'^\s*\d+\s*(?:,\s*\d+\s*)*$')
    if pattern.match(choices) is None:
        print("Invalid syntax.")
        return

    # Ensure list of input integers is within range of options
    choices = [int(choice) for choice in choices.split(",")]
    for choice in choices:
        if choice < 1 or choice > count:
            print("Invalid choice(s). Only use available numbers.")
            return

    # Confirm choices and return them to add()
    print("")
    print("You chose the following song(s):")
    for choice in choices:
        print(f"{files[choice - 1]}")
    confirmation = input("Type Y and press ENTER to confirm, or type any other key and press ENTER to choose again: ")
    if confirmation.lower() == "y":
        print("")
        additions = []
        for choice in choices:
            additions.append(files[choice - 1])
        return additions
    else:
        print("Choice not confirmed.")


def display(sel_playlist: str) -> None:
    """
    Show contents of selected playlist to user.
    """
    os.system("clear")

    print("* * *                   DISPLAY PLAYLIST                  * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This page displays the contents of the selected playlist.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")
    print(f"{sel_playlist} Playlist:")
    print("")

    # Print each line in playlist but only contents after last slash
    with open(sel_playlist + ".m3u8") as f:
        song_paths = f.readlines()
        for song_path in song_paths:
            song = re.search(r'[^\/]+$', song_path)
            print(song.group(0)[:-1])
    print("")

    go_back = input("Press ENTER to go back.")


def main() -> None:
    """
    Provide command-line interface to user.
    """
    sel_playlist = None

    while True:
        os.system("clear")
        greet()

        # Tell user to select playlist if none selected
        if sel_playlist == None:
            print(f"First select a playlist.")
        else:
            print(f"Your selected playlist is {sel_playlist}.")
        print("")

        # Prompt user with instructions
        print("Commands: 'select', 'add', 'display', 'exit'")
        cmd = input("Type a command and press ENTER: ")
        print("")

        # Route user input to function
        if cmd == "select":
            sel_playlist = select()
            print("")
        elif cmd == "add":
            if sel_playlist == None:
                print("Please select a playlist first.")
                print("")
                time.sleep(2)
            else:
                add(sel_playlist)
        elif cmd == "display":
            if sel_playlist == None:
                print("Please select a playlist first.")
                print("")
                time.sleep(2)
            else:
                display(sel_playlist)
        elif cmd == 'exit':
            exit()
        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
