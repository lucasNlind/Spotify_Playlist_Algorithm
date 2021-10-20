import os
import time
import requests
from json.decoder import JSONDecodeError
from pprint import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def print_songs(songs):
    for i in range(len(songs)):
        print(' -', songs[i][0])

def print_recommendations(songs):
    for i in range(len(songs)):
        print(' -', songs[i][0], ',', songs[i][1])

def percent(n):
    return int(n * 100)

cid = 'CID'
secret = 'SECRET'
username = 'username'
scope = 'playlist-modify-public user-top-read'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

try:
    token = util.prompt_for_user_token(username, scope=scope)
except Exception:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope)

# Creating spotify object
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager, auth=token)

user = sp.current_user()

# Grabbing data from the current_user
display_name = user['display_name']
num_followers = user["followers"]['total']
my_id = sp.me()['id']

# ARTIST URI's FOR SAMPLE TESTS
tame_uri = 'spotify:artist:5INjqkS1o8h1imAzPqGZBb'
diplo_uri = 'spotify:artist:5fMUXHkw8R8eOP2RNVYEZX'
calvin_harris_uri = 'spotify:artist:7CajNmpbOovFoOoasH2HaY'

# HELPER FUNCTIONS

def get_top_artists():
    res = sp.current_user_top_artists(time_range='long_term', limit = 5)
    rtn = []
    for el in res['items']:
        rtn.append(el['name'])
    return rtn

def get_artist(name):
    res = sp.search(q='artist:' + name, type='artist')
    items = res['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_recommendations_for_artist(artist):
    res = sp.recommendations(seed_artists=[artist['id']], limit=20)
    rtn = []
    for t in res['tracks']:
        rtn.append([t['name'], t['artists'][0]['name'], t['uri']])
    return rtn

def get_recommendations_for_top_artists(artists):
    rtn = []
    for a in artists:
        tmp = get_artist(a)
        rtn += get_recommendations_for_artist(tmp)
    return rtn
    
def get_audio_features_for_recommended_tracks(recommendations):
    tracks = []
    for i in range(len(recommendations)):
        tracks.append(recommendations[i][2])
    features = sp.audio_features( tracks = tracks )
    return features

def get_reccomendations_for_bad_weather(recommendations):
    features = get_audio_features_for_recommended_tracks(recommendations)
    rtn = []
    for i in range(len(features)):
        if features[i]['energy'] < 0.5 and features[i]['valence'] < 0.5:
            rtn.append([recommendations[i][0], recommendations[i][1]])
    return rtn

def get_reccomendations_for_good_weather(recommendations):
    features = get_audio_features_for_recommended_tracks(recommendations)
    rtn = []
    for i in range(len(features)):
        if features[i]['energy'] > 0.6 and features[i]['valence'] > 0.6:
            rtn.append([recommendations[i][0], recommendations[i][1]])
    return rtn

def display_playlist_features(uri):
    print()

    # Get list of tracks for playlist
    playlist_results = sp.playlist_items(uri, offset = 0, fields='items.track.id,total', additional_types=['track'])
    tracks = []

    # Save the IDS for tracks
    for el in playlist_results['items']:
        tracks.append('spotify:track:' + el['track']['id'])

    # Get audio features
    features = sp.audio_features( tracks = tracks )

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
        if features[i]['tempo'] < 95:
            temp_track = sp.track(features[i]['uri'])
            low_tempo_songs.append([temp_track['name'], features[i]['tempo']])
        if features[i]['danceability'] < 0.65:
            temp_track = sp.track(features[i]['uri'])
            low_danceability_songs.append([temp_track['name'], features[i]['danceability']])
        if features[i]['mode'] == 0:
            temp_track = sp.track(features[i]['uri'])
            minor_key_songs.append([temp_track['name'], 'minor'])
        if features[i]['valence'] < 0.50:
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
    print_songs(low_energy_songs)
    print()
    print(len(low_energy_songs), '/', len(features),
        ':', percent(len(low_energy_songs)/len(features)), '% of tracks fell below the threshold')
    print('-------------------------------------')

    print('Tracks that are low (< 95) tempo: \n')
    print_songs(low_tempo_songs)
    print()
    print(len(low_tempo_songs), '/', len(features),
        ':', percent(len(low_tempo_songs)/len(features)), '% of tracks fell below the threshold')
    print('-------------------------------------')

    print('Tracks with low (< 65) danceability: \n')
    print_songs(low_danceability_songs)
    print()
    print(len(low_danceability_songs), '/', len(features),
        ':', percent(len(low_danceability_songs)/len(features)), '% of tracks fell below the threshold')
    print('-------------------------------------')

    print('Tracks with low (< 0.50) valence: \n')
    print_songs(low_valence_songs)
    print()
    print(len(low_valence_songs), '/', len(features), 
        ':', percent(len(low_valence_songs)/len(features)), '% of tracks fell below the threshold')
    print('-------------------------------------')

    print('Tracks in minor key: \n')
    print_songs(minor_key_songs)
    print()
    print(len(minor_key_songs), "/", len(features),
        ":", percent(len(minor_key_songs)/len(features)), '% of tracks were in the key of minor')
    print('-------------------------------------')
    print()

comedown_uri = 'spotify:playlist:4fIifdSKMpwcXTRO8B40j3'
comeup_uri = 'spotify:playlist:3qTUrOWQdXwc7jh1bn9Sib'

print('\nWelcome to Spotipy! Please choose a selection: \n')
print('   1. Playlist analysis for \'Comeup\'')
print('   2. Playlist analysis for \'Comedown\'')
print('   3. Side-by-side comparison')
print('   4. Generate songs for current weather')

choice = input('\nSelection: ')

if int(choice) == 1:
    print('\nDisplaying playlist features for Comeup...')
    display_playlist_features(comeup_uri)
elif int(choice) == 2:
    print('\nDisplaying playlist features for Comedown...')
    display_playlist_features(comedown_uri)
elif int(choice) == 3:
    print('\nCreating comparison for two both playlists...')
    time.sleep(2.5)
    print('\n*---------- DATA FEATURES: Comedown ----------*')
    print('\nEnergy: 73% of tracks fell below 0.75')
    print('\nTempo: 21% of tracks fell below 95 BPM')
    print('\nDanceability: 50% of tracks fell below 0.65')
    print('\nValence: 67% of tracks fell below 0.50')
    print('\n*---------- DATA FEATURES: Comeup ----------*')
    print('\nEnergy: 40% of tracks fell below 0.75')
    print('\nTempo: 10% of tracks fell below 95 BPM')
    print('\nDanceability: 27% of tracks fell below 0.65')
    print('\nValence: 37% of tracks fell below 0.50')
elif int(choice) == 4:
    location = input('Please enter your current location: ')

    key = 'e578acfe3a0075fde4a5ccf2d1771864'
    weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location, key)
    weather_map_res = requests.get(weather_map_url)
    data = weather_map_res.json()

    temp = data['main']['temp']
    temp = (temp - 273.15) * (9 / 5) + 32
    desc = data['weather'][0]['main']

    if desc == 'Clouds':
        print('\nLooks like it\'s a little gloomy in ' + location + ' right now :( Here are some songs for staying in bed all day:\n')
        print_recommendations(get_reccomendations_for_bad_weather(get_recommendations_for_top_artists(get_top_artists())))
    elif desc == 'Clear':
        print('\nLooks like it\'s nice and sunny in ' + location + ' right now! Here are some songs for you:\n')
        print_recommendations(get_reccomendations_for_good_weather(get_recommendations_for_top_artists(get_top_artists())))
