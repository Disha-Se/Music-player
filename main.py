import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import os

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Pygame Mixer Initialization Error: {e}")

class SongNode:
    def __init__(self, song_name, artist, file_path):
        self.song_name = song_name
        self.artist = artist
        self.file_path = file_path
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None

    def add_song(self, name, artist, file_path):
        new_song = SongNode(name, artist, file_path)
        if not self.head:
            self.head = new_song
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_song
        print(f"Added: {name}")

    def delete_last_song(self):
        if not self.head:
            print("Playlist is empty.")
            return False
        if not self.head.next:
            to_delete = self.head
            self.head = None
            del to_delete
            print("Deleted the last song.")
            return True
        temp = self.head
        while temp.next.next:
            temp = temp.next
        to_delete = temp.next
        temp.next = None
        del to_delete
        print("Deleted the last song.")
        return True

    def display_playlist(self):
        if not self.head:
            print("Playlist is empty.")
            return []
        temp = self.head
        songs = []
        while temp:
            songs.append(f"Song: {temp.song_name} ")
            temp = temp.next
        return songs

    def shuffle_playlist(self):
        if not self.head or not self.head.next:
            return
        prev, current = None, self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
        print("Playlist shuffled.")

    def visualize_playlist(self):
        if not self.head:
            print("Playlist is empty.")
            return None
        G = nx.DiGraph()
        temp = self.head
        pos = {}
        index = 0
        while temp:
            G.add_node(temp.song_name, label=f"{temp.song_name}\n")
            if temp.next:
                G.add_edge(temp.song_name, temp.next.song_name)
            pos[temp.song_name] = (index, 0)
            temp = temp.next
            index += 1
        return G, pos

    def play_first_song(self):
        if self.head:
            return self.head.file_path
        else:
            return None

class PlaylistGUI:
    def __init__(self, root, playlist):
        self.playlist = playlist
        self.root = root
        self.root.title("Interactive Playlist Manager")
        self.root.configure(bg='lightpink')

        self.main_frame = tk.Frame(root, bg='lightpink')
        self.main_frame.pack(padx=20, pady=20)

        self.song_selection_frame = tk.LabelFrame(self.main_frame, text="Add Song", bg='lightpink')
        self.song_selection_frame.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(self.song_selection_frame, text="Add Song", command=self.choose_file, bg='white')
        self.add_button.grid(row=0, column=1, padx=5)

        self.playlist_management_frame = tk.LabelFrame(self.main_frame, text="Manage Playlist", bg='lightpink')
        self.playlist_management_frame.grid(row=1, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(self.playlist_management_frame, text="Delete Last Song", command=self.delete_last_song, bg='white')
        self.delete_button.grid(row=0, column=0, padx=5)

        self.shuffle_button = tk.Button(self.playlist_management_frame, text="Shuffle Playlist", command=self.shuffle_playlist, bg='white')
        self.shuffle_button.grid(row=0, column=1, padx=5)

        self.display_button = tk.Button(self.playlist_management_frame, text="Display Playlist", command=self.display_playlist, bg='white')
        self.display_button.grid(row=0, column=2, padx=5)

        self.play_button = tk.Button(self.playlist_management_frame, text="Play First Song", command=self.play_first_song, bg='white')
        self.play_button.grid(row=0, column=3, padx=5)

        self.visualization_frame = tk.LabelFrame(self.main_frame, text="Playlist Visualization", bg='lightpink')
        self.visualization_frame.grid(row=2, column=0, padx=10, pady=10)

        self.canvas = tk.Canvas(self.visualization_frame, width=600, height=400, bg='lightpink')
        self.canvas.pack()

        self.fig_agg = None

    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Select a music file", filetypes=[("Music Files", "*.mp3")])
        if file_path:
            song_name = os.path.basename(file_path).split('.')[0]  
            artist_name = "Unknown"  
            self.playlist.add_song(song_name, artist_name, file_path)
            self.update_visualization()
        else:
            messagebox.showerror("Error", "No file selected.")

    def delete_last_song(self):
        success = self.playlist.delete_last_song()
        if success:
            self.update_visualization()
        else:
            messagebox.showinfo("Info", "Playlist is empty.")

    def shuffle_playlist(self):
        self.playlist.shuffle_playlist()
        self.update_visualization()

    def display_playlist(self):
        songs = self.playlist.display_playlist()
        messagebox.showinfo("Playlist", "\n".join(songs))

    def play_first_song(self):
        file_path = self.playlist.play_first_song()
        if file_path:
            try:
                print(f"Playing: {file_path}")
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(1.0) 
                self.check_playing()
            except pygame.error as e:
                print(f"Error playing song: {e}")
                messagebox.showerror("Error", f"Could not play the song: {e}")
        else:
            messagebox.showinfo("Info", "No songs in the playlist.")

    def check_playing(self):
        if pygame.mixer.music.get_busy():
            self.root.after(100, self.check_playing)  
        else:
            print("Song finished playing.")

    def update_visualization(self):
        self.canvas.delete("all")
        result = self.playlist.visualize_playlist()
        if result is None:
            if self.fig_agg:
                self.fig_agg.get_tk_widget().pack_forget()
                self.fig_agg = None
            return
        G, pos = result
        if self.fig_agg:
            self.fig_agg.get_tk_widget().pack_forget()
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = nx.get_node_attributes(G, 'label')
        node_colors = ['skyblue' if i % 2 == 0 else 'lightgreen' for i in range(len(G.nodes))]
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, ax=ax)
        self.fig_agg = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_agg.draw()
        self.fig_agg.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    playlist = Playlist()
    gui = PlaylistGUI(root, playlist)
    root.mainloop()
