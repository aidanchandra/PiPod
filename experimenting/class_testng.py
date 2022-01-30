

from tkinter import N
from tkinter.messagebox import NO
from typing import List


class Song:
    def __init__(self, name, artist, album) -> None:
        self.name = name
        self.artist = artist
        self.album = album
        pass
    
    def set_artist(self, artist):
        self.artist = artist
    
    def set_album(self, album):
        self.album = album

    def __str__(self) -> str:
        return self.name



class Artist:
    def __init__(self, name, albums) -> None:
        self.name = name
        self.albums = [] if albums == None else albums

    def set_name(self, name):
        self.name = name

    def add_album(self, album):
        self.albums.append(album)

    def __str__(self) -> str:
        return self.name


class Album:
    def __init__(self, name, songs, artist) -> None:
        self.name = name
        self.songs = [] if songs == None else songs
        self.artist = artist
        pass

    def add_song(self, song):
        self.songs.append(song)

    def __str__(self) -> str:
        return self.name



tdg = Artist("Three Days Grace", albums=None)
onex = Album("One-X", songs=None, artist=tdg)
ntl = Song("Never Too Late",tdg, onex)

print(ntl.artist)
tdg.set_name("A")
print(ntl.artist)
