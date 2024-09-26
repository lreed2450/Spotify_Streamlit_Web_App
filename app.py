# load libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

#load .env file and pull API key

load_dotenv()



CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000'


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      redirect_uri=REDIRECT_URI,
      scope='user-top-read' 

    )
)

st.set_page_config(page_icon=':musical_note:')

current_user = sp.current_user()['display_name']

st.header(f'Hello, {current_user}. Welcome to your Spotify Song Analysis :musical_note:', divider='rainbow')


st.subheader('Discover insights about your spotify listening habits')

st.write('**How far back should we look for your top songs and artists**')

option = st.selectbox(label="Choose an option.",
    options=("long_term", "medium_term", "short_term"),
)

if option =='long_term':
  st.write(f"You selected: {option}. We will pull data from up to a year ago.")

elif option =='medium_term':
  st.write(f"You selected: {option}. We will pull data from up to 6 months ago.")

else:
   st.write(f"You selected: {option}. We will pull data from up to 4 weeks ago.")


st.write('**How many songs should we analyze?**')

limit = st.slider(label='Choose an option.', min_value = 5, max_value = 20, step = 1)

st.write(f"You chose {limit} songs.")


def top_tracks(limit, time_range):
    """displays top n tracks based on limit and time range"""


    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)


    track_ids = [track['id']for track in top_tracks['items']]

    audio_features = sp.audio_features(track_ids)


    tracks_df = pd.DataFrame(audio_features)

    tracks_df['track_name'] = [track['name'] for track in top_tracks['items']]

    tracks_df = tracks_df[['track_name', 'danceability', 'energy', 'instrumentalness']]


    return tracks_df


def top_artists(limit, time_range):
    """displays top n artist based on limit and time range"""

    top_artists = sp.current_user_top_artists(limit=limit, time_range=time_range)

    artists_df = pd.DataFrame(columns=['artist_name', 'genres']) 

    idx = 0


    for artist in top_artists['items']:
        artist_name = top_artists['items'][idx]['name']
        genres = top_artists['items'][idx]['genres']
        artists_df.iloc[idx] = pd.concat({'artist_name': artist_name, 'genres': genres}, ignore_index=True)
        # artists_df = artists_df.append({'artist_name': artist_name, 'genres': genres}, ignore_index=True)
        idx += 1

    # artists_df.set_index(artists_df['artist_name'], inplace=True)

    return artists_df

tracks_df = top_tracks(limit, option)
artists_df = top_artists(limit, option)

tracks_df_for_chart = tracks_df.set_index('track_name', inplace=False)


st.subheader('Audio Features for Top Tracks')
st.bar_chart(tracks_df_for_chart, height=500, x_label='Song Title')

st.subheader('Top songs and artists')
st.dataframe(tracks_df, hide_index=True)

st.dataframe(artists_df, hide_index=True)


