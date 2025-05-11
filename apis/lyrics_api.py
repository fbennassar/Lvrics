"""LyricsOVH API module."""

import requests


def get_lyrics(artist: str, song: str) -> str:
    """Fetch lyrics for a given artist and song title.

    Args:
        artist (str): The name of the artist.
        song (str): The title of the song.

    Returns:
        str: The lyrics of the song or an error message.
    """
    url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        return response.json().get("lyrics", "No lyrics found.")
    else:
        return "Error: Unable to fetch lyrics. Please check the artist and song title."
