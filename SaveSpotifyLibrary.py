#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:33:45 2022

@author: cpiv
"""

import os
import io
import json
import spotipy
import spotipy.util as util
from slugify import slugify
from dotenv import load_dotenv

def iterate_playlist(spotify: spotipy.Spotify, output_file: io.TextIOWrapper, playlist):
  print(f"Indexing {playlist['name']}...")
  # write the playlist name to the top of the file, followed by colon and newline
  output_file.write(playlist["name"] + ":\n")
  playlist_id = playlist["id"]
  # default tracks limit is 100, here so no magic numbers
  tracks_limit = 100
  # pagination acculumator
  current_offset = 0
  while True:
    # get the playlist's tracks, then the 'items' array which contains the tracks
    tracks = spotify.playlist_tracks(
      playlist_id,
      limit=tracks_limit,
      offset=current_offset,
      # we only want the tracks, their names, and their artist(s) names
      fields="items(track(artists(name),name))"
    )["items"]

    # for each track, set track to track["track"] which contains the actual track (idk)
    for track in tracks:
      if track is None or track["track"] is None:
        print(f"Track was none: {json.dumps(track, indent=2)}")
        continue
      track = track["track"]
      artists_str = ", ".join([artist["name"] for artist in track["artists"]])
      # add all artists names to a list so they can be joined
      # for artist in track["artists"]:
      #   artists_str.append(artist["name"])
      output_file.write(f" - {track['name']} - {artists_str} \n")

    current_offset += len(tracks)

    if len(tracks) < tracks_limit:
      break

  print(f"Playlist {playlist['name']} has {current_offset} tracks.")

def iterate_playlists(spotify: spotipy.Spotify):
  # playlist default limit is 50, put here so no magic numbers
  playlists_limit = 50
  # pagination accumulator
  current_offset = 0
  while True:
    # get playlists from api and grab the 'items' array which contains the actual playlists
    playlists = spotify.current_user_playlists(
      offset=current_offset,
      limit=playlists_limit
    )["items"]

    # for each playlist, open a file with the playlists name and iterate it
    for playlist in playlists:
      filename = slugify(playlist['name'])
      if len(filename) == 0:
        filename = "blank"
      while os.path.exists(f"playlists/{filename}.txt"):
        filename += "1"
      with open(f"playlists/{filename}.txt", "x") as output_file:
        iterate_playlist(spotify, output_file, playlist)

    # otherwise accumulate the length for pagination
    current_offset += len(playlists)

    # if the len of the 'items' array is less than the limit, we must have hit the end, so break
    if len(playlists) < playlists_limit:
      break

  print(f"Indexed {current_offset} playlists")

# load a value from environment variables and exit if not found
def assert_env(env: str) -> str:
  value = os.getenv(env)
  if value is None:
    print(f"missing required environment variable: {env}")
    exit(1)
  value

# Example main (This is my spotify username tho feel free to browse my fire lists haha)
def main():
  # load variables from the .env file
  load_dotenv()

  username = assert_env("SPOTIFY_USERNAME")
  client_id = assert_env("SPOTIFY_CLIENT_ID")
  client_secret = assert_env("SPOTIFY_CLIENT_SECRET")
  playlist_dir = os.getenv("PLAYLIST_DIRECTORY", "playlists")

  scope = 'playlist-read-private'
  redirect_uri = 'https://google.com/'

  auth_man = spotipy.oauth2.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username,
    # this does not work in a few cases if `True`.
    # (namely on repl.it)
    # it is more portable to require the user to
    # click/copy the generated link, then paste
    # the code from the URL redirected to
    open_browser=False,
  )

  # Erase cache and start OAuth flow
  try:
      token = util.prompt_for_user_token(
        oauth_manager=auth_man,
        show_dialog=False,
      )
  except:
      os.remove(f".cache-{username}")
      token = util.prompt_for_user_token(
        oauth_manager=auth_man,
        show_dialog=False,
      )

  # Create spotify API client
  spotify = spotipy.Spotify(auth=token)

  try:
    os.mkdir(playlist_dir)
  except:
    pass
  # start iteration over all playlists in account
  iterate_playlists(spotify)

if __name__ == "__main__":
  main()
