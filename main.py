# Name: Jeff Ananias
# Course: CS 361
# Description: This file provides a command-line interface for a user
#              to create, manage, and display local music playlists.
#
#              Playlists must be .m3u8 files and store songs of .mp3,
#              .wav, .flac, .aac, and .ogg format.

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import os
import re
import shutil
import sys
import time
from datetime import datetime

import greetings

# -----------------------------------------------------------------------------
# Global constants
# -----------------------------------------------------------------------------

CMDS = [
    "create", "select", "add", "batch", "remove", "reorder",
    "shuffle", "display", "duplicate", "delete", "stale", "exit"
]
CMDS_NOT_CHECKED = ["create", "select", "delete", "stale", "exit"]
CONFIRM_PROMPT = "Enter Y to confirm or deny with any other key: "
ERROR_INVALID_SYNTAX = "Invalid syntax. Try again."
ERROR_NO_PL_SONGS = "Playlist must contain songs before you can do this."
ERROR_NO_PLS = "Directory must contain playlists before you can do this."
PATH = os.getcwd()
RETURNING = "Returning to main menu."

# -----------------------------------------------------------------------------
# Main function and sub-calls
# -----------------------------------------------------------------------------

def main() -> None:
    """Provide command-line interface to user."""
    # Initialize selected playlist and wait for command
    sel_pl = ""
    while True:
        os.system("clear")
        greetings.main()
        if sel_pl == "":
            print("First, select a playlist.\n")
        else:
            print(f"Your selected playlist is {sel_pl}.\n")
        cmd = prompt()
        sel_pl = route_cmd(cmd, sel_pl)


def prompt() -> str:
    """Prompt user with instructions."""
    print("Commands:\ncreate | select | add | batch | remove | reorder")
    print("shuffle | display | duplicate | delete | stale | exit")
    return input("Type a command and press ENTER: ")


def route_cmd(cmd: str, sel_pl: str) -> None:
    """Route command to intended function with selected playlist."""
    if cmd not in CMDS:
        print("\nInvalid command. Reloading main menu...")
        time.sleep(3)
        return sel_pl
    else:
        if cmd not in CMDS_NOT_CHECKED and sel_pl == "":
            print("\nYou must select a playlist. Reloading main menu...")
            time.sleep(3)
            return sel_pl
        else:
            match cmd:
                case "create":
                    return create_pl(sel_pl)
                case "select":
                    return select_pl(sel_pl)
                case "add":
                    return add_songs(sel_pl)
                case "batch":
                    return batch_add_songs(sel_pl)
                case "remove":
                    return remove_songs(sel_pl)
                case "reorder":
                    return reorder_songs(sel_pl)
                case "shuffle":
                    return shuffle_songs(sel_pl)
                case "display":
                    return display_pl(sel_pl)
                case "duplicate":
                    return duplicate_pl(sel_pl)
                case "delete":
                    return delete_pl(sel_pl)
                case "stale":
                    return find_stale_pls(sel_pl)
                case "exit":
                    sys.exit()

# -----------------------------------------------------------------------------
# Create playlist function
# -----------------------------------------------------------------------------

def create_pl(sel_pl: str) -> None:
    """Show menu for creation of playlist."""
    os.system("clear")
    greetings.create_pl()

    pl_name = ""
    while pl_name == "":
        pl_name = input("\nWhat will be your playlist name? ")
        if pl_name == "":
            print("Cannot use empty string as name.")
    print(f"You named your playlist '{pl_name}'.")

    # Create playlist file and print ASCII art if yes; return if no
    confirmation = input(CONFIRM_PROMPT)
    if confirmation.lower() == "y":
        with open(pl_name + ".m3u8", "w") as f:
            f.write("")  # Create playlist file
        with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("Creation of playlist.")
        time.sleep(1)    # Allow time for microservice response
        with open("ascii_confirmation_generator.txt", "r") as f:
            print(f.read())
        print("Playlist created!\n" + RETURNING)
        with open("ascii_confirmation_generator.txt", "w") as f:
            f.write("")  # Clean microservice text file
        time.sleep(3)
        return sel_pl
    else:
        print("Playlist not created.\n" + RETURNING)
        time.sleep(3)
        return sel_pl

# -----------------------------------------------------------------------------
# Select playlist function and sub-calls
# -----------------------------------------------------------------------------

def select_pl(sel_pl: str) -> str:
    """Show menu for selection of playlist."""
    os.system("clear")
    greetings.select_pl()

    if contains_pls() is False:
        print(ERROR_NO_PLS + "\n" + RETURNING)
        time.sleep(3)
        return ""

    # Create sorted list of .m3u8 files and display them
    pls = [f[:-5] for f in sorted(os.listdir(PATH)) if f.endswith(".m3u8")]
    for i in range(len(pls)):
        print(f"({i + 1}) {pls[i]}")

    # Validate and confirm user input for selection
    choice_list = []
    while len(choice_list) == 0:
        choice_str = input("\nEnter number to select playlist: ")
        choice_list = validate_choice("add", choice_str, len(pls))
    selection = confirm_choice(choice_list, pls)
    if len(selection) != 0:
        print("\nPlaylist selected!\n" + RETURNING)
        time.sleep(3)
        return selection[0]
    else:
        print("\nPlaylist not selected.\n" + RETURNING)
        time.sleep(3)
        return sel_pl


def contains_pls() -> bool:
    """
    Return True if any playlists in current directory;
    return False if not.
    """
    pls = os.listdir(PATH)
    for pl in pls:
        if pl.endswith(".m3u8"):
            return True
    return False


def validate_choice(menu: str, choice_str: str, count: int) -> list:
    """Validate user input for choice(s) made in menus.
    
    Parameters:
    menu       -- menu in which user makes choice(s)
    choice_str -- string to be parsed for proper format
    count      -- maximum number that choice(s) cannot exceed
    """
    # Ensure string input contains either one integer, 'done', or
    # series of comma-delimited integers
    if menu == "select" and choice_str.isnumeric() is False:
        print(ERROR_INVALID_SYNTAX)
        return []
    if menu == "reorder" and choice_str == "done":
        return []
    pattern = re.compile(r"^\s*\d+\s*(?:,\s*\d+\s*)*$")
    if pattern.match(choice_str) is None:
        print(ERROR_INVALID_SYNTAX)
        return []

    # Ensure list of input integers is within range of options
    choice_list = [int(choice) for choice in choice_str.split(",")]
    if menu == "reorder" and len(choice_list) != 2:
        print(ERROR_INVALID_SYNTAX)
        return []
    for choice_item in choice_list:
        if choice_item < 1 or choice_item > count:
            print("Invalid choice. Only use available numbers.")
            return []

    return choice_list


def confirm_choice(choice_list: list, music_items: list) -> list:
    """Confirm user input for choice(s) made in menus.

    Parameters:
    choice_list -- list of integer(s) input by user for choice(s)
    music_items -- list of either songs or playlists
    """
    print("Your choice:")
    for choice_item in choice_list:
        print(f"{music_items[choice_item - 1]}")
    confirmation = input(CONFIRM_PROMPT)
    if confirmation.lower() == "y":
        confirmed_choices = []
        for choice_item in choice_list:
            confirmed_choices.append(music_items[choice_item - 1])
        return confirmed_choices
    else:
        print("Choice not confirmed.")
        return []

# -----------------------------------------------------------------------------
# Add songs function and sub-calls
# -----------------------------------------------------------------------------

def add_songs(sel_pl: str) -> None:
    """Show menu for addition of song(s) to selected playlist."""
    os.system("clear")
    greetings.add_songs()

    local_songs = get_local_songs()
    print_local_songs(sel_pl, local_songs)

    # Validate and confirm user input and store additions
    choice_list = []
    while len(choice_list) == 0:
        choice_str = input("\nEnter number(s) to choose song(s): ")
        choice_list = validate_choice("add", choice_str, len(local_songs))
    additions = confirm_choice(choice_list, local_songs)
    if len(additions) != 0:
        # Write additions to selected playlist
        print("Adding song(s) to playlist...")
        with open(sel_pl + ".m3u8", "a") as f:
            f.writelines(PATH + "/" + addition + "\n" for addition in additions)
        print("Done!")
        time.sleep(3)
        return sel_pl
    else:
        print("\nSongs not added.\n" + RETURNING)
        time.sleep(3)
        return sel_pl


def get_local_songs() -> list:
    """Create list of sorted songs in current path."""
    music_exts = (".mp3", ".wav", ".flac", ".aac", ".ogg")
    return [f for f in sorted(os.listdir(PATH)) if f.endswith(music_exts)]


def print_local_songs(sel_pl: str, songs: list) -> None:
    """Print song names from current directory."""
    with open(sel_pl + ".m3u8", "r") as f:
        playlist_contents = f.read()
        for i in range(len(songs)):
            # If song already in selected playlist, prepend asterisk
            if songs[i] in playlist_contents:
                print(f"({i + 1}) * {songs[i]}")
            else:
                print(f"({i + 1}) {songs[i]}")

# -----------------------------------------------------------------------------
# Batch add songs function and sub-calls
# -----------------------------------------------------------------------------

def batch_add_songs(sel_pl: str) -> None:
    """Write to selected playlist songs that match metadata search."""
    os.system("clear")
    greetings.batch_add_songs()

    songs = get_local_songs()
    with open("music_metadata.txt", "w") as f:
        f.write("\n".join(songs))
    time.sleep(1)

    print("Metadata types: 'artist', 'album', 'year'")
    md_type = input("Choose the type you want to search: ")
    acceptable_types = ["artist", "album", "year"]
    while md_type not in acceptable_types:
        print("Invalid metadata type. Try again.")
        md_type = input("Choose the type you want to search: ")

    md_list = get_md_list(acceptable_types, md_type)
    print(f"\nThese {md_type}s are available to add:\n")
    for i in range(len(md_list)):
        print(f"({i + 1}) {md_list[i]}")
    print()

    md_item = input(f"Choose the {md_type} to add: ")
    acceptable_items = range(len(md_list))
    while (int(md_item) - 1) not in acceptable_items:
        print(f"Invalid {md_type}. Try again.")
        md_item = input(f"Choose the {md_type} to add: ")
    md_choice = md_list[int(int(md_item) - 1)]

    print(f"You chose to add songs from the {md_type} {md_choice}.")
    confirmation = input(CONFIRM_PROMPT)
    if confirmation.lower() == "y":
        print("Adding this batch of songs...")
    else:
        print("Songs in batch not added.\n" + RETURNING)
        time.sleep(3)
        return sel_pl

    batch_additions = get_batch_additions(acceptable_types, md_type, md_choice)
    with open(sel_pl + ".m3u8", "a") as f:
        f.writelines(PATH + "/" + songs[batch_addition] + "\n" 
                     for batch_addition in batch_additions)

    with open("ascii_confirmation_generator.txt", "w") as f:
        f.write("Batch addition to playlist.")
    time.sleep(1)
    with open("ascii_confirmation_generator.txt", "r") as f:
        print(f.read())

    # Clean microservice text files
    with open("ascii_confirmation_generator.txt", "w") as f:
        f.write("")
    with open("music_metadata.txt", "w") as f:
        f.write("")

    print("Batch addition complete!\n" + RETURNING)
    time.sleep(3)
    return sel_pl


def get_md_list(acceptable_types: list, md_type: str) -> list:
    """Return list of metadata of specified type."""
    md_list = []
    with open("music_metadata.txt", "r") as f:
        md_list_from_file = f.read().splitlines()
        i = acceptable_types.index(md_type)
        while i < len(md_list_from_file):
            if md_list_from_file[i] not in md_list:
                md_list.append(md_list_from_file[i])
            i += 3
    return md_list


def get_batch_additions(acceptable_types: list, 
                     md_type: str, md_choice: str) -> list:
    """a"""
    batch_additions = []
    with open("music_metadata.txt", "r") as f:
        list_of_tags = f.read().splitlines()
        i = acceptable_types.index(md_type)
        j = 0
        while i < len(list_of_tags):
            if list_of_tags[i] == md_choice:
                batch_additions.append(j)
            i += 3
            j += 1
    return batch_additions

# -----------------------------------------------------------------------------
# Remove songs function and sub-calls
# -----------------------------------------------------------------------------

def remove_songs(sel_pl: str) -> None:
    """Show menu for removal of song(s) from selected playlist."""
    os.system("clear")
    greetings.remove_songs()

    print_pl_songs(sel_pl)
    pl_songs = get_pl_songs(sel_pl)
    if len(pl_songs) == 0:
        print(ERROR_NO_PL_SONGS + "\n" + RETURNING)
        time.sleep(3)
        return sel_pl

    # Validate and confirm user input and store removals
    choice_list = []
    while len(choice_list) == 0:
        choice_str = input("\nEnter number(s) to choose song(s): ")
        choice_list = validate_choice("remove", choice_str, len(pl_songs))
    removals = confirm_choice(choice_list, pl_songs)
    if len(removals) != 0:
        # Write removals to selected playlist
        print("Removing song(s) from playlist...")
        with open(sel_pl + ".m3u8", "w") as f:
            for pl_song in pl_songs:
                if pl_song not in removals:
                    f.write(PATH + "/" + pl_song + "\n")
        print("Done!")
        time.sleep(3)
        return sel_pl
    else:
        print("\nSongs not removed.\n" + RETURNING)
        time.sleep(3)
        return sel_pl


def print_pl_songs(sel_pl: str) -> None:
    """Print song names from selected playlist."""
    pl_songs = get_pl_songs(sel_pl)
    for i in range(len(pl_songs)):
        print(f"({i + 1}) {pl_songs[i]}")


def get_pl_songs(sel_pl: str) -> list:
    """Create list of songs in the selected playlist."""
    pl_songs = []
    with open(sel_pl + ".m3u8", "r") as f:
        song_paths = f.read().splitlines()
        for i in range(len(song_paths)):
            song = re.search(r"[^\/]+$", song_paths[i])
            pl_songs.append(song.group(0))
    return pl_songs

# -----------------------------------------------------------------------------
# Reorder songs function
# -----------------------------------------------------------------------------

def reorder_songs(sel_pl: str) -> None:
    """Swap items in selected playlist to reorder them."""
    os.system("clear")
    greetings.reorder_songs()

    print()
    pl_songs = get_pl_songs(sel_pl)
    if len(pl_songs) == 0:
        print(ERROR_NO_PL_SONGS + "\n" + RETURNING)
        time.sleep(3)
        return sel_pl

    choice_str = ""
    while choice_str != "done":
        print()
        print_pl_songs(sel_pl)
        choice_str = input("\nEnter the numbers of two songs to swap: ")
        choice_list = validate_choice("reorder", choice_str, len(pl_songs))
        if len(choice_list) != 0:
            reorder_couple = confirm_choice(choice_list, pl_songs)
            if len(reorder_couple) == 2:
                pl_songs[choice_list[0] - 1] = reorder_couple[1] # Second to first
                pl_songs[choice_list[1] - 1] = reorder_couple[0] # First to second
                with open(sel_pl + ".m3u8", "w") as f:
                    f.writelines(PATH
                                 + "/" 
                                 + pl_song 
                                 + "\n" for pl_song in pl_songs)
                print(f"{reorder_couple[0]} swapped with {reorder_couple[1]}")

    print("\nReorder complete!\n" + RETURNING)
    time.sleep(3)
    return sel_pl

# -----------------------------------------------------------------------------
# Display playlist function
# -----------------------------------------------------------------------------

def display_pl(sel_pl: str) -> None:
    """Show contents of selected playlist."""
    os.system("clear")
    greetings.display_pl(sel_pl)

    print_pl_songs(sel_pl)
    input("\nPress ENTER to go back.")
    return sel_pl

# -----------------------------------------------------------------------------
# Shuffle songs function
# -----------------------------------------------------------------------------

def shuffle_songs(sel_pl: str) -> None:
    """Randomize order of songs in selected playlist."""
    os.system("clear")
    greetings.shuffle_songs()
    
    pl_songs = get_pl_songs(sel_pl)
    if len(pl_songs) == 0:
        print(ERROR_NO_PL_SONGS + "\n" + RETURNING)
        time.sleep(3)
        return sel_pl
    
    print("Pre-shuffle order:\n")
    print_pl_songs(sel_pl)

    preshuffle_order = ""
    postshuffle_order = ""

    with open(sel_pl + ".m3u8", "r") as f:
        preshuffle_order = f.read()
    with open("list_randomizer.txt", "w") as f:
        f.write(preshuffle_order)
    time.sleep(1)
    with open("list_randomizer.txt", "r") as f:
        postshuffle_order = f.read()
    with open(sel_pl + ".m3u8", "w") as f:
        f.write(postshuffle_order)

    print("\nPost-shuffle order:")
    print_pl_songs(sel_pl)

    with open("ascii_confirmation_generator.txt", "w") as f:
        f.write("Shuffle of playlist.")
    time.sleep(1)
    with open("ascii_confirmation_generator.txt", "r") as f:
        print(f.read())

    print("Shuffle complete!\n" + RETURNING)

    # Clean microservice text files
    with open("ascii_confirmation_generator.txt", "w") as f:
        f.write("")
    with open("list_randomizer.txt", "w") as f:
        f.write("")

    time.sleep(3)
    return sel_pl

# -----------------------------------------------------------------------------
# Duplicate playlist function
# -----------------------------------------------------------------------------

def duplicate_pl(sel_pl: str) -> None:
    """Write new playlist file identical to selected playlist."""
    os.system("clear")
    greetings.duplicate_pl(sel_pl)

    confirmation = input(CONFIRM_PROMPT)
    if confirmation.lower() == "y":
        print("Starting duplication...")
    else:
        print("Duplication not confirmed.\n" + RETURNING)
        time.sleep(3)
        return sel_pl

    pl_file = PATH + "/" + sel_pl
    i = 1
    while os.path.exists(pl_file + " " + str(i) + ".m3u8"):
        i += 1
    shutil.copy2(pl_file + ".m3u8", pl_file + " " + str(i) + ".m3u8")

    print("Duplication complete!\n" + RETURNING)
    time.sleep(3)
    return sel_pl

# -----------------------------------------------------------------------------
# Delete playlist function
# -----------------------------------------------------------------------------

def delete_pl(sel_pl) -> str:
    """Delete playlist(s) from current directory."""
    os.system("clear")
    greetings.delete_pl()

    if contains_pls() is False:
        print(ERROR_NO_PLS + "\n" + RETURNING)
        time.sleep(3)
        return ""

    pls = [f[:-5] for f in sorted(os.listdir(PATH)) if f.endswith(".m3u8")]
    for i in range(len(pls)):
        print(f"({i + 1}) {pls[i]}")

    # Validate and confirm user input and delete playlist(s)
    choice_list = []
    while len(choice_list) == 0:
        choice_str = input("\nEnter number(s) to delete playlist(s): ")
        choice_list = validate_choice("delete", choice_str, len(pls))
    pls_to_del = confirm_choice(choice_list, pls)
    if len(pls_to_del) != 0:
        print("Starting deletion...")
        for pl_to_del in pls_to_del:
            os.remove(PATH + "/" + pl_to_del + ".m3u8")
        print("Deletion complete!\n" + RETURNING)
        time.sleep(3)
        if sel_pl in pls_to_del:
            return ""
        else:
            return sel_pl
    else:
        print("\nPlaylist(s) not deleted.\n" + RETURNING)
        time.sleep(3)
        return sel_pl

# -----------------------------------------------------------------------------
# Find stale playlists function
# -----------------------------------------------------------------------------

def find_stale_pls(sel_pl: str) -> None:
    """Print playlists that have been unmodified for >7 days."""
    os.system("clear")
    greetings.find_stale_pls()

    if contains_pls() is False:
        print(ERROR_NO_PLS + "\n" + RETURNING)
        time.sleep(3)
        return ""

    # Create list of sorted .m3u8 files in current path
    pls = [f[:-5] for f in sorted(os.listdir(PATH)) if f.endswith(".m3u8")]

    for pl in pls:
        last_mod_float = os.path.getmtime(PATH + "/" + pl + ".m3u8")
        last_mod_ts = datetime.fromtimestamp(last_mod_float)  # noqa: DTZ006
        last_mod_strf = last_mod_ts.strftime("%Y-%m-%d")
        with open("date_diff.txt", "w") as f:
            f.write(last_mod_strf)
        time.sleep(1)
        with open("date_diff.txt", "r") as f:
            response = f.read().split()
            status = response[0]
            days = int(response[1])
            if status == "OVERDUE:" and days > 7:
                print(pl)

    # Clean microservice text file
    with open("date_diff.txt", "w") as f:
        f.write("")

    input("\nPress ENTER to go back.")
    return sel_pl

# -----------------------------------------------------------------------------
# Run main function by default
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
