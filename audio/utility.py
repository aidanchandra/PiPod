import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

def dump(data:dict, filename:str, path:str='temp/'):
    f = open(path+filename+".json", "w") #TODO: Inconsistent implementation of adding filetype
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

def load_dict(path) -> dict:
    with open(path) as f:
        data = f.read()
    return json.loads(data)

def instantiate_spotipy():
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

    try:
        cid = os.environ["SPOTIPY_CLIENT_ID"]
        secret = os.environ["SPOTIPY_CLIENT_SECRET"]
    except KeyError:
        with open("creds.cache", encoding="utf-8") as f:
            creds = json.load(f)
            cid = creds["SPOTIPY_CLIENT_ID"]
            secret = creds["SPOTIPY_CLIENT_SECRET"]
            
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret, redirect_uri="http://localhost/"))

