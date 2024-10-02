🎵 Interactive Playlist Manager

This Python project is a simple and interactive music player built with Tkinter for the GUI, Pygame for music playback, and NetworkX/Matplotlib for playlist visualization. It allows users to add, delete, shuffle, and visualize songs in a playlist, as well as play the first song in the list.

Features:
Add Songs: Upload music files from your local storage.
Delete Songs: Remove the last added song from the playlist.
Shuffle Playlist: Randomly shuffle the order of the playlist.
Display Playlist: View the current list of songs.
Play Music: Plays the first song in the playlist.
Visualize Playlist: View a graphical representation of the playlist as a directed graph, where each node represents a song.
Requirements:
Python 3.x
Tkinter: For GUI components.
Pygame: For music playback.
Matplotlib & NetworkX: For playlist visualization.
Installation:
Clone this repository:


git clone https://github.com/yourusername/interactive-playlist-manager.git
cd interactive-playlist-manager
Install the required dependencies:


pip install matplotlib networkx pygame
Run the application:


python music_player.py
Usage:
Add Song: Click on the Add Song button to choose a music file (MP3 format) from your local machine.
Manage Playlist: You can delete the last song, shuffle the playlist, and display the playlist.
Play Song: Play the first song in your playlist, with the volume set to maximum by default.
Visualize Playlist: View a graph where each song is a node connected by edges representing the order of the playlist.

Screenshot:

![image](https://github.com/user-attachments/assets/bda151a7-8281-43e7-a6f7-2c54e3f73e6d)



Notes:
Ensure your music files are in .mp3 format, as this is what Pygame supports by default.
The playlist is represented as a linked list, ensuring efficient addition and deletion operations.
The visualization helps to better understand the current order of the playlist.

License:

This project is licensed under the MIT License - see the LICENSE file for details.
