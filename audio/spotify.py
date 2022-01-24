import utility

from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class spotify_controller:
    def __init__(self) -> None:
        cid = os.environ["SPOTIPY_CLIENT_ID"]
        secret = os.environ["SPOTIPY_CLIENT_SECRET"]
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

        # playlists = sp.user_playlists('spotify')
        # while playlists:
        #     for i, playlist in enumerate(playlists['items']):
        #         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        #     if playlists['next']:
        #         playlists = sp.next(playlists)
        #     else:
        #         playlists = None

        # artist = "Three Day's Grace"
        # track = "Never Too Late"
        # track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')
        # print(type(track_id))
        # utility.dump(track_id, "Example_Song_Data")

        # urn = '2xiIXseIJcq3nG7C8fHeBj'
        # track = sp.artist_albums(urn)
        # for track_item in track["items"]:
        #     print(track_item["name"],"   ",track_item["album_group"],"   ",track_item["album_type"],"   ",track_item["total_tracks"])
        # utility.dump(track, "Example_Song_Data")

        query = 'aidanchandra'


        track = sp.current_user_playlists(query)


        utility.dump(track, "api_analysis/current_user_playlists")
    

if __name__ == '__main__':
    spotify_controller()