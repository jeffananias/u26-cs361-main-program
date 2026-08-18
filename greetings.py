# Name: Jeff Ananias
# Course: CS 361
# Description: This file provides the print statements for the
#              greetings called in main.

def main() -> None:
    """Show informative greeting at main menu."""
    print("\n           ____ ____ ____ ____ ____ ____ ____ ____ ")
    print("          ||P |||L |||A |||Y |||L |||I |||S |||T ||")
    print("          ||__|||__|||__|||__|||__|||__|||__|||__||")
    print("          |/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|")
    print("                ____ ____ ____ ____ ____ ____ ")
    print("               ||E |||D |||I |||T |||O |||R ||")
    print("               ||__|||__|||__|||__|||__|||__||")
    print("               |/__\\|/__\\|/__\\|/__\\|/__\\|/__\\|\n")
    print("                 Welcome to Playlist Editor!\n")
    print("This program creates, manages, and displays local music playlists.")
    print("Users must send commands in the local directory that contains the")
    print("playlists and songs they want to work with.\n")
    print("To exit the program from a sub-menu, press Ctrl+C.\n")


def create_pl() -> None:
    """Show informative greeting at create menu."""
    print("* * *                   CREATE PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you create a playlist file.                  *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")


def select_pl() -> None:
    """Show informative greeting at select menu."""
    print("* * *                   SELECT PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you select a playlist to then edit to        *")
    print("* contain any songs you want in any order that you specify.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def add_songs() -> None:
    """Show informative greeting at add menu."""
    print("* * *                ADD SONG TO PLAYLIST                 * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you add one or more songs to the selected    *")
    print("* playlist. To add more than one song, enter multiple         *")
    print("* numbers separated by commas. Stars indicate that the song   *")
    print("* is already in the playlist.                                 *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def batch_add_songs() -> None:
    """Show informative greeting at batch menu."""
    print("* * *             BATCH ADD SONGS TO PLAYLIST             * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you add a batch of songs to the selected     *")
    print("* playlist. Choose the metadata tag and then type your        *")
    print("* desired tag contents to automatically add all songs whose   *")
    print("* metadata tag matches the string you entered.                *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def remove_songs() -> None:
    """Show informative greeting at remove menu."""
    print("* * *              REMOVE SONG FROM PLAYLIST              * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you remove one or more songs from the        *")
    print("* selected playlist. To remove more than one song, enter      *")
    print("* multiple numbers separated by commas.                       *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def reorder_songs() -> None:
    """Show informative greeting at reorder menu."""
    print("* * *                   REORDER SONGS                     * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you reorder songs in the selected playlist.  *")
    print("* Enter two number separated by a comma to swap the songs     *")
    print("* next to those numbers. Enter 'done' to go to the main menu. *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")


def display_pl(sel_pl: str) -> None:
    """Show informative greeting at display menu."""
    print("* * *                   DISPLAY PLAYLIST                  * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This page displays the contents of the selected playlist.   *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")
    print(f"{sel_pl} Playlist:\n")


def shuffle_songs() -> None:
    """Show informative greeting at shuffle menu."""
    print("* * *                  SHUFFLE SONGS                      * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you shuffle songs in the selected playlist.  *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def duplicate_pl(sel_pl: str) -> None:
    """Show informative greeting at duplicate menu."""
    print("* * *                DUPLICATE PLAYLIST                   * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu confirms whether you want to duplicate your       *")
    print("* selected playlist.                                          *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")
    print(f"Selected playlist: {sel_pl}\n")


def delete_pl() -> None:
    """Show informative greeting at delete menu."""
    print("* * *                  DELETE PLAYLIST                    * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you delete one of your playlists.            *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")


def find_stale_pls() -> None:
    """Show informative greeting at find stale playlist menu."""
    print("* * *                FIND STALE PLAYLISTS                 * * *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *")
    print("* This menu lets you find stale playlists that have not been  *")
    print("* modified in more than 7 days. The process is automatic.     *")
    print("* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n")
