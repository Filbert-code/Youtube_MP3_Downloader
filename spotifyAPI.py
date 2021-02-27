from __future__ import unicode_literals
import re
import spotipy
import youtube_dl
import urllib.request
import time
import glob
import os

CLIENT_ID = '7478f0f30f9b4ad38f4814deb7bbac67'
CLIENT_SECRET = '2aa8a992152e4571a3754e588b8fd2c4'

PLAYLIST_NAME = ['Coding', 'Hacking']
PLAYLIST_USERNAME = 'dewanderer'
PLAYLIST_ID = ''

curr_directory = os.getcwd()


def spotify_track_names():
    tracks = []
    token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    cache_token = token.get_access_token()
    if token:
        spotify = spotipy.Spotify(cache_token)

        # playlists = spotify.user_playlists(PLAYLIST_USERNAME)
        # for item in playlists['items']:
        #     if PLAYLIST_NAME[0] in item['name'] and PLAYLIST_NAME[1] in item['name']:
        #         PLAYLIST_ID = item['id']
        #         print(item['name'])
        #         print(item['id'])

        results = spotify.user_playlist_tracks(PLAYLIST_USERNAME, PLAYLIST_ID)
        tracks_res = results['items']
        while results['next']:
            results = spotify.next(results)
            tracks_res.extend(results['items'])
        for res in tracks_res:
            #print(res['track']['name'] + " - " + res['track']['artists'][0]['name'])
            tracks.append(res['track']['name'] + " - " + res['track']['artists'][0]['name'])
    return tracks

def youtube_to_mp3(track_links):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    for count, track in enumerate(track_links):
        print('Downloading track #' + str(count + 1))
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([track])
        except Exception as e:
            print(track + " - " + str(e))

def get_youtube_links(track_names):
    track_links = []
    url = 'https://www.youtube.com/results?search_query='
    headers = {'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    for count, track in enumerate(track_names):
        print("Youtube links found: " + str(count + 1))
        track = track.replace(" ", "+")
        track_url = url + track
        try:
            html = urllib.request.urlopen(track_url)
        except Exception as e:
            print(e)
            continue
        try:
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            track_link = 'https://www.youtube.com/watch?v=' + video_ids[0]
            track_links.append(track_link)
        except Exception as e:
            print(e)
    return track_links


def append_to_file(file_name, list):
    with open(file_name, 'w') as writer:
        for item in list:
            writer.writelines(item + "\n")


def text_to_track_links(file):
    links = []
    with open(file, 'r') as reader:
        for line in reader:
            links.append(line)
    return links


if __name__ == '__main__':
    playlist_dict = {
        'alexlingfungfilbert':'2bO250NJik0KArLd0Gr9Sz',
        'david':'7JirxyGz96TkdPzVK40Rdw',
        'gmerdelta':'79EflHPZ5AaGikNUFbRGp6',
        'Oscar Lallier': '6yPiKpy7evrwvZodByKvM9',
    }

    # for username in playlist_dict:
    #     PLAYLIST_USERNAME = username
    #     PLAYLIST_ID = playlist_dict[username]
    #     tracks = spotify_track_names()
    #     track_links = get_youtube_links(tracks)
    #     append_to_file(username + '.txt', track_links)

    # gets filenames for all text files in the current directory
    link_files = glob.glob('*.txt')
    print(link_files)
    for file in link_files:
        track_links = text_to_track_links(file)
        print('GOT YOUTUBE LINKS -- Size: ' + str(len(track_links)))
        youtube_to_mp3(track_links)



