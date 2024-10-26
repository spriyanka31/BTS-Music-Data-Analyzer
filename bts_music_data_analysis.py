# -*- coding: utf-8 -*-
"""BTS_Music_Data_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lSyhMzuqTtd1ds5R08p7uu1vVhfwndmQ

# Install Required Libraries for spotify
"""

pip install requests pandas spotipy beautifulsoup4

"""# Authenticate with Spotify"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify authentication
CLIENT_ID = 'ad439884a7db417ea25fbc87e99d3642'
CLIENT_SECRET = '07d349ae57484fbdba278cdd4d3e237e'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""# Fetch BTS Song Metadata: Use the Spotify API to search for BTS songs and collect relevant metadata."""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from IPython.display import display
from datetime import datetime

# Set your client ID and client secret
client_id = 'YOUR_CLIENT_ID'        # Replace with your Client ID
client_secret = 'YOUR_CLIENT_SECRET'  # Replace with your Client Secret

# Authenticate
credentials = SpotifyClientCredentials(client_id='ad439884a7db417ea25fbc87e99d3642', client_secret='07d349ae57484fbdba278cdd4d3e237e')
sp = spotipy.Spotify(client_credentials_manager=credentials)

# Search for BTS songs
results = sp.search(q='BTS', type='track', limit=50)  # Adjust the limit as needed

# Extract metadata
bts_songs = []
for track in results['tracks']['items']:
    song_data = {
        'name': track['name'],
        'artists': [artist['name'] for artist in track['artists']],
        'album': track['album']['name'],
        'release_date': track['album']['release_date'],
        'popularity': track['popularity'],
        'duration_ms': track['duration_ms'],
        'url': track['external_urls']['spotify'],
    }
    bts_songs.append(song_data)

# Create a DataFrame
bts_songs_df = pd.DataFrame(bts_songs)

# Add extra features
bts_songs_df['release_year'] = pd.to_datetime(bts_songs_df['release_date']).dt.year
bts_songs_df['artist_count'] = bts_songs_df['artists'].apply(len)
current_year = datetime.now().year
bts_songs_df['track_age'] = current_year - bts_songs_df['release_year']

# Retrieve Audio Features
def get_audio_features(track_id):
    features = sp.audio_features(track_id)[0]
    if features is not None:
        return {
            'danceability': features.get('danceability', 0),
            'energy': features.get('energy', 0),
            'valence': features.get('valence', 0),
            'tempo': features.get('tempo', 0),
            'loudness': features.get('loudness', 0),
        }
    return {
        'danceability': None,
        'energy': None,
        'valence': None,
        'tempo': None,
        'loudness': None,
    }

# Add audio features to DataFrame
audio_features = []
for track in results['tracks']['items']:
    audio_feature_data = get_audio_features(track['id'])
    audio_features.append(audio_feature_data)

# Create a DataFrame for audio features and concatenate with existing DataFrame
audio_features_df = pd.DataFrame(audio_features)
bts_songs_df = pd.concat([bts_songs_df, audio_features_df], axis=1)

# Export the DataFrame to a CSV file
output_file = 'bts_songs.csv'
bts_songs_df.to_csv(output_file, index=False)

# Fill NaN values with zeros (optional)
bts_songs_df.fillna(0, inplace=True)
bts_songs_df.index = bts_songs_df.index + 1
# Display the updated DataFrame
display(bts_songs_df)

"""# Data Analysis

1. Data Cleaning
"""

# Check for missing values
print(bts_songs_df.isnull().sum())

"""2. Descriptive Statistics"""

import pandas as pd

# Get descriptive statistics
desc_stats = bts_songs_df.describe()

# Reset index and add 1 to each index
desc_stats_reset = desc_stats.reset_index()
desc_stats_reset.index = desc_stats_reset.index + 1  # Start indexing from 1

# Display the descriptive statistics in table format
print(desc_stats_reset)

"""3. Data Grouping"""

# Average popularity by album
average_popularity = bts_songs_df.groupby('album')['popularity'].mean().reset_index()

# Sort in descending order
average_popularity = average_popularity.sort_values(by='popularity', ascending=False)

# Reset the index and start from 1
average_popularity.reset_index(drop=True, inplace=True)
average_popularity.index += 1  # Start index from 1

# Print the result in a structured format
print(average_popularity.to_string(index=True))

"""# Data visualization"""

#1. Bar Chart for Popularity by Song
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')  # Use seaborn style with a light background
# Set the figure size
plt.figure(figsize=(12, 8))
# Vertical bar chart for song popularity
plt.bar(bts_songs_df['name'], bts_songs_df['popularity'], color='#8A2BE2')
plt.xlabel('Song Name')
plt.ylabel('Popularity')
plt.title('POPULARITY OF BTS SONGS')
plt.xticks(rotation=90, ha='right')  # Rotate x labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
plt.show()

# 2. Line Chart for Popularity Over Time
plt.figure(figsize=(17, 9))
plt.subplot(2, 2, 3)
bts_songs_df.sort_values('release_date', inplace=True)
plt.plot(bts_songs_df['release_date'], bts_songs_df['popularity'], marker='o', linestyle='-')
plt.xlabel('Release Date')
plt.ylabel('Popularity')
plt.title('POPULARITY OF BTS SONGS OVER TIME')
plt.xticks(rotation=45)  # Rotate x labels for better readability
plt.grid()

# 3. Scatter Plot for Duration vs. Popularity
plt.figure(figsize=(17, 10))
plt.subplot(2, 2, 4)
bts_songs_df['duration_min'] = bts_songs_df['duration_ms'] / (1000 * 60)  # Convert milliseconds to minutes
plt.scatter(bts_songs_df['duration_min'], bts_songs_df['popularity'], color='orange')
plt.title('DURATION VS POPULARITY OF BTS SONGS')
plt.xlabel('Duration (minutes)')
plt.ylabel('Popularity')
plt.grid()

#4. Release Year Analysis
def release_year_analysis(df):
    avg_features_by_year = df.groupby('release_year')[['danceability', 'energy']].mean()
    avg_features_by_year.plot(kind='bar', figsize=(12, 6), color=['lightgreen', 'lightblue'])
    plt.title('Average Danceability and Energy of BTS Songs by Release Year')
    plt.xlabel('Release Year')
    plt.ylabel('Average Value')
    plt.xticks(rotation=45)
    plt.legend(['Danceability', 'Energy'])
    plt.show()

release_year_analysis(bts_songs_df)

"""The release year analysis reveals trends in BTS's music style regarding average danceability and energy over time. Increases or decreases in these features can indicate shifts in their musical direction, reflecting the impact of specific albums or events on their sound. Consistent values suggest stability in their style, while fluctuations may indicate experimentation with new genres."""

#Word Cloud of Song Titles
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Generate text from song titles
text = ' '.join(bts_songs_df['name'].tolist())

# Create the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Plot the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off axis
plt.title('Word Cloud of BTS Song Titles')
plt.show()

#5. Heatmap for Correlation Analysis
import seaborn as sns

def correlation_analysis(df):
    correlation = df[['popularity', 'danceability', 'energy', 'tempo']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation between Audio Features and Popularity')
    plt.show()

correlation_analysis(bts_songs_df)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Group by song name and album, then calculate the average popularity
avg_popularity = bts_songs_df.groupby(['name', 'album'])['popularity'].mean().reset_index()

# Create a mapping of songs to colors
unique_songs = avg_popularity['name'].unique()
colors = sns.color_palette("husl", len(unique_songs))  # Generate distinct colors
song_color_map = dict(zip(unique_songs, colors))  # Create a mapping of songs to colors

# Create a combined label for each song-album combination
avg_popularity['label'] = avg_popularity['name'] + ' - ' + avg_popularity['album']

# Plotting
plt.figure(figsize=(14, 7))

# Iterate over each unique song
for song in unique_songs:
    subset = avg_popularity[avg_popularity['name'] == song]
    plt.bar(subset['album'], subset['popularity'],
            label=song,
            color=song_color_map[song],
            alpha=0.7)

# Customize the plot
plt.title('Average Popularity of BTS Songs by Album')
plt.ylabel('Average Popularity')
plt.xlabel('Album')
plt.xticks(rotation=90)

# Create custom legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Remove duplicate labels
plt.legend(by_label.values(), by_label.keys(), title='Songs', loc='upper left', bbox_to_anchor=(1, 1), title_fontsize='13')

plt.tight_layout()
plt.grid(axis='y')
plt.show()