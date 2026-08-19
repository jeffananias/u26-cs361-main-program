# Playlist Editor

## Description

Playlist Editor is a Python app that creates, edits, and displays music playlists from the command line. It relies on four microservices: [Date Difference](https://github.com/jeffananias/Date-Difference-Microservice), [Music Metadata Fetcher](https://github.com/jeffananias/Music-Metadata-Fetcher-Microservice), [List Randomizer](https://github.com/jeffananias/List-Randomizer-Microservice), and [ASCII Confirmation Generator](https://github.com/jeffananias/ASCII-Confirmation-Generator-Microservice).

It runs entirely on Python in a terminal. No frameworks or libraries were used except for the [tinytag](https://pypi.org/project/tinytag/) library. No LLMs were used in the creation of this project or the microservices.

This was my portfolio project for CS 361 Software Engineering I at Oregon State University in Summer 2026.

---

## Requirements

- The main program must be executed in a directory that contains music files.
- All playlist files must be in .m3u8 format.
- All music files must be in one of these formats: .mp3, .wav, .flac, .aac, or .ogg.
- All four microservices must be running to access the full feature set.
- Users must install [tinytag](https://pypi.org/project/tinytag/) (>=2.3.0) to use the Music Metadata Fetcher microservice.

---

## Features

Available commands: `create`, `select`, `add`, `batch`, `remove`, `reorder`, `shuffle`, `display`, `duplicate`, `delete`, `stale`, `exit`

- Create a playlist in the current working directory ("cwd")
- Select a playlist from the cwd
- Add one or more songs from the cwd to the selected playlist
- Add one or more songs in batch by artist, album, or year from the cwd to the selected playlist
- Remove one or more songs from the selected playlist
- Reorder songs in the selected playlist
- Shuffle songs in the selected playlist
- Display the contents of the selected playlist
- Duplicate the selected playlist file in the cwd
- Delete one or more playlists from the cwd
- Find stale playlists in the cwd (playlists with last modified dates that exceed seven days prior to today's date)
- Exit the program
