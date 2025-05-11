"""Genius API integration."""

import requests


def get_genius_list(song: str, access_token: str) -> str:
    """Fetch lyrics for a given artist and song title from Genius."""
    url = f"https://api.genius.com/search?q={song}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, timeout=5)
    # Check if the request was successful
    response_data = response.json().get("response", {}).get("hits", [])[:10]
    results = []
    for hit in response_data:
        song_info = hit.get("result", {})
        song_title = song_info.get("title")
        artist_name = song_info.get("primary_artist", {}).get("name")
        # song_id = song_info.get("api_path")
        artist_song = song_title + " - " + artist_name
        results.append((artist_song))
        # print(results)

    if response.status_code == 200:
        # Parse the response to extract lyrics (this depends on Genius API's response structure)
        return results
    else:
        return "Error: Unable to fetch songs from Genius."
