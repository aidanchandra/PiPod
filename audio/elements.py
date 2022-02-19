from abc import ABC, abstractmethod
from curses.ascii import SO
from multiprocessing.spawn import spawn_main
from pprint import pp, pprint
from turtle import update
from numpy import isin
from prettyprinter import cpprint
from re import I, L, S
from tkinter.messagebox import NO
from typing import Iterable, List
from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import utility
import unittest


class Element:
    ...

class Song:
    ...

class Song_Collecion(ABC):
    ...

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
class Song_Collection(ABC): #TODO: Force implementation

    @abstractmethod
    def get_songs(self) -> List[Song]:
        pass


artists = {}
albums = {}
users = {}
playlists = {}
songs = {}
    


class Song:

    # This might be ugly but let's store the data's name and then a tuple to its API path and then the data and/or object
    required_datas = {
        "name": ("name", None),
        "duration_ms": ("duration_ms", None),
        "disc_number": ("disc_number", None),
        "uri": ("uri", None),
        "album": (["album","uri"], None),
        "artist": (["artists",0,"uri"], None), #EVEN UGLIER - if the path is 
    }

    def __init__(self, song_data, sp_manager) -> None:

        self.data = None
        self.update_data(song_data)
        self.sp_manager = sp_manager

        songs[self.data["uri"]] = self


    def update_data(self, data_input):
        """An icky but potentially timesaving method to query an API json and
        store data from it into a dictionary elegantly and automatically

        Args:
            data_input (dict): The data we are about to update from - either partial or complete

        Raises:
            Exception: If we for some reason are not given a URI - from which the gaps may need 
            to be filled by querying spotify
        """
        self.data = self.required_datas.copy()
        for key in self.data:
            data = data_input

            location = self.data[key][0] ##OOOOOOOOOOOOOH goD THIS IS UGLY BUT IT MIGHT BE GENIUS
            if isinstance(location, List):
                for specifity in location:
                    try:
                        data = data[specifity]
                    except KeyError:
                        data = None
                        break
            else:
                try:
                    data = data[location]
                except KeyError:
                    data = None
                
            self.data[key] = data

        if self.data["uri"] == None:
            raise Exception("Tried to instantiate song without specifying a valid URI")


    def update_data_from_spotify(self):
        """
            Simply updates the objects data
        """
        if self.sp_manager == None:
            #TODO: Ideally this never happens except in testing 
            self.sp_manager = utility.instantiate_spotipy()

        data = self.sp_manager.track(self.data["uri"])
        self.update_data(data)

    @classmethod
    def from_urn(cls, song_urn:str, sp_manager:spotipy.Spotify) -> Song:
        """We can instantiate a song from its song_ID and the credentials manager

        Args:
            song_urn (str): URI/ID of the song
            sp_manager (spotipy.Spotify): Credentials manager

        Raises:
            Exception: Raises exception if fed the URN of something incorrect
        """        

        track = sp_manager.track(song_urn)

        if track["type"] != "track":
            raise Exception("Expected a type of track, not " + str(track["type"]))

        return cls(track,sp_manager)

    @classmethod
    def from_dict(cls, data:dict) -> Song:
        """We can instantiate a song from all the tons of data provided in an earlier API call, too

        Args:
            data (dict): the pertinent data from a previous api call
        """
        return cls(data, None)


    ##Simple getter methods that auto-update if we don't have the data that someone needs
    def get_name(self) -> str:
        if self.data["name"] == None:
            self.update_data_from_spotify()
        return self.data["name"]

    def get_duration(self) -> int:
        if self.data["duration_ms"] == None:
            self.update_data_from_spotify()
        return self.data["duration_ms"]

    def get_disc_number(self) -> int:
        if self.data["disc_number"] == None:
            self.update_data_from_spotify()
        return self.data["disc_number"]
    
    def get_ID(self):
        if self.data["uri"] == None:
            self.update_data_from_spotify()
        return self.data["uri"]

    def get_artist_ID(self):
        if self.data["artist"] == None:
            self.update_data_from_spotify()
        return self.data['artist']
        
    def get_artist(self, debug=False) -> Artist:
        """Here we want to return a class but it would be both time and resource
        intensive to regenerate that object each time. Also, by the nature of
        music, people tend to listen to lots of songs by the same artist. So in
        this implementation we keep a cache of each class so we can just
        grab that if a song wants to reference it's artist

        Returns:
            Artist: The Artist object of thsi song
        """

        #If we for some reason don't even no who the artist of a song is update that        
        if self.data["artist"] == None:
            self.update_data_from_spotify()

        if self.data["artist"] not in artists.keys():
            if debug:
                print("Getting new artist")
                regenerated = True
            artist = Artist(self.data["artist"], self.sp_manager)
            artists[self.data["artist"]] = artist #TODO: This should be removed and handled in Artist
        
        if not debug:
            return artists[self.data["artist"]]
        else:
            return (artists[self.data["artist"]], regenerated)


    
    def get_album_ID(self):
        if self.data["album"] == None:
            self.update_data_from_spotify()
        return self.data['album']

    def get_album(self, debug=False) -> Album:

        #If we for some reason don't even no who the artist of a song is update that        
        if self.data["album"] == None:
            self.update_data_from_spotify()

        if self.data["album"] not in albums.keys():
            if debug:
                print("Getting new album")
                regenerated = True
            album = Album(self.data["album"], self.sp_manager)
        
        if not debug:
            return albums[self.data["album"]]
        else:
            return (artists[self.data["artist"]], regenerated)

    def __str__(self) -> str:
        return self.get_name() #TODO: + "-" + self.get_artist().get_name()
    
    def __repr__(self) -> str:
        return "\'" + self.__str__() + "\'" 
    
    def data(self):
        return self.track
class Album(Song_Collecion):

    # This might be ugly but let's store the data's name and then a tuple to its API path and then the data and/or object
    required_datas = {
        "name": ("name", None),
        "image": (["images",2], None),
        "total_tracks": ("total_tracks", None),
        "uri": ("uri", None),
        "artist": (["artists",0,"id"], None), #EVEN UGLIER - if the path is 
        "songs": []
    }

    def __init__(self, song_data, sp_manager) -> None:

        self.data = None
        self.update_data(song_data)
        self.sp_manager = sp_manager

        albums[self.data["uri"]] = self


    def update_data(self, data_input):
        """An icky but potentially timesaving method to query an API json and
        store data from it into a dictionary elegantly and automatically

        Args:
            data_input (dict): The data we are about to update from - either partial or complete

        Raises:
            Exception: If we for some reason are not given a URI - from which the gaps may need 
            to be filled by querying spotify

        """

        if self.data == None:
            self.data = self.required_datas.copy()
        for key in self.data:
            data = data_input

            if isinstance(self.data[key], List):
                #If we come across a plan list in the required_datas spec, that
                #means it is supposed to come from somewhere more 'special'
                continue

            location = self.data[key][0] ##OOOOOOOOOOOOOH goD THIS IS UGLY BUT IT MIGHT BE GENIUS
            if isinstance(location, List):
                for specifity in location:
                    try:
                        data = data[specifity]
                    except KeyError:
                        data = None
                        break
            else:
                try:
                    data = data[location]
                except KeyError:
                    data = None
                
            self.data[key] = data

        if self.data["uri"] == None:
            raise Exception("Tried to instantiate album without specifying a valid URI")

        songs_temp = []
        for item in data_input["tracks"]["items"]:
            songs_temp.append(item["uri"])
            if item["uri"] not in songs: #We got data for a song we are not aware of! Might as well take it
                Song.from_dict(item) ##The Song class automatically adds itself to the cache upon instantiation


        self.data["songs"] = songs_temp


        


    def update_data_from_spotify(self):
        """
            Simply updates the objects data
        """
        if self.sp_manager == None:
            #TODO: Ideally this never happens except in testing 
            self.sp_manager = utility.instantiate_spotipy()

        data = self.sp_manager.album(self.data["uri"])
        self.update_data(data)

    @classmethod
    def from_urn(cls, album_urn:str, sp_manager:spotipy.Spotify) -> Album:
        """We can instantiate a song from its song_ID and the credentials manager

        Args:
            song_urn (str): URI/ID of the song
            sp_manager (spotipy.Spotify): Credentials manager

        Raises:
            Exception: Raises exception if fed the URN of something incorrect
        """        

        track = sp_manager.album(album_urn)

        if track["type"] != "album":
            raise Exception("Expected a type of album, not " + str(track["type"]))

        return cls(track,sp_manager)

    @classmethod
    def from_dict(cls, data:dict) -> Album:
        """We can instantiate a song from all the tons of data provided in an earlier API call, too

        Args:
            data (dict): the pertinent data from a previous api call
        """
        return cls(data, None)


    ##Simple getter methods that auto-update if we don't have the data that someone needs
    def get_name(self) -> str:
        if self.data["name"] == None:
            self.update_data_from_spotify()
        return self.data["name"]

    def get_image(self) -> int:
        if self.data["image"] == None:
            self.update_data_from_spotify()
        return self.data["image"]

    def get_total_tracks(self) -> int:
        if self.data["total_tracks"] == None:
            self.update_data_from_spotify()
        return self.data["total_tracks"]
    
    def get_ID(self):
        if self.data["uri"] == None:
            self.update_data_from_spotify()
        return self.data["uri"]

    def get_artist_ID(self):
        if self.data["artist"] == None:
            self.update_data_from_spotify()
        return self.data['artist']

        
    def get_artist(self, debug=False) -> Artist:
        """Here we want to return a class but it would be both time and resource
        intensive to regenerate that object each time. Also, by the nature of
        music, people tend to listen to lots of songs by the same artist. So in
        this implementation we keep a cache of each class so we can just
        grab that if a song wants to reference it's artist

        Returns:
            Artist: The Artist object of thsi song
        """

        #If we for some reason don't even no who the artist of a song is update that        
        if self.data["artist"] == None:
            self.update_data_from_spotify()

        if self.data["artist"] not in artists.keys():
            if debug:
                print("Generating a new artist!")
            artist = Artist(self.data["artist"], self.sp_manager)
            artists[self.data["artist"]] = artist
        
        return artists[self.data["artist"]]

    def get_songs_ID(self) -> List[str]:
        if self.data["songs"] == []:
            self.update_data_from_spotify()

        return self.data["songs"]

    def get_songs(self) -> List[Song]:
        if self.data["songs"] == []:
            self.update_data_from_spotify()

        returnable = []
        for song in self.data["songs"]:
            returnable.append(songs[song])

        return returnable

    def __str__(self) -> str:
        return self.get_name() #TODO: + "-" + self.get_artist().get_name()
    
    def __repr__(self) -> str:
        return "\'" + self.__str__() + "\'" 
    
    def data(self):
        return self.track
  

class Artist(Song_Collecion):

    # This might be ugly but let's store the data's name and then a tuple to its API path and then the data and/or object
    required_datas = {
        "name": ("name", None),
        "image": (["images",2], None),
        "uri": ("uri", None),
        "albums":("items"),
        "top_tracks":()
    },

    def __init__(self, artist_data, artist_top_songs, sp_manager) -> None:

        self.data = None
        self.update_data(artist_data)
        self.update_data(artist_top_songs)
        self.sp_manager = sp_manager


    def update_data(self, data_input):
        """An icky but potentially timesaving method to query an API json and
        store data from it into a dictionary elegantly and automatically

        Args:
            data_input (dict): The data we are about to update from - either partial or complete

        Raises:
            Exception: If we for some reason are not given a URI - from which the gaps may need 
            to be filled by querying spotify
        """
        if self.data == None: #TODO: Is this stricly necessary?
            self.data = self.required_datas.copy()
        for key in self.data:
            data = data_input

            location = self.data[key][0] ##OOOOOOOOOOOOOH goD THIS IS UGLY BUT IT MIGHT BE GENIUS
            if isinstance(location, List):
                for specifity in location:
                    try:
                        data = data[specifity]
                    except KeyError:
                        data = None
                        break
            else:
                try:
                    data = data[location]
                except KeyError:
                    data = None
                
            self.data[key] = data

        if self.data["uri"] == None:
            raise Exception("Tried to instantiate artist without specifying a valid URI")


    def update_data_from_spotify(self):
        """
            Simply updates the objects data
        """
        if self.sp_manager == None:
            #TODO: Ideally this never happens except in testing 
            self.sp_manager = utility.instantiate_spotipy()

        data = self.sp_manager.artist(self.data["uri"])
        top_songs = self.sp_manager.artist_top_tracks(self.data["uri"])

        self.update_data(data)
        self.update_data(top_songs)

    @classmethod
    def from_urn(cls, artist_urn:str, sp_manager:spotipy.Spotify) -> Album:
        """We can instantiate a song from its song_ID and the credentials manager

        Args:
            song_urn (str): URI/ID of the song
            sp_manager (spotipy.Spotify): Credentials manager

        Raises:
            Exception: Raises exception if fed the URN of something incorrect
        """        

        artist = sp_manager.artist(artist_urn)
        top_songs = sp_manager.artist_top_tracks(artist_urn)

        if artist["type"] != "artist":
            raise Exception("Expected a type of artist, not " + str(artist["type"]))

        return cls(artist,top_songs,sp_manager)

    @classmethod
    def from_dict(cls, data:dict) -> Album:
        """We can instantiate a song from all the tons of data provided in an earlier API call, too

        Args:
            data (dict): the pertinent data from a previous api call
        """
        return cls(data, None, None)


    ##Simple getter methods that auto-update if we don't have the data that someone needs
    def get_name(self) -> str:
        if self.data["name"] == None:
            self.update_data_from_spotify()
        return self.data["name"]

    def get_image(self) -> int:
        if self.data["image"] == None:
            self.update_data_from_spotify()
        return self.data["image"]

    def get_total_tracks(self) -> int:
        if self.data["total_tracks"] == None:
            self.update_data_from_spotify()
        return self.data["total_tracks"]
    
    def get_ID(self):
        if self.data["uri"] == None:
            self.update_data_from_spotify()
        return self.data["uri"]

    def get_artist_ID(self):
        if self.data["artist"] == None:
            self.update_data_from_spotify()
        return self.data['artist']

        
    def get_artist(self) -> Artist:
        """Here we want to return a class but it would be both time and resource
        intensive to regenerate that object each time. Also, by the nature of
        music, people tend to listen to lots of songs by the same artist. So in
        this implementation we keep a cache of each class so we can just
        grab that if a song wants to reference it's artist

        Returns:
            Artist: The Artist object of thsi song
        """

        #If we for some reason don't even no who the artist of a song is update that        
        if self.data["artist"] == None:
            self.update_data_from_spotify()

        if self.data["artist"] not in artists.keys():
            artist = Artist(self.data["artist"], self.sp_manager)
            artists[self.data["artist"]] = artist
        
        return artists[self.data["artist"]]

    def __str__(self) -> str:
        return self.get_name() #TODO: + "-" + self.get_artist().get_name()
    
    def __repr__(self) -> str:
        return "\'" + self.__str__() + "\'" 
    
    def data(self):
        return self.track
  


    


class Artist(Song_Collection):
    def __init__(self, urn:str, sp_manager:spotipy.Spotify) -> None:

        if sp_manager == None:
            sp_manager = utility.instantiate_spotipy()

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

  
class Elements_Test(unittest.TestCase):
    def setUp(self) -> None:

        self.sp_manager = utility.instantiate_spotipy()
        
        self.example_song_ID = "1kkM2kJVrhixB11RJK6qH9" ##Alive by Late Night Savior
        self.example_album_ID = "5pvuWbDHuIa12iIX34fj6N" ##Into the Aftermath by Late Night Savior

        
        test_data = utility.load_dict("test_data.json")

        self.song_data_from_album = test_data["song_data_from_album"]
        self.song_data_from_playlist = test_data["song_data_from_playlist"]["track"]
        self.song_malformed_data = test_data["song_malformed_data"]["track"]
        self.song_no_URI = test_data["song_no_URI"]["track"]

    def test_song_from_song_ID(self):
        test_song = Song.from_urn(self.example_song_ID, self.sp_manager)
        self.assertEqual(test_song.get_name(),"Alive")
        self.assertEqual(test_song.get_disc_number(),1)
        self.assertEqual(test_song.get_duration(),205250)
    
    def test_song_data_from_playlist(self):
        test_song = Song.from_dict(self.song_data_from_playlist)
        self.assertEqual(test_song.get_name(),"Stricken")
        self.assertEqual(test_song.get_disc_number(),1)
        self.assertEqual(test_song.get_duration(),245226)

    def test_song_from_malformed_data(self):
        test_song = Song.from_dict(self.song_malformed_data)
        self.assertEqual(test_song.get_name(),"Stricken")
        self.assertEqual(test_song.get_disc_number(),1)
        self.assertEqual(test_song.get_duration(),245226)

    def test_song_from_no_URI(self):
        with self.assertRaises(Exception):
            Song.from_dict(self.song_no_URI)

    def test_album_from_album_ID(self):
        test_album = Album.from_urn(self.example_album_ID, self.sp_manager)
        self.assertEqual(test_album.get_name(),"Into the Aftermath")
        self.assertEqual(test_album.get_total_tracks(),7)
        self.assertEqual(test_album.get_artist_ID(),"4yMIEw1F5ALRIv7bZz0jid")

        expected = ['Devil', 'Photograph', 'Angel', 'Forever', 'Alive', 'Sick and Twisted', 'Division']
        index = 0
        for song in test_album.get_songs():
            self.assertEqual(str(song), expected[index])
            index +=1

    def test_song_caching_after_album_instantiation(self):
        songs["spotify:track:6RJdYpFQwLyNfDc5FbjkgV"] #Testing to see if "Stricken" is in songs

    # def test_artist_caching_after_album_instantiation(self):
    #     pprint(artists)
    #     #We've never asked for Stricken so this should print getting a new artist #TODO:
    #     songs["spotify:track:6RJdYpFQwLyNfDc5FbjkgV"].get_artist(debug=True)

    #     songs["spotify:track:0GCX2m4I2m0ydo1Z0jyn1y"].get_artist(debug=True) #TODO:
        


            
if __name__ == "__main__":
    unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1
    unittest.main(exit=False)









