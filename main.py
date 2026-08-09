# Name: Jeff Ananias
# Course: CS 361
# Due Date: 2026-08-10
# Description: This file provides a command-line interface for a user to
#              select a playlist, add a playlist, display the selected
#              playlist, and exit the interface. Playlists are .m3u8 files
#              and store songs of .mp3, .wav, .flac, .aac, and .ogg format.

import os
import re
from time import sleep


PATH = os.getcwd()


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
    print("This program creates, manages, and displays local music playlists.")
    print("Users must send commands in the local directory that contains the")
    print("playlists and songs they want to work with.")
    print("")
    print("To exit the program from a submenu, press Ctrl+C.")
    print("")


def check_selection(sel_playlist: str) -> None:
    """
    Tell user to select playlist if none selected.
    """
    if sel_playlist == None:
        print(f"First select a playlist.\n")
    else:
        print(f"Your selected playlist is {sel_playlist}.\n")


def prompt() -> str:
    """
    Prompt user with instructions.
    """
    print("Commands:")
    print("create | select | add | remove | reorder | display")
    print("shuffle | duplicate | delete | batch | sort | exit")
    return input("Type a command and press ENTER: ")


def route_cmd(cmd: str, sel_playlist: str) -> None:
    """
    Route user input command to intended function with selected playlist.
    """
    if cmd != "create" and sel_playlist == None:
        print("Please select a playlist first.\n")
        sleep(2)
    else:
        match cmd:
            case "create":
                create()
            case "add":
                add(sel_playlist)
            case "remove":
                remove(sel_playlist)
            case "reorder":
                reorder(sel_playlist)
            case "display":
                display(sel_playlist)
            case "shuffle":
                shuffle(sel_playlist)
            case "duplicate":
                duplicate(sel_playlist)
            case "delete":
                delete(sel_playlist)
            case "batch":
                add_batch(sel_playlist)
            case "sort":
                sort(sel_playlist)
            case 'exit':
                exit()
            case _:
                print("Invalid command.")


def create() -> None:
    os.system("clear")

    print("* * *                   CREATE PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you create a playlist file.                  *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")

    playlist_name = input("What will be your playlist name? ")
    print(f"You named your playlist '{playlist_name}'.")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        with open(playlist_name + ".m3u8", "w") as f:
            f.write("")
        print("")
        print("Playlist created. Returning to main menu.")
        sleep(2)
    else:
        print("Playlist not created. Returning to main menu.")
        sleep(2)


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
    files = sorted(os.listdir(PATH))
    playlists = [f[:-5] for f in files if f.endswith('.m3u8')]

    # Print enumerated playlist file names
    playlist_count = len(playlists)
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
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("")
        return files[choice - 1]
    else:
        print("Choice not confirmed.")


def create_song_list() -> list:
    """
    Create list of sorted music files in current path.
    """
    files = sorted(os.listdir(PATH))
    music_exts = ('.mp3', '.wav', '.flac', '.aac', '.ogg')
    return [f for f in files if f.endswith(music_exts)]


def print_song_list(menu: str, sel_playlist: str, songs: list) -> None:
    """
    Print enumerated music file names based on whether the list is for the add
    menu or the remove menu.
    """
    match menu:
        case "add":
            with open(sel_playlist + ".m3u8") as f:
                playlist_contents = f.read()
                for i in range(len(songs)):
                    # If song already in selected playlist, prepend asterisk
                    if songs[i] in playlist_contents:
                        print(f"({i + 1}) * {songs[i]}")
                    else:
                        print(f"({i + 1}) {songs[i]}")
            print("")
        case "remove":
            with open(sel_playlist + ".m3u8") as f:
                song_paths = f.readlines()
                for i in range(len(song_paths)):
                    song = re.search(r'[^\/]+$', song_paths[i])
                    print(f"({i + 1}) {song.group(0)[:-1]}")
            print("")


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

    songs = create_song_list()
    print_song_list("add", sel_playlist, songs)

    # Validate user input and store additions
    additions = validate_add_or_rem(songs, len(songs))
    while additions is None:
        additions = validate_add_or_rem(songs, len(songs))
    add_count = len(additions)
    
    # Write additions to selected playlist
    print("Adding song(s) to playlist...")
    with open(sel_playlist + ".m3u8", "a") as f:
        for addition in additions:
            f.write(PATH + "/" + addition + "\n")
    print("Done!")
    print("")


def remove(sel_playlist: str) -> None:
    """
    Show menu to user for removal of one or more songs to selected playlist.
    """
    os.system("clear")

    print("* * *              REMOVE SONG FROM PLAYLIST              * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you remove one or more songs from the        *")
    print("* selected playlist. To remove more than one song, enter      *")
    print("* multiple numbers separated by commas.                       *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("")

    songs = create_song_list()
    print_song_list("remove", sel_playlist, songs)

    # Validate user input and store additions
    removals = validate_add_or_rem(songs, len(songs))
    while removals is None:
        removals = validate_add_or_rem(songs, len(songs))
    remove_count = len(removals)
    
    # Write additions to selected playlist
    print("Removing song(s) from playlist...")
    with open(sel_playlist + ".m3u8", "w") as f:
        for song in songs:
            if song not in removals:
                f.write(PATH + "/" + song + "\n")
    print("Done!")
    print("")


def validate_add_or_rem(files: list, count: int) -> list:
    """
    Validate user input for addition or removal of one or more songs to
    selected playlist.
    """
    # Ensure string input is series of comma-delimited integers
    choices = input("Enter number(s) to choose song(s): ")
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

    # Confirm choices and return them
    print("")
    print("You chose the following song(s):")
    for choice in choices:
        print(f"{files[choice - 1]}")
    confirmation = input("Confirm with Y or deny with any other key: ")
    if confirmation.lower() == "y":
        print("")
        adds_or_rems = []
        for choice in choices:
            adds_or_rems.append(files[choice - 1])
        return adds_or_rems
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
        check_selection(sel_playlist)
        cmd = prompt()
        if cmd == "select":
            sel_playlist = select()
        else:
            route_cmd(cmd, sel_playlist)


if __name__ == '__main__':
    main()
