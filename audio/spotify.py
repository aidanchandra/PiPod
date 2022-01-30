import utility

from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os


scope = "user-follow-read," \
        "user-library-read," \
        "user-library-modify," \
        "user-modify-playback-state," \
        "user-read-playback-state," \
        "user-read-currently-playing," \
        "app-remote-control," \
        "playlist-read-private," \
        "playlist-read-collaborative," \
        "playlist-modify-public," \
        "playlist-modify-private," \
        "streaming"


class spotify_controller:
    def __init__(self) -> None:
        try:
            cid = os.environ["SPOTIPY_CLIENT_ID"]
            secret = os.environ["SPOTIPY_CLIENT_SECRET"]
        except KeyError:
            
        print(cid)
        print(secret)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

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

        query = '1kkM2kJVrhixB11RJK6qH9?'


        track = sp.track(query)


        utility.dump(track, "api_analysis/track")
    

if __name__ == '__main__':
    spotify_controller()