from abc import ABC, abstractmethod
from curses.ascii import SO
from pprint import pprint
from prettyprinter import cpprint
from re import I, S
from tkinter.messagebox import NO
from typing import List
from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class Playlist:
    ...

class Artist:
    ...

class Album:
    ...

class Search:
    ...

class User:
    ...

class Song:

    def __init__(self, data, sp_manager) -> None:

        self.track = data
        self.sp_manager = sp_manager

        pass

    @classmethod
    def from_urn(cls, song_urn:str, sp_manager:spotipy.Spotify) -> None:
        """We can instantiate a song from its song_ID and the credentials manager

        Args:
            song_urn (str): URI/ID of the song
            sp_manager (spotipy.Spotify): Credentials manager

        Raises:
            Exception: Raises exception if fed the URN of something incorrect
        """        

        sp_manager = sp_manager
        track = sp_manager.track(song_urn)

        if track["type"] != "track":
            raise Exception("Expected a type of track, not " + str(track["type"]))

        return cls(track,sp_manager)

    @classmethod
    def from_dict(cls, data:dict) -> None:
        """We can instantiate a song from all the tons of data provided in an earlier API call, too

        Args:
            data (dict): the pertinent data from a previous api call
        """
        return cls(data, None)

    def get_name(self) -> str:
        return self.track["name"]

    def get_duration(self) -> int:
        return self.track["duration_ms"]

    def get_disc_number(self) -> int:
        return self.track["disc_number"]
    
    def get_ID(self):
        return self.track["uri"]

    def get_artist(self) -> Artist:

        return Artist(self.track["artists"][0]["id"], sp_manager=self.sp_manager)

    def __str__(self) -> str:
        return self.get_name() #TODO: + "-" + self.get_artist().get_name()
    
    def __repr__(self) -> str:
        return "\'" + self.__str__() + "\'" 
    
    def data(self):
        return self.track

class Song_Collection(ABC):

    @abstractmethod
    def get_songs(self) -> List[Song]:
        pass

class Album(Song_Collection):

    def __init__(self, urn:str, sp_manager:spotipy.Spotify) -> None:

        self.album = sp_manager.album(urn)
        self.sp_manager = sp_manager

        if self.album["type"] != "album":
            raise Exception("Expected a type of album, not " + str(self.track["type"]))

        self.songs = []

    def get_songs(self) -> List[Song]:
        if self.songs != []:
            return self.songs
        
        for item in self.album["tracks"]["items"]:
            self.songs.append(Song.from_dict(item))

        return self.songs
    


class Artist(Song_Collection):
    def __init__(self, urn:str, sp_manager:spotipy.Spotify) -> None:

        self.artist = sp_manager.artist(urn)
        self.artist_albums_manager = sp_manager.artist_albums(urn)
        self.artist_top_songs_manager = sp_manager.artist_top_tracks(urn)

        self.sp_manager = sp_manager
        if self.artist["type"] != "artist":
            raise Exception("Expected a type of artist, not " + str(self.track["type"]))
        
        self.artist_albums = []
        self.artist_top_songs = []

    def from_urn(cls, urn:str, sp_manager:spotipy.Spotify):
        pass

    def from_dict(cls, data:dict):
        pass

    def get_name(self) -> str:
        return self.artist["name"]

    def get_popularity(self) -> int:
        return self.artist["popularity"]

    def get_thumbnail(self) -> str:
        return self.artist["images"][2]["url"]

    def get_genres(self) -> str:
        return self.artist["genres"]

    def get_ID(self):
        return self.track["uri"]

    def get_albums(self):
        if self.artist_albums != []:
            return self.artist_albums

        for item in self.artist_albums_manager["items"]:
            print(item["uri"])
            self.artist_albums.append(Album(urn=item["uri"], sp_manager=self.sp_manager))

    def get_songs(self) -> List[Song]:
        if self.artist_top_songs != []:
            return self.artist_top_songs
        
        for item in self.artist_top_songs_manager["tracks"]:
            self.artist_top_songs.append(Song(song_urn=item["uri"], sp_manager=self.sp_manager))




class User:
    def __init__(self, user_urn:str, sp_manager:spotipy.Spotify) -> None:
        self.user = sp_manager.user(user_urn)
        if self.user["type"] != "user":
            raise Exception("Expected a type of user, not " + str(self.track["type"]))
        self.user_playlists = sp_manager.user_playlists(user_urn)
        self.sp_manager = sp_manager
        self.playlists = []


    def get_playlists(self) -> List[Playlist]:
        if self.playlists != []:
            return self.playlists

        for playlist_item in self.user_playlists["items"]:
            playlist_uri = playlist_item["uri"]
            self.playlists.append(Playlist(playlist_uri, self.sp_manager))

        return self.playlists


class Playlist(Song_Collection): ##Done
    def __init__(self, urn:str, sp_manager:spotipy.Spotify) -> None:
        self.playlist = sp_manager.playlist(urn)
        self.sp_manager = sp_manager
        if self.playlist["type"] != "playlist":
            raise Exception("Expected a type of playlist, not " + str(self.track["type"]))
        self.songs = []

    def get_name(self) -> str:
        return self.playlist["name"]

    def get_thumbnail(self) -> str:
        return self.playlist["images"][2]["url"]

    def get_ID(self):
        return self.playlist["uri"]

    def get_owner(self) -> User:
        return self.playlist["owner"]

    def get_songs(self) -> List[Song]:
        if self.songs != []:
            return self.songs

        for song_item in self.playlist["tracks"]["items"]:
            self.songs.append(Song(song_item["track"]["uri"], sp_manager=self.sp_manager))
        return self.songs

    def __str__(self) -> str:
        return self.get_name()

    def __repr__(self) -> str:
        return "\'" + self.__str__() + "\'" 


            
if __name__ == "__main__":
    def get_sp_manager():
        cid = os.environ["SPOTIPY_CLIENT_ID"]
        secret = os.environ["SPOTIPY_CLIENT_SECRET"]
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    sp_m = get_sp_manager()
    print("Running elements.py as main")

    # user = User("aidanchandra", sp_m)
    # playlists = user.get_playlists()
    # print(playlists[0].get_songs())

    # artist = Artist("2xiIXseIJcq3nG7C8fHeBj", sp_m)
    album = Album("13topfW33NjnACjnRiZBX7", sp_m)

    cpprint(album.get_songs())
    for song in album.get_songs():
        cpprint(song.data())








