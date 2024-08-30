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

st.set_page_config(page_title="Spotify Song Analysis", page_icon=':musical_note:')

st.title('Analysis for Your Top Songs')
st.write('Discover insights about your spotify listening habits')

limit = 10
time_range = 'long_term'

top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)

top_artits = sp.current_user_top_artists(limit=limit, time_range=time_range)

track_ids = [track['id']for track in top_tracks['items']]

audio_features = sp.audio_features(track_ids)


df = pd.DataFrame(audio_features)

df['track_name'] = [track['name'] for track in top_tracks['items']]

df = df[['track_name', 'danceability', 'energy', 'instrumentalness']]

df.set_index('track_name', inplace=True)

st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height=500, x_label='Song Title')


