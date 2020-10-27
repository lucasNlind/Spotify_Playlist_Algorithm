import os
import sys
import json
import webbrowser
from json.decoder import JSONDecodeError
from pprint import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import pandas as pd

def percent(n):
    return int(n * 100)

cid = 'ab16321ec31348b881a8965914f2f23a'
secret = '926b25bd2ec74144b2b7627120fbd1d0'
username = 'pimplepopper23'
scope = 'playlist-modify-public user-top-read'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

try:
    token = util.prompt_for_user_token(username, scope=scope)
except Exception:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope)

# Prints json data in a format that we can read \/
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# Creating spotify object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager, auth=token)

user = sp.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

# Grabbing data from the current_user
display_name = user['display_name']
num_followers = user["followers"]['total']
my_id = sp.me()['id']

# ARTIST URI's FOR SAMPLE TESTS
tame_uri = 'spotify:artist:5INjqkS1o8h1imAzPqGZBb'
diplo_uri = 'spotify:artist:5fMUXHkw8R8eOP2RNVYEZX'
calvin_harris_uri = 'spotify:artist:7CajNmpbOovFoOoasH2HaY'


# ******************* RUNNING STATISTICS ON 'SUNNYD' and "RAINY DAY" PLAYLISTS *******************

# Save the URI of the playlist I want to analyze
sunny_d_uri = 'spotify:playlist:6h5GNBGSdzPy0SE6NOMddo'
rainy_day_uri = 'spotify:playlist:5BqayxS0OumOudUrK6Txek'

# Store the track URI's into an array that is needed for the audio_features method
sunny_d_results = sp.playlist_items(sunny_d_uri, offset = 0, fields='items.track.id,total', additional_types=['track'])
sunny_d_tracks = []

rainy_day_results = sp.playlist_items(rainy_day_uri, offset = 0, fields='items.track.id.total', additional_types=['track'])
rainy_day_tracks = []

# Adding track id's from playlist into a local array
for el in sunny_d_results['items']:
    sunny_d_tracks.append('spotify:track:' + el['track']['id'])
for el in rainy_day_results['items']:
    rainy_day_tracks.append('spotify:track:' + el['track']['id'])

# Features
sunny_d_features = sp.audio_features(tracks=sunny_d_tracks)
rainy_day_features = sp.audio_features(tracks=rainy_day_tracks)

print()

# Features that I want to track:
# Energy
# Tempo
# Danceability
# Valence
# Tempo

def display_playlist_features(features):
    low_energy_songs = []
    sum_energy = 0
    low_tempo_songs = []
    sum_tempo = 0
    low_danceability_songs = []
    sum_danceability = 0
    low_valence_songs = []
    sum_valence = 0
    minor_key_songs = []

    for i in range(len(features)):
        if features[i]['energy'] < 0.75:
            temp_track = sp.track(features[i]['uri'])
            low_energy_songs.append([temp_track['name'], features[i]['energy']])
        if features[i]['tempo'] < 105:
            temp_track = sp.track(features[i]['uri'])
            low_tempo_songs.append([temp_track['name'], features[i]['tempo']])
        if features[i]['danceability'] < 0.65:
            temp_track = sp.track(features[i]['uri'])
            low_danceability_songs.append([temp_track['name'], features[i]['danceability']])
        if features[i]['mode'] == 0:
            temp_track = sp.track(features[i]['uri'])
            minor_key_songs.append([temp_track['name'], 'minor'])
        if features[i]['valence'] < 0.75:
            temp_track = sp.track(features[i]['uri'])
            low_valence_songs.append([temp_track['name'], features[i]['valence']])
        
        sum_energy += features[i]['energy']
        sum_tempo += features[i]['tempo']
        sum_danceability += features[i]['danceability']
        sum_valence += features[i]['valence']

    print()
    print('*---------- DATA FEATURES----------*' + '\n')
    print('Average energy: ', round(sum_energy / len(features), 2))
    print('Average tempo: ', round(sum_tempo / len(features), 2))
    print('Average danceability: ', round(sum_danceability / len(features), 2))
    print('Average valence: ', round(sum_valence / len(features), 2))

    print()
    print('-------------------------------------')
    print('Tracks with low (< 0.75) energy: \n')
    pprint(low_energy_songs)
    print()
    print(len(low_energy_songs), '/', len(features),
        ':', percent(len(low_energy_songs)/len(features)), '%')
    print('-------------------------------------')

    print('Tracks that are low (< 105) tempo: \n')
    pprint(low_tempo_songs)
    print()
    print(len(low_tempo_songs), '/', len(features),
        ':', percent(len(low_tempo_songs)/len(features)), '%')
    print('-------------------------------------')

    print('Tracks with low (< 65) danceability: \n')
    pprint(low_danceability_songs)
    print()
    print(len(low_danceability_songs), '/', len(features),
        ':', percent(len(low_danceability_songs)/len(features)), '%')
    print('-------------------------------------')

    print('Tracks with low (< 0.75) valence: \n')
    pprint(low_valence_songs)
    print()
    print(len(low_valence_songs), '/', len(features), ':', percent(len(low_valence_songs)/len(features)), '%')
    print('-------------------------------------')

    print('Tracks in minor key: \n')
    pprint(minor_key_songs)
    print()
    print(len(minor_key_songs), "/", len(features),
        ":", percent(len(minor_key_songs)/len(features)), '%')
    print('-------------------------------------')
    print()

print('Generating audio features for playlist: SunnyD...')
display_playlist_features(sunny_d_features)
print('Generating audio features for playlist: Rainy Day...')
display_playlist_features(rainy_day_features)

# ******************* DISPLAY CURRENT USER PLAYLISTS *******************
current_playlists = sp.current_user_playlists(limit=50, offset=0)
playlists_data = current_playlists['items']
my_playlists = []
while current_playlists['next']:
    current_playlists = sp.next(current_playlists)
    playlists_data.extend(current_playlists['items'])

for play in playlists_data:
    my_playlists.append(play['name'])

# print("My Playlists: ", my_playlists)
# print()

# ******************* ADD ITEM TO PLAYLIST *******************
input_playlist = 'spotify:playlist:1Yp1rShzcf3wOrHhGJloNw'
songs_to_add = ['spotify:track:2IFFKj9orAsQOOS0JRhHAW']
# sp.playlist_add_items(input_playlist, songs_to_add)

# ******************* DISPLAY A PLAYLISTS'S TRACKS *******************
lo_fi_playlist_uri = 'spotify:playlist:7Ea4ut5vVyWwK6ssFfFmP8'
#fetched = sp.playlist_items(lo_fi_playlist_uri, offset=offset, fields='items.track.name')

# pprint(fetched['items'])
# print()

# ******************* DISPLAY MY TOP ARTISTS *******************
fetched_top_artists = sp.current_user_top_artists(limit=20,offset=0,time_range='medium_term')
#for i, item in enumerate(fetched_top_artists['items']):
    #print(i + 1, item['name'])
#print()

# ******************* DISPLAY MY TOP ARTISTS *******************
fetched_top_tracks = sp.current_user_top_tracks(limit=20,offset=0,time_range='medium_term')
#for i, item in enumerate(fetched_top_tracks['items']):
    #print(i + 1, item['name'])
#print()

# ******************* CREATE A PLAYLIST FOR USER *******************
playlist_name = "Spotify API"
# sp.user_playlist_create(my_id, playlist_name)

# ******************* DISPLAY ARTIST ALBUMS *******************
results = sp.artist_albums(calvin_harris_uri, album_type='album')
albums_data = results['items']
albums = []
while results['next']:
    results = sp.next(results)
    albums_data.extend(results['items'])

for album in albums_data:
    if not album['name'] in albums:
        albums.append(album['name'])

# print("Calvin Harris's Albums: ", albums)

# ******************* DISPLAY AUDIO FEATURES *******************
results = sp.audio_features(tracks=['spotify:track:7ef4DlsgrMEH11cDZd32M6'])
# print(results[0]['danceability'])

# ******************* CREATE PLAYLIST AND ADD SONGS TO PLAYLIST *******************

# Create playlist
playlist_name = "SunnyD"
playlist_description = "Go outside silly!"
# sp.user_playlist_create(my_id, playlist_name, description=playlist_description)

# Get the ID of the most recently created playlist
playlists = sp.current_user_playlists()
playlist_id = 'spotify:playlist:' + playlists['items'][0]['id']

# Upload a cover image
playlist_image = ''
#sp.playlist_upload_cover_image(playlist_id, playlist_image)

