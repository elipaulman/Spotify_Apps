import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# Set up Spotify API credentials and authentication
scope = "user-read-recently-played user-top-read playlist-modify-private"
client_id = "78a4698f20204bc6a14509b82dd8b954"
client_secret = "edde5b5b8f72476fa787a4ee8a84d0b9"
redirect_uri = "http://localhost:8888/callback"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Extract the playlist ID from the link
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXcE1QMIy9azKM"
playlist_id = playlist_link.split('/')[-1].split('?')[0]

# Get user's ID
user_id = sp.current_user()['id']

# Get playlist information
try:
    playlist = sp.playlist(playlist_id, fields='name,tracks')
except spotipy.exceptions.SpotifyException as e:
    if e.http_status == 404:
        print("Playlist not found.")
        exit()
    else:
        raise e

playlist_name = playlist['name']
last_updated = playlist['tracks']['items'][0]['added_at'].split('T')[0]

# Create a new playlist with the name "Discover Weekly - Last Updated Date"
new_playlist_name = f"{playlist_name} - {last_updated}"
new_playlist = sp.user_playlist_create(user=user_id, name=new_playlist_name, public=False)

# Get all tracks from the original playlist
tracks = playlist['tracks']['items']
track_ids = [track['track']['id'] for track in tracks]

# Add tracks to the new playlist
sp.playlist_add_items(new_playlist['id'], track_ids)

print(f"New playlist '{new_playlist_name}' created and populated with {len(track_ids)} songs!")
